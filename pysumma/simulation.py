import os
import subprocess
import xarray as xr
import glob

from .decisions import Decisions
from .file_manager import FileManager
from .output_control import OutputControl
from .local_param_info import LocalParamInfo
from .force_file_list import ForceFileList


class Simulation(object):
    """The simulation object provides a wrapper for SUMMA simulations"""
    library_path = None
    process = None

    manager: FileManager = None
    decisions: Decisions = None
    output_control: OutputControl = None
    local_param_info: LocalParamInfo = None
    basin_param_info: LocalParamInfo = None
    force_file_list: ForceFileList = None
    local_attributes: xr.Dataset = None
    parameter_trial: xr.Dataset = None

    def __init__(self, executable, filemanager):
        """Initialize a new simulation object"""
        self.executable = executable
        self.manager_path = filemanager
        self.manager = FileManager(filemanager)
        self._status = 'Initialized'
        self.decisions = self.manager.decisions
        self.output_control = self.manager.output_control
        self.parameter_trial = self.manager.parameter_trial
        self.force_file_list = self.manager.force_file_list
        self.local_param_info = self.manager.local_param_info
        self.basin_param_info = self.manager.basin_param_info
        self.local_attributes = self.manager.local_attributes

    def exec_hydroshare(self, run_suffix, specworker_img=None):
        #TODO: This needs to be updated
        raise NotImplementedError('This needs to be updated')
        self.run_suffix = ""
        #TODO: This should be up top
        from specworker import jobs
        # define the image that we want to execute
        # save these paths in the env_vars dictionary
        # which will be passed to the model
        env_vars = {'LOCALBASEDIR': self.base_dir,
                    'MASTERPATH': self.manager_path}
        # define the location we want to mount these
        # data in the container
        vol_target = '/tmp/summa'
        # define the base path of the input data for SUMMA
        vol_source = self.base_dir
        # run the container with the arguments specified above
        res = jobs.run(specworker_img, '-x', vol_source,
                       vol_target, env_vars)

    def gen_summa_cmd(self, processes=1, prerun_cmds=[],
                  startGRU=None, countGRU=None, iHRU=None, freq_restart=None,
                  progress='m'):
        prerun_cmds.append('export OMP_NUM_THREADS={}'.format(processes))

        summa_run_cmd = "{} -s {} -m {}".format(self.executable,
                                                     self.run_suffix,
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

    def run_local(self, run_suffix=None, processes=1, prerun_cmds=[],
                  startGRU=None, countGRU=None, iHRU=None, freq_restart=None,
                  progress=None):
        run_cmd = self.gen_summa_cmd(processes, prerun_cmds,
                                     startGRU, countGRU, iHRU, freq_restart,
                                     progress)
        print(run_cmd)
        self.process = subprocess.Popen(run_cmd, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, shell=True)
        self._status = 'Running'

    def run_docker(self, docker_img, run_suffix=None, processes=1,
                   prerun_cmds=[], startGRU=None, countGRU=None, iHRU=None,
                   freq_restart=None, progress=None):
        self.executable = docker_img
        run_cmd = self.gen_summa_cmd(processes, prerun_cmds,
                                     startGRU, countGRU, iHRU,
                                     freq_restart, progress)

        fman_dir = os.path.dirname(self.manager_path.value)
        settings_path = self.manager.settings_path.value
        input_path = self.manager.input_path.value
        output_path = self.manager.output_path.value
        cmd = "".join(["docker run -v {}:{}".format(fman_dir, fman_dir),
                       " -v {}:{}".format(settings_path, settings_path),
                       " -v {}:{}".format(input_path, input_path),
                       " -v {}:{} ".format(output_path, output_path),
                       run_cmd])
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, shell=True)
        self._status = 'Running'

    def start(self, run_option,  run_suffix='pysumma_run', processes=1,
              prerun_cmds=[], startGRU=None, countGRU=None, iHRU=None,
              freq_restart=None, progress=None, docker_img=None):
        """Run a SUMMA simulation"""
        #TODO: Implement running on hydroshare here
        self.run_suffix=run_suffix
        self._write_configuration()
        if run_option == 'local':
            self.run_local(run_suffix, processes, prerun_cmds,
                           startGRU, countGRU, iHRU, freq_restart, progress)
        elif run_option == 'docker':
            self.run_docker(docker_img, run_suffix, processes, prerun_cmds,
                            startGRU, countGRU, iHRU, freq_restart, progress)

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
        assert self._status == 'Success'
        out_files = []
        for l in self.stdout.split('\n'):
            if new_file_text in l:
                out_files.append(l.replace(new_file_text, ''))
        return out_files

    def execute(self, run_option, run_suffix=None,
                preprocess_cmds=[], monitor=False):
        """Run a SUMMA simulation"""
        self.start(run_option, run_suffix, preprocess_cmds)
        if monitor:
            result = self.monitor()
            self.process = result
            return result
        else:
            return self.process

    def monitor(self):
        if self.process is None:
            raise RuntimeError('No simulation running! Use simulation.start '
                               'or simulation.execute to begin a simulation!')
        if self._status in ['Error', 'Success']:
            return self._status == 'Success'
        self._result = bool(self.process.wait())

        try:
            self._stderr = self.process.stderr.read().decode('utf-8')
            self._stdout = self.process.stdout.read().decode('utf-8')
        except UnicodeDecodeError:
            self._stderr = self.process.stderr.read()
            self._stdout = self.process.stdout.read()

        try:
            self._output = [xr.open_dataset(f) for f in self._get_output()]
            if len(self._output) == 1:
                self._output = self._output[0]
        except Exception:
            self._output = None
        if self._result:
            self._status = 'Error'
        else:
            self._status = 'Success'
        return self._result

    @property
    def result(self):
        if self.process is None:
            raise RuntimeError('No simulation started! Use simulation.start '
                               'or simulation.execute to begin a simulation!')
        elif isinstance(self.process, str):
            return self._status == 'Success'
        else:
            return self.monitor()

    @property
    def stdout(self):
        if self.process is None:
            raise RuntimeError('No simulation started! Use simulation.start '
                               'or simulation.execute to begin a simulation!')
        elif isinstance(self.process, str):
            return self._stdout
        else:
            self.monitor()
            return self._stdout

    @property
    def stderr(self):
        if self.process is None:
            raise RuntimeError('No simulation started! Use simulation.start '
                               'or simulation.execute to begin a simulation!')
        elif isinstance(self.process, str):
            return self._stderr
        else:
            self.monitor()
            return self._stderr

    @property
    def output(self):
        if self.process is None:
            raise RuntimeError('No simulation started! Use simulation.start '
                               'or simulation.execute to begin a simulation!')
        elif isinstance(self.process, str):
            return self._output
        else:
            self.monitor()
            return self._output

    def __repr__(self):
        repr = []
        repr.append("Executable path: {}".format(self.executable))
        repr.append("Simulation status: {}".format(self._status))
        repr.append("File manager configuration:")
        repr.append(str(self.manager))
        return '\n'.join(repr)
