import os
import copy
import subprocess
import xarray as xr

from .decisions import Decisions
from .file_manager import FileManager
from .output_control import OutputControl
from .local_param_info import LocalParamInfo
from .force_file_list import ForceFileList


class Simulation():
    """The simulation object provides a wrapper for SUMMA simulations"""

    manager: FileManager = None
    decisions: Decisions = None
    output_control: OutputControl = None
    local_param_info: LocalParamInfo = None
    basin_param_info: LocalParamInfo = None
    force_file_list: ForceFileList = None
    local_attributes: xr.Dataset = None
    parameter_trial: xr.Dataset = None

    def __init__(self, executable, filemanager, initialize=True):
        """Initialize a new simulation object"""
        self.stdout = None
        self.stderr = None
        self.process = None
        self.executable = executable
        self.manager_path = filemanager
        self.status = 'Uninitialized'
        if initialize:
            self.initialize()

    def initialize(self):
        self.manager = FileManager(self.manager_path)
        self.status = 'Initialized'
        self.decisions = self.manager.decisions
        self.output_control = self.manager.output_control
        self.parameter_trial = self.manager.parameter_trial
        self.force_file_list = self.manager.force_file_list
        self.local_param_info = self.manager.local_param_info
        self.basin_param_info = self.manager.basin_param_info
        self.local_attributes = self.manager.local_attributes
        self.create_backup()
        self.status = 'Initialized'

    def apply_config(self, config):
        for k, v in config.get('file_manager', {}).items():
            self.manager.set_option(k, v)
        for k, v in config.get('decisions', {}).items():
            self.decisions.set_option(k, v)
        for k, v in config.get('parameters', {}).items():
            self.local_param_info.set_option(k, v)

    def create_backup(self):
        self.backup = {}
        self.backup['manager'] = copy.deepcopy(self.manager)

    def reset(self):
        self.manager = copy.deepcopy(self.backup['manager'])
        self.decisions = self.manager.decisions
        self.output_control = self.manager.output_control
        self.parameter_trial = self.manager.parameter_trial
        self.force_file_list = self.manager.force_file_list
        self.local_param_info = self.manager.local_param_info
        self.basin_param_info = self.manager.basin_param_info
        self.local_attributes = self.manager.local_attributes


    def _gen_summa_cmd(self, run_suffix, processes=1, prerun_cmds=[],
                       startGRU=None, countGRU=None, iHRU=None,
                       freq_restart=None, progress='m'):
        prerun_cmds.append('export OMP_NUM_THREADS={}'.format(processes))

        summa_run_cmd = "{} -s {} -m {}".format(self.executable,
                                                run_suffix,
                                                self.manager_path)

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
        self._write_configuration()
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

        if bool(self.process.wait()):
            self.status = 'Error'
        else:
            self.status = 'Success'

        try:
            self.stderr = self.process.stderr.read().decode('utf-8')
            self.stdout = self.process.stdout.read().decode('utf-8')
        except UnicodeDecodeError:
            self.stderr = self.process.stderr.read()
            self.stdout = self.process.stdout.read()

        try:
            self._output = [xr.open_dataset(f) for f in self._get_output()]
            if len(self._output) == 1:
                self._output = self._output[0]
        except Exception:
            self._output = None


        return self.status

    def _write_configuration(self):
        #TODO: Still need to update for all netcdf writing
        self.manager.write()
        self.decisions.write()
        self.force_file_list.write()
        self.local_param_info.write()
        self.basin_param_info.write()
        self.output_control.write()

    def _get_output(self):
        new_file_text = 'Created output file:'
        out_files = []
        for l in self.stdout.split('\n'):
            if new_file_text in l:
                out_files.append(l.replace(new_file_text, ''))
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
