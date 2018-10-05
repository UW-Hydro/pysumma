from pysumma.Decisions import Decisions
from pysumma.Option import Option
from pysumma.ModelOutput import ModelOutput
import os              # get directory or filename from filepath
import subprocess      # run shell script in python
import shlex           # splite shell script
import xarray as xr    # create xarray data from summa output (NetCDF file)
import glob

class Simulation:
    # set filepath parameter as a a directory and a filename of file manager text file
    def __init__(self, case_data, summa_code = None):
        # create self object from file manager text file
        self.filepath = os.path.abspath(case_data)
        self.file_dir = os.path.dirname(self.filepath)
        self.file_contents = self.open_read()
        self.fman_ver = FileManagerOption(self, 'fman_ver')
        self.setting_path = FileManagerOption(self, 'setting_path')
        self.input_path = FileManagerOption(self, 'input_path')
        self.output_path = FileManagerOption(self, 'output_path')
        self.decision_path = FileManagerOption(self, 'decision')
        self.meta_time = FileManagerOption(self, 'meta_time')
        self.meta_attr = FileManagerOption(self, 'meta_attr')
        self.meta_type = FileManagerOption(self, 'meta_type')
        self.meta_force = FileManagerOption(self, 'meta_force')
        self.meta_localpar = FileManagerOption(self, 'meta_localpar')
        self.OUTPUT_CONTROL = FileManagerOption(self, 'OUTPUT_CONTROL')
        self.meta_index = FileManagerOption(self, 'meta_index')
        self.meta_basinpar = FileManagerOption(self, 'meta_basinpar')
        self.meta_basinvar = FileManagerOption(self, 'meta_basinvar')
        self.local_attr = FileManagerOption(self, 'local_attr')
        self.local_par = FileManagerOption(self, 'local_par')
        self.basin_par = FileManagerOption(self, 'basin_par')
        self.forcing_list = FileManagerOption(self, 'forcing_list')
        self.initial_cond = FileManagerOption(self, 'initial_cond')
        self.para_trial = FileManagerOption(self, 'para_trial')
        self.output_prefix = FileManagerOption(self, 'output_prefix')
        self.base_dir = case_data.split('/settings')[0]
        # create self object from decision text file
        self.decision_obj = Decisions(self.base_dir + '/settings/' + self.decision_path.value)

        if summa_code == None:
            self.modeloutput_obj = ModelOutput(self.base_dir + '/settings/' + self.OUTPUT_CONTROL.value, self.base_dir + '/settings/meta/var_lookup.f90')
            self.summa_code = summa_code
        else:
            self.summa_code = summa_code
            self.modeloutput_obj = ModelOutput(self.base_dir + '/settings/' + self.OUTPUT_CONTROL.value,summa_code + '/build/source/dshare/var_lookup.f90')

    def open_read(self):
        # read filemanager text file
        with open(self.filepath, 'rt') as f:
            # read every line of filemanager and return as list format
            return f.readlines()

    def execute(self, run_option, run_suffix, specworker_img = None):
        # set run_suffix to distinguish the output name of summa
        self.run_suffix = run_suffix
        # 'local' run_option runs summa with summa execution file where is in a local computer.
        if run_option == 'local' :
            if self.summa_code == None:
                cmd = "{} -p never -s {} -m {}".format(self.executable, self.run_suffix, self.filepath)
                # run shell script in python and print output
                cmd = shlex.split(cmd)
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                output = p.communicate()[0].decode('utf-8')
                print(output)
                if 'FATAL ERROR' in output:
                    raise Exception("SUMMA failed to execute!")
                # define output file name as sopron version of summa
                out_file_path = self.output_path.filepath + \
                                self.output_prefix.value + '_output_' + \
                                self.run_suffix + '_timestep.nc'
            else:
                self.executable = self.summa_code + '/bin/summa.exe'
                cmd = "{} -p never -s {} -m {}".format(self.executable, self.run_suffix, self.filepath)
                # run shell script in python and print output
                cmd = shlex.split(cmd)
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                output = p.communicate()[0].decode('utf-8')
                print(output)
                if 'FATAL ERROR' in output:
                    raise Exception("SUMMA failed to execute!")
                # define output file name as sopron version of summa
                out_file_path = self.output_path.filepath + \
                                self.output_prefix.value + '_output_' + \
                                self.run_suffix + '_timestep.nc'


        # 'docker_sopron_2018' run_option runs summa with docker hub online, and the version name is "'uwhydro/summa:sopron_2018'.
        elif run_option == "docker_sopron_2018":
            self.executable = 'uwhydro/summa:sopron_2018'
            if self.file_dir+'/' == self.setting_path.filepath:
                cmd = "docker run -v {}:{}".format(self.file_dir, self.file_dir) + \
                      " -v {}:{}".format(self.input_path.filepath, self.input_path.filepath) + \
                      " -v {}:{}".format(self.output_path.filepath, self.output_path.filepath) + \
                      " {} -p never -s {} -m {}".format(self.executable, self.run_suffix, self.filepath)
            else:
                cmd = "docker run -v {}:{}".format(self.file_dir, self.file_dir) + \
                      " -v {}:{}".format(self.setting_path.filepath, self.setting_path.filepath) + \
                      " -v {}:{}".format(self.input_path.filepath, self.input_path.filepath) + \
                      " -v {}:{}".format(self.output_path.filepath, self.output_path.filepath) + \
                      " {} -p never -s {} -m {}".format(self.executable, self.run_suffix, self.filepath)
            # run shell script in python and print output
            cmd = shlex.split(cmd)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            output = p.communicate()[0].decode('utf-8')
            print(output)
            if 'FATAL ERROR' in output:
                raise Exception("SUMMA failed to execute!")
            # define output file name as sopron version of summa
            if self.output_path.filepath.split('/')[0] == '<BASEDIR>':
                out_file_path = self.output_path.filepath.split('<BASEDIR>')[1] + \
                                self.output_prefix.value + '_output_' + \
                                self.run_suffix + '_timestep.nc'
            else:
                out_file_path = self.output_path.filepath + \
                                self.output_prefix.value + '_output_' + \
                                self.run_suffix + '_timestep.nc'

        # "specworker" run_option run summa with summa image in docker of HydroShare Jupyter Hub
        elif run_option == "specworker":
            self.run_suffix = ""
            from specworker import jobs
            # define the image that we want to execute
            if specworker_img == 'cuahsi/summa:master':
                # save these paths in the env_vars dictionary which will be passed to the model
                env_vars = {'LOCALBASEDIR': self.base_dir, 'MASTERPATH': self.filepath}
                # define the location we want to mount these data in the container
                vol_target = '/tmp/summa'
                # define the base path of the input data for SUMMA
                vol_source = self.base_dir
                # run the container with the arguments specified above
                res = jobs.run(specworker_img, '-x', vol_source, vol_target, env_vars)

                list = glob.glob(self.base_dir + self.output_path.value.split('>')[1]+"*.nc")
                output_list = [x for x in list if self.output_prefix.value in x]
                myoutput_list = ' '.join(output_list[1:])
                if myoutput_list.count(self.output_prefix.value) > 1:
                    output_name = self.base_dir + self.output_path.value.split('>')[1] + \
                                self.output_prefix.value + '_' + \
                                self.decision_obj.simulStart.value[0:4] + '-' + \
                                self.decision_obj.simulFinsh.value[0:4] + '_' + \
                                self.run_suffix + '1.nc'
                    merge_netcdf = 'ncrcat ' + myoutput_list + ' -O ' + output_name
                    subprocess.run(merge_netcdf, shell=True)
                    myList = ' '.join(output_list[:])
                    delete_netcdf = 'rm -rf ' + myList
                    subprocess.run(delete_netcdf, shell=True)

                # define output file name as sopron version of summa
                out_file_path = self.base_dir + self.output_path.value.split('>')[1] + \
                                self.output_prefix.value + '_' + \
                                self.decision_obj.simulStart.value[0:4] + '-' + \
                                self.decision_obj.simulFinsh.value[0:4] + '_' + '1.nc'

            elif specworker_img == 'cuahsi/summa:sopron':
                # save these paths in the env_vars dictionary which will be passed to the model
                env_vars = {'LOCALBASEDIR': self.base_dir, 'MASTERPATH': self.filepath}
                # define the location we want to mount these data in the container
                vol_target = '/tmp/summa'
                # define the base path of the input data for SUMMA
                vol_source = self.base_dir
                # run the container with the arguments specified above
                res = jobs.run(specworker_img, '-x', vol_source, vol_target, env_vars)

                # define output file name as sopron version of summa
                out_file_path = self.base_dir + '/' + self.output_path.filepath.split('/')[1] + '/' + \
                                self.output_prefix.value + '_output_' + 'timestep.nc'

            else:
                raise ValueError('You need to deinfe the exact SUMMA_image_name')

        else:
            raise ValueError('No executable defined. Set as "executable" attribute of Simulation or check run_option')

        return xr.open_dataset(out_file_path), out_file_path

    def get_output(self, version, output_prefix):
        if version == "cuahsi_sopron_":
            out_file_path = self.base_dir + '/' + self.output_path.filepath.split('/')[1] + '/' + \
                            output_prefix + '_output_' + \
                            self.run_suffix + 'timestep.nc'
            xr_output = xr.open_dataset(out_file_path)
        elif version == "cuahsi_master":
            out_file_path = self.base_dir + self.output_path.value.split('>')[1] + \
                            output_prefix + '_' + \
                            self.decision_obj.simulStart.value[0:4] + '-' + \
                            self.decision_obj.simulFinsh.value[0:4] + '_' + '1.nc'
            xr_output = xr.open_dataset(out_file_path)
        elif version == "docker_sopron":
            if self.output_path.filepath.split('/')[0] == '<BASEDIR>':
                out_file_path = self.output_path.filepath.split('<BASEDIR>')[1] + \
                                self.output_prefix.value + '_output_' + \
                                self.run_suffix + '_timestep.nc'
            else:
                out_file_path = self.output_path.filepath + \
                                self.output_prefix.value + '_output_' + \
                                self.run_suffix + '_timestep.nc'
            xr_output = xr.open_dataset(out_file_path)
        else:
            raise ValueError('You need to write "cuahsi_sopron" or "cuahsi_master"or "docker_sorpon_" for version')
        return xr_output, out_file_path

class FileManagerOption(Option):

    # key_position is the position in line.split() where the key name is
    # value_position is the position in line.split() where the value is
    # By default, delimiter=None, but can be set to split each line on different characters
    def __init__(self, parent, name):
        super().__init__(name, parent, key_position=1, value_position=0, delimiter="!")

    # get value to change file manager value (value : a line divides by delimiter "!", and directory and filename are value)
    @property
    def value(self):
        return self.get_value()
    # change old value by new value
    @value.setter
    def value(self, new_value):
        self.write_value(old_value=self.value, new_value=new_value)

    # filepath is the path up to the filename, not including it
    @property
    def filepath(self):
        if not self.value.endswith('/'):
            return "/".join(self.value.split('/')[:-1]) + "/"
        else:
            return self.value

    # Replace the filepath in the value in fileManager.txt
    @filepath.setter
    def filepath(self, new_filepath):
        value = new_filepath + self.filename
        self.write_value(old_value=self.value, new_value=value)

    # Returns the file name of the FileManagerOption
    @property
    def filename(self):
        return self.value.split('/')[-1]

    @filename.setter
    def filename(self, new_filename):
        value = self.filepath + new_filename
        self.write_value(old_value=self.value, new_value=value)
