import os
import subprocess

from pysumma.Option import Option
from pysumma.Decisions import Decisions
from pysumma.ModelOutput import ModelOutput
from pysumma.OutputControl import OutputControl


class Simulation(object):
    """
    A wrapper class around a SUMMA simulation.
    """
    proc = None

    def __init__(self, file_manager):
        """Constructor"""
        self.file_manager_path = os.path.abspath(file_manager)
        self.file_manager_dir = os.path.dirname(file_manager)
        with open(self.file_manager, 'r') as f:
            self.file_manager = f.readlines()
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
        self.output_control = FileManagerOption(self, 'output_control')
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
        self.decision_obj = Decisions(
                self.setting_path.value + self.decision_path.value)
        self.output_control = OutputControl(
                self.setting_path.value + self.output_control.value)
        self.modeloutput_obj = ModelOutput(
                self.setting_path.value + self.output_control.value)

    def execute(self, run_suffix, run_option, arglist=[]):
        self.run_suffix = run_suffix
        if run_option == 'local':
            cmd = "{} -p never -s {} -m {}".format(
                    self.executable, self.run_suffix, self.file_manager_path)
        elif run_option == "docker_latest":
            self.executable = 'bartnijssen/summa:latest'
            cmd = "".join([
                "docker run -v {}:{}".format(self.file_dir, self.file_dir),
                " -v {}:{}".format(
                    self.setting_path.filepath, self.setting_path.filepath),
                " -v {}:{}".format(
                    self.input_path.filepath, self.input_path.filepath),
                " -v {}:{}".format(
                    self.output_path.filepath, self.output_path.filepath),
                " {} -p never -s {} -m {}".format(
                    self.executable, self.run_suffix, self.filepath)])
        elif run_option == "docker_develop":
            self.executable = 'bartnijssen/summa:develop'
            cmd = "".join([
                "docker run -v {}:{}".format(self.file_dir, self.file_dir),
                " -v {}:{}".format(
                    self.setting_path.filepath, self.setting_path.filepath),
                " -v {}:{}".format(
                    self.input_path.filepath, self.input_path.filepath),
                " -v {}:{}".format(
                    self.output_path.filepath, self.output_path.filepath),
                " {} -p never -s {} -m {}".format(
                    self.executable, self.run_suffix, self.filepath)])
        else:
            raise ValueError('No executable defined. Set as "executable" '
                             'attribute of Simulation or check run_option')
        # run shell script in python
        preprocess = []
        if self.library_path:
            preprocess = ['export LD_LIBRARY_PATH="{}" && '.format(
                self.library_path)]
        if arglist:
            preprocess.append('{} && '.join(arglist))
        preprocess = "".join(preprocess)
        cmd = preprocess + " && " + cmd
        self.proc = subprocess.Popen(cmd, shell=True,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        # define output file name
        self.out_file_path = "".join([self.output_path.filepath,
                                      self.output_prefix.value, 'output_',
                                      self.run_suffix, '_timestep.nc'])
        return self.proc

    def monitor(self):
        """
        Wait until the simulation is finished and set
        variables for the return code, stdout, and stderr
        """
        if self.proc is None:
            return
        self.return_code = self.proc.wait()
        self.stdout = self.proc.stdout.read()
        self.stderr = self.proc.stderr.read()

    def set_decision(self, key, value):
        """Helper function for setting decision options"""
        self.decision_obj.__dict__[key].value = value


class FileManagerOption(Option):

    def __init__(self, parent, name):
        """
        key_position is the position in line.split() where the key name is
        value_position is the position in line.split() where the value is
        By default, delimiter=None, but can be set to split each line on
        different characters
        """
        super().__init__(name, parent, key_position=1,
                         value_position=0, delimiter="!")

    @property
    def value(self):
        return self.get_value()

    @value.setter
    def value(self, new_value):
        self.write_value(old_value=self.value, new_value=new_value)

    @property
    def filepath(self):
        """filepath is the path up to the filename, not including it"""
        if not self.value.endswith('/'):
            return "/".join(self.value.split('/')[:-1]) + "/"
        else:
            return self.value

    @filepath.setter
    def filepath(self, new_filepath):
        """Replace the filepath in the value in fileManager.txt"""
        value = new_filepath + self.filename
        self.write_value(old_value=self.value, new_value=value)

    @property
    def filename(self):
        """Returns the file name of the FileManagerOption"""
        return self.value.split('/')[-1]

    @filename.setter
    def filename(self, new_filename):
        value = self.filepath + new_filename
        self.write_value(old_value=self.value, new_value=value)
