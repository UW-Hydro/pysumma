#from Decisions import Decisions         # This is for testing in cmd window.
from pysumma.Option import Option
from .ProposedDecisions import Decisions       # This is for testing in this python code.
import subprocess
import os


class Simulation:
    executable = ''
    run_suffix = '_'

    def __init__(self, filepath):
        self.filepath = filepath
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


class FileManagerOption(Option):
    # key_position is the position in line.split() where the key name is
    # value_position is the position in line.split() where the value is
    # By default, delimiter=None, but can be set to split each line on different characters
    def __init__(self, name, file_manager_filepath):
        super().__init__(name, file_manager_filepath, key_position=2, value_position=0, delimiter=None)

    '''
        value is the thing read from the Simulation file-a filepath with or without a trailing '/'
        filepath adds a '/' to the value, if needed (does not contain the filename?)
        filename is the last part of the value-only the filename
        value = filepath + filename
    '''

    # TODO: Do we actually need a value and a filepath? What if we just added a trailing '/' to the value automatically?
    @property
    def value(self):
        return self.get_value()

    @value.setter
    def value(self, new_value):
        self.write_value(old_value=self.value, new_value=new_value)

    # TODO: What does this do? it just puts a '/' at the end of the value?
    # filepath is the path up to the filename, not including it
    @property
    def filepath(self):
        print("value: " + self.value)
        if not self.value.endswith('/'):
            return "/".join(self.value.split('/')[:-1]) + "/"
        else:
            return self.value

    @filepath.setter
    def filepath(self, new_filepath):
        value = new_filepath + self.filename
        self.write_value(old_value=self.value, new_value=value)

    # TODO: Do we want to just use Unix file URLS (dir/dir/file) or also Windows (dir\dir\file)?
    # Returns the file name of the FileManagerOption
    @property
    def filename(self):
        if self.value.endswith('/'):
            return self.value.split('/')[-2]
        else:
            return self.value.split('/')[-1]

    @filename.setter
    def filename(self, new_filename):
        value = self.filepath + new_filename
        self.write_value(old_value=self.value, new_value=value)
