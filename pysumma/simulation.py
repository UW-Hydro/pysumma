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
        self.run_suffix = run_suffix
        self.manager = FileManager(filemanager)
        self.decisions = self.manager.decisions
        self.output_control = self.manager.output_control
        self.parameter_trial = self.manager.parameter_trial
        self.force_file_list = self.manager.force_file_list
        self.local_param_info = self.manager.local_param_info
        self.basin_param_info = self.manager.basin_param_info
        self.local_attributes = self.manager.local_attributes
        self._status = 'Initialized'

    def execute(self, run_option, run_suffix, specworker_img=None):
        # set run_suffix to distinguish the output name of summa
        self.run_suffix = run_suffix
        # 'local' run_option runs summa with summa execution
        # file where is in a local computer.
        if run_option == 'local':
            if self.summa_code is None:
                cmd = "{} -p never -s {} -m {}".format(
                    self.executable, self.run_suffix, self.filepath)
                # run shell script in python and print output
                cmd = shlex.split(cmd)
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                output = p.communicate()[0].decode('utf-8')
                print(output)
                if 'FATAL ERROR' in output:
                    raise Exception("SUMMA failed to execute!")
                # define output file name as sopron version of summa
                out_file_path = (self.output_path.filepath
                                 + self.output_prefix.value + '_output_'
                                 + self.run_suffix + '_timestep.nc')
            else:
                self.executable = self.summa_code + '/bin/summa.exe'
                cmd = "{} -p never -s {} -m {}".format(
                    self.executable, self.run_suffix, self.filepath)
                # run shell script in python and print output
                cmd = shlex.split(cmd)
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                output = p.communicate()[0].decode('utf-8')
                print(output)
                if 'FATAL ERROR' in output:
                    raise Exception("SUMMA failed to execute!")
                # define output file name as sopron version of summa
                out_file_path = (self.output_path.filepath
                                 + self.output_prefix.value + '_output_'
                                 + self.run_suffix + '_timestep.nc')
        # 'docker_sopron_2018' run_option runs summa with docker hub online,
        # and the version name is "'uwhydro/summa:sopron_2018'.
        elif run_option == "docker_sopron_2018":
            self.executable = 'uwhydro/summa:sopron_2018'
            in_path = self.input_path.filepath
            out_path = self.output_path.filepath
            base_cmd = "docker run -v {}:{}".format(
                self.file_dir, self.file_dir)
            if self.file_dir+'/' == self.setting_path.filepath:
                cmd = (base_cmd
                       + " -v {}:{}".format(in_path, in_path)
                       + " -v {}:{}".format(out_path, out_path)
                       + " {} -p never -s {} -m {}".format(self.executable,
                                                           self.run_suffix,
                                                           self.filepath))
            else:
                setting_path = self.setting_path.filepath
                cmd = (base_cmd
                       + " -v {}:{}".format(setting_path, setting_path)
                       + " -v {}:{}".format(in_path, in_path)
                       + " -v {}:{}".format(out_path, out_path)
                       + " {} -p never -s {} -m {}".format(self.executable,
                                                           self.run_suffix,
                                                           self.filepath))
            # run shell script in python and print output
            cmd = shlex.split(cmd)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            output = p.communicate()[0].decode('utf-8')
            if 'FATAL ERROR' in output:
                raise Exception("SUMMA failed to execute!")
            # define output file name as sopron version of summa
            if self.output_path.filepath.split('/')[0] == '<BASEDIR>':
                out_file_path = (
                    self.output_path.filepath.split('<BASEDIR>')[1]
                    + self.output_prefix.value + '_output_'
                    + self.run_suffix + '_timestep.nc')
            else:
                out_file_path = (
                    self.output_path.filepath
                    + self.output_prefix.value + '_output_'
                    + self.run_suffix + '_timestep.nc')

        # "specworker" run_option run summa with summa image
        # in docker of HydroShare Jupyter Hub
        elif run_option == "specworker":
            self.run_suffix = ""
            from specworker import jobs
            # define the image that we want to execute
            if specworker_img == 'cuahsi/summa:master':
                # save these paths in the env_vars dictionary
                # which will be passed to the model
                env_vars = {'LOCALBASEDIR': self.base_dir,
                            'MASTERPATH': self.filepath}
                # define the location we want to mount these
                # data in the container
                vol_target = '/tmp/summa'
                # define the base path of the input data for SUMMA
                vol_source = self.base_dir
                # run the container with the arguments specified above
                res = jobs.run(specworker_img, '-x', vol_source,
                               vol_target, env_vars)

                list = glob.glob(self.base_dir
                                 + self.output_path.value.split('>')[1]+"*.nc")
                output_list = [x for x in list
                               if self.output_prefix.value in x]
                myoutput_list = ' '.join(output_list[1:])
                if myoutput_list.count(self.output_prefix.value) > 1:
                    output_name = (
                        self.base_dir + self.output_path.value.split('>')[1]
                        + self.output_prefix.value + '_'
                        + self.decision_obj.simulStart.value[0:4] + '-'
                        + self.decision_obj.simulFinsh.value[0:4] + '_'
                        + self.run_suffix + '1.nc')
                    merge_netcdf = ('ncrcat ' + myoutput_list
                                    + ' -O ' + output_name)
                    subprocess.run(merge_netcdf, shell=True)
                    myList = ' '.join(output_list[:])
                    delete_netcdf = 'rm -rf ' + myList
                    subprocess.run(delete_netcdf, shell=True)

                # define output file name as sopron version of summa
                out_file_path = (
                    self.base_dir + self.output_path.value.split('>')[1]
                    + self.output_prefix.value + '_'
                    + self.decision_obj.simulStart.value[0:4] + '-'
                    + self.decision_obj.simulFinsh.value[0:4] + '_' + '1.nc')

            elif specworker_img == 'cuahsi/summa:sopron':
                # save these paths in the env_vars dictionary
                # which will be passed to the model
                env_vars = {'LOCALBASEDIR': self.base_dir,
                            'MASTERPATH': self.filepath}
                # define the location we want to mount
                # these data in the container
                vol_target = '/tmp/summa'
                # define the base path of the input data for SUMMA
                vol_source = self.base_dir
                # run the container with the arguments specified above
                res = jobs.run(specworker_img, '-x', vol_source,
                               vol_target, env_vars)

                # define output file name as sopron version of summa
                out_file_path = (
                    self.base_dir + '/'
                    + self.output_path.filepath.split('/')[1] + '/'
                    + self.output_prefix.value + '_output_' + 'timestep.nc')

            else:
                raise ValueError('You need to deinfe the '
                                 'exact SUMMA_image_name')

        else:
            raise ValueError('No executable defined. '
                             'Set as "executable" attribute '
                             'of Simulation or check run_option')

        return xr.open_dataset(out_file_path), out_file_path

    def get_output(self, version, output_prefix=None, run_suffix=None):
        if version == "cuahsi_sopron":
            out_file_path = (self.base_dir + '/'
                             + self.output_path.filepath.split('/')[1] + '/'
                             + output_prefix + '_output_' + 'timestep.nc')
            xr_output = xr.open_dataset(out_file_path)
        elif version == "cuahsi_master":
            out_file_path = (
                self.base_dir + self.output_path.value.split('>')[1]
                + output_prefix + '_'
                + self.decision_obj.simulStart.value[0:4] + '-'
                + self.decision_obj.simulFinsh.value[0:4] + '_' + '1.nc')
            xr_output = xr.open_dataset(out_file_path)
        elif version == "docker_sopron":
            if self.output_path.filepath.split('/')[0] == '<BASEDIR>':
                out_file_path = (
                    self.output_path.filepath.split('<BASEDIR>')[1]
                    + self.output_prefix.value + '_output_'
                    + run_suffix + '_timestep.nc')
            else:
                out_file_path = (
                    self.output_path.filepath
                    + self.output_prefix.value + '_output_'
                    + run_suffix + '_timestep.nc')
            xr_output = xr.open_dataset(out_file_path)
        else:
            raise ValueError('You need to write "cuahsi_sopron" or'
                             ' "cuahsi_master"or "docker_sorpon" for version')
        return xr_output, out_file_path
