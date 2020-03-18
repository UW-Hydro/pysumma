import os
import copy
import shutil
import subprocess
import numpy as np
import xarray as xr
from pathlib import Path
from typing import List

from .decisions import Decisions
from .file_manager import FileManager
from .output_control import OutputControl
from .local_param_info import LocalParamInfo
from .force_file_list import ForceFileList


class Simulation():
    """The simulation object provides a wrapper for SUMMA simulations"""

    def __init__(self, executable, filemanager, initialize=True):
        """Initialize a new simulation object"""
        self.stdout = None
        self.stderr = None
        self.process = None
        self.executable = executable
        self.manager_path = Path(os.path.abspath(filemanager))
        self.config_path = self.manager_path.parent / '.pysumma'
        self.status = 'Uninitialized'
        if initialize:
            self.initialize()

    def initialize(self):
        self.manager = FileManager(
            self.manager_path.parent, self.manager_path.name)
        self.status = 'Initialized'
        self.decisions = self.manager.decisions
        self.output_control = self.manager.output_control
        self.parameter_trial = self.manager.parameter_trial
        self.force_file_list = self.manager.force_file_list
        self.local_param_info = self.manager.local_param_info
        self.basin_param_info = self.manager.basin_param_info
        self.local_attributes = self.manager.local_attributes
        self.initial_conditions = self.manager.initial_conditions
        self.genparm = self.manager.genparm
        self.mptable = self.manager.mptable
        self.soilparm = self.manager.soilparm
        self.vegparm = self.manager.vegparm
        self.create_backup()
        self.status = 'Initialized'

    def apply_config(self, config):
        if 'file_manager' in config:
            self.manager_path = Path(os.path.abspath(config['file_manager']))
        for k, v in config.get('decisions', {}).items():
            self.decisions.set_option(k, v)
        for k, v in config.get('parameters', {}).items():
            self.local_param_info.set_option(k, v)
        for k, v in config.get('output_control', {}).items():
            self.output_control.set_option(k, **v)
        for k, v in config.get('attributes', {}).items():
            self.assign_attributes(k, v)
        if self.decisions['snowLayers'] == 'CLM_2010':
            self.validate_layer_params(self.local_param_info)

    def assign_attributes(self, name, data):
        required_shape = self.local_attributes[name].shape
        try:
            self.local_attributes[name].values = np.array(data).reshape(required_shape)
        except ValueError as e:
            raise ValueError('The shape of the provided replacement data does',
                             ' not match the shape of the original data.', e)
        except KeyError as e:
            raise KeyError(f'The key {name} does not exist in this attribute',
                           'file. See the documentation at https://summa.readthedocs.',
                           'io/en/latest/input_output/SUMMA_input/#attribute-and-',
                           'parameter-files for more information', e)

    def create_backup(self):
        self.backup = {}
        self.backup['manager'] = copy.deepcopy(self.manager)
        self.backup['manager_path'] = copy.deepcopy(self.manager_path)

    def reset(self):
        self.manager = copy.deepcopy(self.backup['manager'])
        self.manager_path = copy.deepcopy(self.backup['manager_path'])
        self.config_path = self.manager_path.parent / '.pysumma'
        self.decisions = self.manager.decisions
        self.output_control = self.manager.output_control
        self.parameter_trial = self.manager.parameter_trial
        self.force_file_list = self.manager.force_file_list
        self.local_param_info = self.manager.local_param_info
        self.basin_param_info = self.manager.basin_param_info
        self.local_attributes = self.manager.local_attributes
        self.initial_conditions = self.manager.initial_conditions
        self.genparm = self.manager.genparm
        self.mptable = self.manager.mptable
        self.soilparm = self.manager.soilparm
        self.vegparm = self.manager.vegparm

    def validate_layer_params(self, params):
        for i in range(1, 5):
            assert (params[f'zmaxLayer{i}_upper']
                    <= params[f'zmaxLayer{i}_lower'], i)
            assert (params[f'zmaxLayer{i}_upper'] / params[f'zminLayer{i}']
                    >= 2.5, i)
            assert (params[f'zmaxLayer{i}_upper'] / params[f'zminLayer{i+1}']
                    >= 2.5, i)

    def _gen_summa_cmd(self, run_suffix, processes=1, prerun_cmds=[],
                       startGRU=None, countGRU=None, iHRU=None,
                       freq_restart=None, progress='m'):
        prerun_cmds.append('export OMP_NUM_THREADS={}'.format(processes))

        summa_run_cmd = "{} -s {} -m {}".format(self.executable,
                                                run_suffix, self.manager_path)

        if startGRU is not None and countGRU is not None:
            summa_run_cmd += ' -g {} {}'.format(startGRU, countGRU)
        if iHRU is not None:
            summa_run_cmd += ' -h {}'.format(iHRU)
        if freq_restart is not None:
            summa_run_cmd += ' -r {}'.format(freq_restart)
        if progress is not None:
            summa_run_cmd += ' -p {}'.format(progress)
        if len(prerun_cmds):
            preprocess_cmd = " && ".join(prerun_cmds) + " && "
        else:
            preprocess_cmd = ""

        return preprocess_cmd + summa_run_cmd

    def _run_local(self, run_suffix, processes=1, prerun_cmds=None,
                   startGRU=None, countGRU=None, iHRU=None, freq_restart=None,
                   progress=None):
        """Start a local simulation"""
        run_cmd = self._gen_summa_cmd(run_suffix, processes, prerun_cmds,
                                      startGRU, countGRU, iHRU, freq_restart,
                                      progress)
        self.process = subprocess.Popen(run_cmd, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, shell=True)
        self.status = 'Running'

    def _run_docker(self, run_suffix, processes=1,
                    prerun_cmds=None, startGRU=None, countGRU=None, iHRU=None,
                    freq_restart=None, progress=None):
        """Start a docker simulation"""
        run_cmd = self._gen_summa_cmd(run_suffix, processes, prerun_cmds,
                                      startGRU, countGRU, iHRU,
                                      freq_restart, progress)
        run_cmd = run_cmd.replace(self.executable, '/code/bin/summa.exe')

        fman_dir = os.path.dirname(self.manager_path)
        settings_path = self.manager['settings_path'].value
        input_path = self.manager['input_path'].value
        output_path = self.manager['output_path'].value
        cmd = ''.join(['docker run -v {}:{}'.format(fman_dir, fman_dir),
                       ' -v {}:{}'.format(settings_path, settings_path),
                       ' -v {}:{}'.format(input_path, input_path),
                       ' -v {}:{} '.format(output_path, output_path),
                       " --entrypoint '/bin/bash' ",
                       self.executable,
                       '  -c "',
                       run_cmd, '"'])
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, shell=True)
        self.status = 'Running'

    def start(self, run_option,  run_suffix='pysumma_run', processes=1,
              prerun_cmds=[], startGRU=None, countGRU=None, iHRU=None,
              freq_restart=None, progress=None):
        """Run a SUMMA simulation"""
        #TODO: Implement running on hydroshare here
        if not prerun_cmds:
            prerun_cmds = []
        self.run_suffix = run_suffix
        self._write_configuration(name=run_suffix)
        if run_option == 'local':
            self._run_local(run_suffix, processes, prerun_cmds,
                            startGRU, countGRU, iHRU, freq_restart, progress)
        elif run_option == 'docker':
            self._run_docker(run_suffix, processes, prerun_cmds,
                             startGRU, countGRU, iHRU, freq_restart, progress)
        else:
            raise NotImplementedError('Invalid runtime given! '
                                      'Valid options: local, docker')

    def run(self, run_option,  run_suffix='pysumma_run', processes=1,
            prerun_cmds=None, startGRU=None, countGRU=None, iHRU=None,
            freq_restart=None, progress=None):
        self.start(run_option, run_suffix, processes, prerun_cmds,
                   startGRU, countGRU, iHRU, freq_restart, progress)
        self.monitor()

    def monitor(self):
        # Simulation already run
        if self.status in ['Error', 'Success']:
            return self.status

        if self.process is None:
            raise RuntimeError('No simulation started! Use simulation.start '
                               'or simulation.execute to begin a simulation!')

        self.stdout, self.stderr = self.process.communicate()
        if isinstance(self.stdout, bytes):
            self.stderr = self.stderr.decode('utf-8', 'ignore')
            self.stdout = self.stdout.decode('utf-8', 'ignore')

        SUCCESS_MSG = 'FORTRAN STOP: finished simulation successfully.'
        if SUCCESS_MSG not in self.stdout:
            self.status = 'Error'
        else:
            self.status = 'Success'

        try:
            self._output = [xr.open_dataset(f) for f in self.get_output()]
            if len(self._output) == 1:
                self._output = self._output[0]
        except Exception:
            self._output = None


        return self.status

    def _write_configuration(self, name, write_netcdf: str=False):
        self.config_path = self.config_path / name
        self.config_path.mkdir(parents=True, exist_ok=True)
        manager_path = str(self.manager_path.parent)
        settings_path = str(self.manager['settings_path'].value)
        print(settings_path)
        print(manager_path)
        print(self.config_path)
        settings_path = Path(settings_path.replace(manager_path, str(self.config_path)))
        self.manager_path = self.config_path / self.manager.file_name
        self.manager['settings_path'] = str(settings_path) + os.sep
        self.manager.write(path=self.config_path)
        self.decisions.write(path=settings_path)
        self.force_file_list.write(path=settings_path)
        self.local_param_info.write(path=settings_path)
        self.basin_param_info.write(path=settings_path)
        self.output_control.write(path=settings_path)
        self.local_attributes.to_netcdf(settings_path / self.manager['local_attributes'].value)
        self.parameter_trial.to_netcdf(settings_path / self.manager['parameter_trial'].value)
        self.initial_conditions.to_netcdf(settings_path / self.manager['model_init_cond'].value)
        with open(settings_path / 'GENPARM.TBL', 'w+') as f:
            f.writelines(self.genparm)
        with open(settings_path / 'MPTABLE.TBL', 'w+') as f:
            f.writelines(self.mptable)
        with open(settings_path / 'SOILPARM.TBL', 'w+') as f:
            f.writelines(self.soilparm)
        with open(settings_path / 'VEGPARM.TBL', 'w+') as f:
            f.writelines(self.vegparm)

    def get_output(self) -> List[str]:
        new_file_text = 'Created output file:'
        out_files = []
        for l in self.stdout.split('\n'):
            if new_file_text in l:
                out_files.append(
                    l.split(';')[0].replace(new_file_text, '').strip())
        return out_files

    @property
    def output(self):
        if self.status == 'Success':
            return self._output
        elif self.status == 'Error':
            raise RuntimeError('There was an error during the simulation!'
                               ' Print the `stdout` and `stderr` for more'
                               ' information.')
        else:
            raise RuntimeError('No simulation started! Use simulation.start '
                               'or simulation.execute to begin a simulation!')

    def __repr__(self):
        repr = []
        repr.append("Executable path: {}".format(self.executable))
        repr.append("Simulation status: {}".format(self.status))
        repr.append("File manager configuration:")
        repr.append(str(self.manager))
        return '\n'.join(repr)
