import os
import subprocess
import shlex
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

    def __init__(self, executable, filemanager, run_suffix='_pysumma_run'):
        """Initialize a new simulation object"""
        self.executable = executable
        self.manager_path = filemanager
        self.manager = FileManager(filemanager)
        self.run_suffix = run_suffix
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

        if specworker_img == 'cuahsi/summa:master':
            list = glob.glob(self.base_dir
                             + self.output_path.value.split('>')[1]+"*.nc")
            output_list = [x for x in list
                           if self.output_prefix.value in x]
            myoutput_list = ' '.join(output_list[1:])
            if myoutput_list.count(self.output_prefix.value) > 1:
                output_name = (
                    self.base_dir + self.manager.output_path.value.split('>')[1]
                    + self.output_prefix.value + '_'
                    + self.decision_obj.simulStart.value[0:4] + '-'
                    + self.decision_obj.simulFinsh.value[0:4] + '_'
                    + self.run_suffix + '1.nc')
                #TODO: This could be done via xarray - also eneralized
                merge_netcdf = ('ncrcat ' + myoutput_list
                                + ' -O ' + output_name)
                subprocess.run(merge_netcdf, shell=True)
                myList = ' '.join(output_list[:])
                #TODO: This is a bad idea
                delete_netcdf = 'rm -rf ' + myList
                subprocess.run(delete_netcdf, shell=True)

            # define output file name as sopron version of summa
            out_file_path = (
                self.base_dir + self.output_path.value.split('>')[1]
                + self.output_prefix.value + '_'
                + self.decisions.simulStart.value[0:4] + '-'
                + self.decisions.simulFinsh.value[0:4] + '_' + '1.nc')

        elif specworker_img == 'cuahsi/summa:sopron':
            out_file_path = (
                self.base_dir + '/'
                + self.output_path.filepath.split('/')[1] + '/'
                + self.output_prefix.value + '_output_' + 'timestep.nc')
            #TODO: WHy doesn't this run anything?
        else:
            #TODO: This error message isn't specific enough
            raise ValueError('You need to deinfe the '
                             'exact SUMMA_image_name')
        return out_file_path

    def start(self, run_option, run_suffix=None, preprocess_cmds=[]):
        """Run a SUMMA simulation"""
        #TODO: Implement running on hydroshare here
        errstring = ('No executable defined. Set as "executable" attribute'
                     ' of Simulation or check run_option ')
        self._write_configuration()
        if run_suffix:
            self.run_suffix = run_suffix
        summa_run_cmd = "{} -p m -s {} -m {}".format(
                self.executable, self.run_suffix, self.manager_path)

        if run_option == 'local':
            cmd = summa_run_cmd
        elif run_option.startswith('docker'):

            if run_option == 'docker_latest':
                self.executable = 'bartnijssen/summa:latest'
            elif run_option == 'doocker_develop':
                self.executable = 'bartnijssen/summa:develop'
            else:
                raise ValueError(errstring)

            fman_dir = os.path.dirname(self.manager_path.value)
            settings_path = self.manager.settings_path.value
            input_path = self.manager.input_path.value
            output_path = self.manager.output_path.value
            cmd = "".join(["docker run -v {}:{}".format(fman_dir, fman_dir),
                           " -v {}:{}".format(settings_path, settings_path),
                           " -v {}:{}".format(input_path, input_path),
                           " -v {}:{} ".format(output_path, output_path),
                           summa_run_cmd])
        else:
            raise ValueError(errstring)

        preprocess = []
        if self.library_path:
            preprocess = ['export LD_LIBRARY_PATH="{}" '.format(
                self.library_path)]
        if len(preprocess_cmds):
            preprocess.append(' && '.join(preprocess_cmds))
        preprocess = "".join(preprocess)
        if len(preprocess):
            cmd = preprocess + " && " + cmd

        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, shell=True)
        self._status = 'Running'

    def _write_configuration(self):
        #TODO: Still need to update for all netcdf writing
        self.manager.write()
        self.decisions.write()
        self.force_file_list.write()
        self.local_param_info.write()
        self.basin_param_info.write()
        self.output_control.write()

    def _get_output(self):
        output_files = set()
        base_file = "".join(
            [self.manager.output_path.value, self.manager.output_prefix.value,
             'output_', self.run_suffix, '_{}.nc'])
        for o in self.output_control.options:
            if o.period == 1:
                output_files.add(base_file.format('timestep'))
            elif o.period > 1:
                output_files.add(base_file.format(o.statistic))
        return list(output_files)

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
