import os
import copy
import shutil
import subprocess
import numpy as np
import pandas as pd
import xarray as xr
from glob import glob
from pathlib import Path
from typing import List

from .decisions import Decisions
from .file_manager import FileManager
from .output_control import OutputControl
from .global_params import GlobalParams
from .force_file_list import ForcingList, ForcingOption


class Simulation():
    """
    The simulation object provides a wrapper for SUMMA simulations

    Attributes
    ----------
    stdout:
        Store standard output of the run
    stderr:
        Handle to the process during runtime
    manager_path:
        Path to the file manager
    config_path:
        Path to where configuration will be written
    status:
        Current status of the simulation
    manager:
        File manager object (populated after calling ``initialize``)
    decisions:
        Decisions object (populated after calling ``initialize``)
    output_control:
        OutputControl object (populated after calling ``initialize``)
    trial_params:
        Spatially distributed parameters (populated after calling ``initialize``)
    force_file_list:
        ForcingList object (populated after calling ``initialize``)
    global_hru_params:
        GlobalParams object for hru (populated after calling ``initialize``)
    global_gru_params:
        GlobalParams object for gru (populated after calling ``initialize``)
    local_attributes:
        LocalAttributes object (populated after calling ``initialize``)
    initial_conditions:
        InitialConditions object (populated after calling ``initialize``)
    """

    def __init__(self, executable, filemanager, initialize=True, config_dir='.pysumma'):
        """Initialize a new simulation object"""
        self.stdout = None
        self.stderr = None
        self.process = None
        self.executable = executable
        self.manager_path = Path(os.path.abspath(os.path.realpath(filemanager)))
        self.config_path = self.manager_path.parent / config_dir
        self.status = 'Uninitialized'
        if initialize:
            self.initialize()

    def initialize(self):
        """
        Initialize reads in all of the relevant files. This may not
        be desired on instantiation, so the ``initialize`` parameter
        can be set in the constructor. Calling this will also create
        a backup of the configuration that can be restored via the
        ``reset`` method.
        """
        self.manager = FileManager(
            self.manager_path.parent, self.manager_path.name)
        self.status = 'Initialized'
        self.decisions = self.manager.decisions
        self.output_control = self.manager.output_control
        self.trial_params = self.manager.trial_params
        self.force_file_list = self.manager.force_file_list
        self.global_hru_params = self.manager.global_hru_params
        self.global_gru_params = self.manager.global_gru_params
        self.local_attributes = self.manager.local_attributes
        self.initial_conditions = self.manager.initial_conditions
        self.genparm = self.manager.genparm
        self.mptable = self.manager.mptable
        self.soilparm = self.manager.soilparm
        self.vegparm = self.manager.vegparm
        self.create_backup()
        self.status = 'Initialized'

    def apply_config(self, config: dict):
        """
        Change the settings of the simulation based on a configuration
        dictionary.

        Parameters
        ----------
        config:
            A dictionary where keys represent the type of change and
            the values represent the changes to be applied. A representative
            example might be:

            ::
            config = {
                'file_manager': '/home/user/cool_setup/file_manager_new.txt',
                'decisions': {'snowLayers': 'CLM_2010'},
                'parameters': {'albedoDecayRate': 1e-6},
                'trial_parameters': {'theta_mp': 0.4},
                'attributes': {'mHeight': 15}
                }
        """
        if 'file_manager' in config:
            self.manager_path = Path(os.path.abspath(config['file_manager']))
        for k, v in config.get('decisions', {}).items():
            self.decisions.set_option(k, v)
        for k, v in config.get('parameters', {}).items():
            self.global_hru_params.set_option(k, v)
        for k, v in config.get('output_control', {}).items():
            self.output_control.set_option(k, **v)
        for k, v in config.get('attributes', {}).items():
            self.assign_attributes(k, v)
        for k, v in config.get('trial_parameters', {}).items():
            self.assign_trial_params(k, v)
        if self.decisions['snowLayers'] == 'CLM_2010':
            self.validate_layer_params(self.global_hru_params)

    def assign_attributes(self, name, data):
        """
        Assign new data to the ``local_attributes`` dataset.

        Parameters
        ----------
        name:
            The name (or key) of the attribute to modify
        data:
            The data to change the attribute to. The shape
            must match the shape in the local attributes file
        """
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

    def assign_trial_params(self, name, data, dim='hru', create=True):
        """
        Assign new data to the ``spatial_params`` dataset.

        Parameters
        ----------
        name:
            The name (or key) of the attribute to modify
        data:
            The data to change the parameter to. The shape
            must match the shape in the parameter trial file
        """
        # Create the variable if we need
        if create and name not in self.trial_params.variables:
            self.trial_params[name] = self.trial_params[dim].astype(float).copy()
        required_shape = self.trial_params[name].shape
        try:
            self.trial_params[name].values = np.array(data).reshape(required_shape)
        except ValueError as e:
            raise ValueError('The shape of the provided replacement data does',
                             ' not match the shape of the original data.', e)
        except KeyError as e:
            raise KeyError(f'The key {name} does not exist in this trial parameter',
                           'file. See the documentation at https://summa.readthedocs.',
                           'io/en/latest/input_output/SUMMA_input/#attribute-and-',
                           'parameter-files for more information', e)



    def create_backup(self):
        self.backup = {}
        self.backup['manager'] = copy.deepcopy(self.manager)
        self.backup['manager_path'] = copy.deepcopy(self.manager_path)

    def reset(self):
        """Restores the original settings of the Simulation"""
        self.manager = copy.deepcopy(self.backup['manager'])
        self.manager_path = copy.deepcopy(self.backup['manager_path'])
        self.config_path = self.manager_path.parent / '.pysumma'
        self.decisions = self.manager.decisions
        self.output_control = self.manager.output_control
        self.trial_params = self.manager.trial_params
        self.force_file_list = self.manager.force_file_list
        self.global_hru_params = self.manager.global_hru_params
        self.global_gru_params = self.manager.global_gru_params
        self.local_attributes = self.manager.local_attributes
        self.initial_conditions = self.manager.initial_conditions
        self.genparm = self.manager.genparm
        self.mptable = self.manager.mptable
        self.soilparm = self.manager.soilparm
        self.vegparm = self.manager.vegparm

    def validate_layer_params(self, params):
        """Ensure that the layer parameters are valid"""
        for i in range(1, 5):
            assert params[f'zmaxLayer{i}_upper'] \
                    <= params[f'zmaxLayer{i}_lower'], i
            assert params[f'zmaxLayer{i}_upper'] / params[f'zminLayer{i}'] \
                    >= 2.5, i
            assert params[f'zmaxLayer{i}_upper'] / params[f'zminLayer{i+1}'] \
                    >= 2.5, i

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
        settings_path = self.manager['settingsPath'].value
        input_path = self.manager['forcingPath'].value
        output_path = self.manager['outputPath'].value
        cmd = ''.join(['docker run -v {}:{}'.format(fman_dir, fman_dir),
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
              freq_restart=None, progress=None, **kwargs):
        """
        Run a SUMMA simulation without halting. Most likely this should
        not be used. Use the ``run`` method for most common use cases.
        """
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
            freq_restart=None, progress=None, **kwargs):
        """
        Run a SUMMA simulation and halt until completion or error.

        Parameters
        ----------
        run_option:
            Method to run SUMMA, must be one of either local or docker
        run_suffix:
            Name to append to the output files for this SUMMA run
        processes:
            Number of openmp processes to use for this run. For this
            to do anything SUMMA must be compiled with openmp support
        prerun_cmds:
            A list of commands to execute before running SUMMA. May be
            necessary to set environment variables or do any preprocessing
        startGRU:
            GRU index to start the simulation on (must also set ``countGRU``
            if this argument is set)
        countGRU:
            Number of GRU to run, starting at ``startGRU`` (must also set
            ``startGRU`` if this argument is set)
        iHRU:
            Index of HRU to run (cannot be used with ``startGRU`` and
            ``countGRU``)
        freq_restart:
            Frequency to write restart files. Options include
            ``[y, m, d, never]`` for yearly, monthly, and daily restart
            files. Defaults to ``never``
        progress:
            Frequency to write stdout progress. Note this is not printed
            during runtime via pysumma, but can be checked after completion.
            Options include ``[m, d, h, never]`` for monthly, daily, and
            hourly output.
        """
        self.start(run_option, run_suffix, processes, prerun_cmds,
                   startGRU, countGRU, iHRU, freq_restart, progress, **kwargs)
        self.monitor()

    def monitor(self):
        '''Halt execution until Simulation either finishes or errors'''
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
            self._output = [xr.open_dataset(f) for f in self.get_output_files()]
            if len(self._output) == 1:
                self._output = self._output[0]
        except Exception:
            self._output = None

        return self.status

    def spinup(self, run_option, period='1Y', niters=10, run_suffix='pysumma_spinup', **kwargs):
        # open forcings
        spinup_force_name = f'{run_suffix}.nc'
        with xr.open_mfdataset(self.force_file_list.forcing_paths) as ds:
            start_date = pd.to_datetime(ds['time'].values[0])
            end_date = pd.to_datetime(start_date + pd.Timedelta(period))
            forcings = ds.sel(time=slice(start_date, end_date)).load()
        spinup_force_path = self.manager['forcingPath'].value + spinup_force_name
        forcings.to_netcdf(spinup_force_path)
        self.force_file_list.options = [ForcingOption(spinup_force_path)]
        self.manager['simStartTime'] = start_date
        self.manager['simEndTime'] = end_date
        ymdh = str(self.manager['simEndTime'].value).replace(' ', '-').replace('-', '').split(':')[0]
        for n in range(niters):
            self.run(run_option, run_suffix=run_suffix, freq_restart='e', **kwargs)
            out_dir = self.manager['outputPath'].value
            prefix = self.manager['outFilePrefix'].value
            restart_file_name = f'{prefix}_restart_{ymdh}_{run_suffix}*nc'
            restart_file_path = glob(f'{out_dir}{restart_file_name}')[0]
            restart_file_name = restart_file_path.split(os.path.sep)[-1]
            self.reset()
            self.manager['simStartTime'] = start_date
            self.manager['simEndTime'] = end_date
            restart_dest = os.path.dirname(self.manager['initConditionFile'].value) + f'/{restart_file_name}'
            shutil.copy(restart_file_path, self.manager['settingsPath'].value + restart_dest)
            [os.remove(f) for f in self.get_output_files()]
            self.manager['initConditionFile'] = restart_dest
            with xr.open_dataset(self.manager['settingsPath'].value + restart_dest) as ds:
                self.initial_conditions = ds.load()

    def _write_configuration(self, name=''):
        import shutil

        self.config_path = self.config_path / name
        self.config_path.mkdir(parents=True, exist_ok=True)
        manager_path = str(self.manager_path.parent)
        settings_path = os.path.abspath(os.path.realpath(str(self.manager['settingsPath'].value)))
        settings_path = Path(settings_path.replace(manager_path, str(self.config_path)))

        self.manager_path = self.config_path / self.manager.file_name
        self.manager['settingsPath'] = str(settings_path) + os.sep
        self.manager.write(path=self.config_path)
        self.decisions.write(path=settings_path)
        self.force_file_list.write(path=settings_path)
        self.global_hru_params.write(path=settings_path)
        self.global_gru_params.write(path=settings_path)
        self.output_control.write(path=settings_path)
        self.local_attributes.to_netcdf(settings_path / self.manager['attributeFile'].value)
        self.trial_params.to_netcdf(settings_path / self.manager['trialParamFile'].value)
        self.initial_conditions.to_netcdf(settings_path / self.manager['initConditionFile'].value)
        with open(settings_path / self.manager['generalTableFile'].value, 'w+') as f:
            f.writelines(self.genparm)
        with open(settings_path / self.manager['noahmpTableFile'].value, 'w+') as f:
            f.writelines(self.mptable)
        with open(settings_path / self.manager['soilTableFile'].value, 'w+') as f:
            f.writelines(self.soilparm)
        with open(settings_path / self.manager['vegTableFile'].value, 'w+') as f:
            f.writelines(self.vegparm)

    def get_output_files(self) -> List[str]:
        """Find output files given the ``stdout`` generated from a run"""
        new_file_text = 'Created output file:'
        out_files = []
        for l in self.stdout.split('\n'):
            if new_file_text in l:
                out_files.append(
                    l.split(';')[0].replace(new_file_text, '').strip())
        return out_files

    @property
    def output(self):
        """Get the output as an xarray dataset"""
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
        try:
            repr.append("File manager configuration:")
            repr.append(str(self.manager))
        except:
            repr.append("Use Simulation.initialize() to "
                        "read input files for more information")
        return '\n'.join(repr)
