#from Decisions import Decisions         # This is for testing in cmd window.
from .Decisions import Decisions       # This is for testing in this python code.
import subprocess
import os
import xarray as xr

class Simulation:
    executable = ''
    def __init__(self, filepath):
        self.filepath = os.path.abspath(filepath)
        self.setting_path = FileManagerOption('setting_path', self.filepath)
        self.input_path = FileManagerOption('input_path', self.filepath)
        self.output_path = FileManagerOption('output_path', self.filepath)
        self.decision_path = FileManagerOption('decision', self.filepath)
        self.meta_time = FileManagerOption('meta_time', self.filepath)
        self.meta_attr = FileManagerOption('meta_attr', self.filepath)
        self.meta_type = FileManagerOption('meta_type', self.filepath)
        self.meta_force = FileManagerOption('meta_force', self.filepath)
        self.meta_localpar = FileManagerOption('meta_localpar', self.filepath)
        self.OUTPUT_CONTROL = FileManagerOption('OUTPUT_CONTROL', self.filepath)
        self.meta_index = FileManagerOption('meta_index', self.filepath)
        self.meta_basinpar = FileManagerOption('meta_basinpar', self.filepath)
        self.meta_basinvar = FileManagerOption('meta_basinvar', self.filepath)
        self.local_attr = FileManagerOption('local_attr', self.filepath)
        self.local_par = FileManagerOption('local_par', self.filepath)
        self.basin_par = FileManagerOption('basin_par', self.filepath)
        self.forcing_list = FileManagerOption('forcing_list', self.filepath)
        self.initial_cond = FileManagerOption('initial_cond', self.filepath)
        self.para_trial = FileManagerOption('para_trial', self.filepath)
        self.output_prefix = FileManagerOption('output_prefix', self.filepath)
        self.decision_obj = Decisions(self.setting_path.value + self.decision_path.value)

    def execute(self,     run_suffix):
        self.run_suffix = run_suffix
        if self.executable == '':
            raise ValueError('No executable defined. Set as "executable" attribute of Simulation')
        else:
            cmd = "{} -p never -s {}       -m {}".format(self.executable, self.run_suffix, self.filepath)
            subprocess.run(cmd, shell=True)
            out_file_path = 	self.output_path.filepath + \
						self.output_prefix.value+'_' + \
						self.decision_obj.simulStart.value[0:4] + '-' + \
						self.decision_obj.simulFinsh.value[0:4] + '_' + \
						self.run_suffix + '_1.nc'
            return xr.open_dataset(out_file_path)

class FileManagerOption:
    def __init__(self, name, filepath):
        self.name = name
        self.file_manager_filepath = filepath
        self.text = self.open_read()

    def open_read(self):
        with open(self.file_manager_filepath, 'rt') as f:
            return f.readlines()

    def get_line_no(self, name):
        for line_no, line_contents in enumerate(self.text):
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
        self.text[self.line_no] = self.line_contents.replace(self.value, new_value, 1)
        self.edit_save()

    def edit_save(self):
        with open(self.file_manager_filepath, 'wt') as f:
            f.writelines(self.text)

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

