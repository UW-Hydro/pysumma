#from Decisions import Decisions         # This is for testing in cmd window.
from pysumma.Decisions import Decisions       # This is for testing in this python code.
import subprocess
import os
import xarray as xr

class Simulation:
    def __init__(self, filepath):
        self.filepath = os.path.abspath(filepath)
        self.file_dir = os.path.dirname(self.filepath)
        self.file_manager_filepath = filepath
        self.file_contents = self.open_read()
        self.fman_ver = FileManagerOption(self,'fman_ver')
        self.setting_path = FileManagerOption(self,'setting_path')
        self.input_path = FileManagerOption(self,'input_path')
        self.output_path = FileManagerOption(self,'output_path')
        self.decision_path = FileManagerOption(self,'decision')
        self.meta_time = FileManagerOption(self,'meta_time')
        self.meta_attr = FileManagerOption(self,'meta_attr')
        self.meta_type = FileManagerOption(self,'meta_type')
        self.meta_force = FileManagerOption(self,'meta_force')
        self.meta_localpar = FileManagerOption(self,'meta_localpar')
        self.OUTPUT_CONTROL = FileManagerOption(self,'OUTPUT_CONTROL')
        self.meta_index = FileManagerOption(self,'meta_index')
        self.meta_basinpar = FileManagerOption(self,'meta_basinpar')
        self.meta_basinvar = FileManagerOption(self,'meta_basinvar')
        self.local_attr = FileManagerOption(self,'local_attr')
        self.local_par = FileManagerOption(self,'local_par')
        self.basin_par = FileManagerOption(self,'basin_par')
        self.forcing_list = FileManagerOption(self,'forcing_list')
        self.initial_cond = FileManagerOption(self,'initial_cond')
        self.para_trial = FileManagerOption(self,'para_trial')
        self.output_prefix = FileManagerOption(self,'output_prefix')
        self.decision_obj = Decisions(self.setting_path.value + self.decision_path.value)

    def open_read(self):
        with open(self.file_manager_filepath, 'rt') as f:
            return f.readlines()

    def execute(self, run_suffix, run_option):

        if run_option == 'local':
            executable = ''
            self.run_suffix = run_suffix
            cmd = "{} -p never -s {}       -m {}".format(self.executable, self.run_suffix, self.filepath)
            subprocess.run(cmd, shell=True)
            out_file_path = 	self.output_path.filepath + \
						self.output_prefix.value+'_' + \
						self.decision_obj.simulStart.value[0:4] + '-' + \
						self.decision_obj.simulFinsh.value[0:4] + '_' + \
						self.run_suffix + '_1.nc'
            return xr.open_dataset(out_file_path)

        elif run_option == "docker" :
#            dir = self.setting_path.filepath.split('/')[:-2]
#            mount_dir = '/'+dir[1]+'/'+dir[2]+'/'+dir[3]
#            self.disk_mapping = mount_dir + ':' + mount_dir
            self.executable = 'bartnijssen/summa:develop'
            self.run_suffix = run_suffix
            cmd = "docker run -v {}:{}".format(self.file_dir, self.file_dir)+ \
                            " -v {}:{}".format(self.setting_path.filepath, self.setting_path.filepath)+ \
                            " -v {}:{}".format(self.input_path.filepath, self.input_path.filepath)+ \
                            " -v {}:{}".format(self.output_path.filepath, self.output_path.filepath)+ \
                            " {} -p never -s {} -m {}".format(self.executable, self.run_suffix, self.filepath)
            subprocess.run(cmd, shell=True)
            out_file_path = self.output_path.filepath + \
						self.output_prefix.value+'_output_' + \
						self.run_suffix + '_timestep.nc'
            return xr.open_dataset(out_file_path)
        else:
            raise ValueError('No executable defined. Set as "executable" attribute of Simulation or check run_option')

class FileManagerOption:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.line_no, self.line_contents = self.get_line_no(self.name)
        # self.text = self.open_read()

    def get_line_no(self, name):
        for line_no, line_contents in enumerate(self.parent.file_contents):
            filepath_filename = line_contents.split("'")
            name1 = filepath_filename[2].split(" ")[-1].strip()
            if name1 == name:
                return line_no, line_contents

    def get_value(self):
        self.line_no, self.line_contents = self.get_line_no(self.name)
        words = self.line_contents.split("'")
        words = [w.strip() for w in words if w.strip() != "" and w.strip() != "!"]
        return words[0]

    def write_value(self, new_value):
        self.parent.file_contents[self.line_no] = self.line_contents.replace(self.value, new_value, 1)
        self.edit_save()

    def edit_save(self):
        with open(self.parent.filepath, 'wt') as f:
            f.writelines(self.parent.file_contents)

    @property
    def value(self):
        return self.get_value()


    @value.setter
    def value(self, new_value):
        self.write_value(new_value)

    @property
    def filepath(self):
        if not self.value.endswith('/'):
            return "/".join(self.value.split('/')[:-1]) + "/"
        else:
            return self.value

    @filepath.setter
    def filepath(self, new_value):
        value = new_value + self.filename
        self.write_value(value)

    @property
    def filename(self):
        return self.value.split('/')[-1]

    @filename.setter
    def filename(self, new_value):
        value = self.filepath + new_value
        self.write_value(value)

