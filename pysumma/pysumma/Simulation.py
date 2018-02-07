#from Decisions import Decisions         # This is for testing in cmd window.
from .Decisions import Decisions       # This is for testing in this python code.
import subprocess
import os

class Simulation:
    executable = ''
    run_suffix = '_'
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

    def execute(self):
        if self.executable == '':
            raise ValueError('No executable defined. Set as "executable" attribute of Simulation')
        else:
            cmd = "{} -p never -s {}       -m {}".format(self.executable, self.run_suffix, self.filepath)
            subprocess.run(cmd, shell=True)

class FileManagerOption:
    def __init__(self, name, filepath):
        self.name = name
        self.file_manager_filepath = filepath

    def open_read(self):
        with open(self.file_manager_filepath, 'rt') as f:
            self.text = f.readlines()
        return self.text

    def get_line_no(self, name):
        text = self.open_read()
        for line_no, line in enumerate(text):
            filepath_filename = line.split("'")
            name1 = filepath_filename[2].split(" ")[-1].strip()
            if name1 == name:
                return line_no, line

    def get_value(self):
        line_no, line = self.get_line_no(self.name)
        words = line.split("'")
        words = [w.strip() for w in words if w.strip() != "" and w.strip() != "!"]
        return words[0]

    def write_value(self, new_value):
        line_no, line = self.get_line_no(self.name)
        lines = self.open_read()
        lines[line_no] = line.replace(self.value, new_value, 1)
        self.edit_save(lines)

    def edit_save(self, new_lines):
        with open(self.file_manager_filepath, 'wt') as f:
            f.writelines(new_lines)

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

