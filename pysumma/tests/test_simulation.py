from unittest import TestCase
from shutil import copyfile
import os
from pysumma.Simulation import Simulation


class TestSimulation(TestCase):
    # Create a new fileManager.txt file with the correct file paths for the system it's run on
    my_path = os.path.abspath(os.path.dirname(__file__))
    whitespace = 50
    with open("fileManager.txt", "w") as file:
        file.write("'SUMMA FILE_MANAGER_V1.0'")
        file.write("! fman_ver\n".rjust(whitespace))
        file.write("'" + my_path + "/'")
        file.write("! setting_path\n".rjust(whitespace))
        file.write("'" + my_path + "/'")
        file.write("! input_path\n".rjust(whitespace))
        file.write("'" + my_path + "/'")
        file.write("! output_path\n".rjust(whitespace))
        # Take the template file (never changes) and append it to fileManager.txt
        with open("fileManagerTemplate.txt", "r") as template:
            for line in template:
                file.write(line)
        template.close()
        file.close()

    # Setting up test environment and creating Simulation object
    filename = 'fileManager.txt'
    filepath = os.path.join(my_path, filename)
    filename2 = 'tmp_{}'.format(filename)
    filepath2 = os.path.join(my_path, filename2)
    copyfile(filepath, filepath2)
    Simulation_obj = Simulation(filepath2)

    def read_value_from_file(self, setting_name):
        with open(self.filepath2) as fileManager_file:
            for line in fileManager_file:
                if setting_name in line:
                    return line.split("'")[1]

    def filepath_from_value(self, setting_name):
        value = self.read_value_from_file(setting_name)
        if not value.endswith('/'):
            return "/".join(value.split('/')[:-1]) + "/"
        else:
            return value

    def filename_from_value(self, setting_name):
        value = self.read_value_from_file(setting_name)
        return value.split('/')[-1]

    def read_text_from_file(self, setting_name):
        with open(self.read_value_from_file(setting_name)) as file:
            return ''.join(file.readlines())

    def value_filepath_filename_test(self, fileManagerObject, setting_name):
        assert fileManagerObject.name == setting_name, "FM Object name is: " + fileManagerObject.name + "; actual is: " + setting_name
        assert fileManagerObject.value == self.read_value_from_file(setting_name), "FM Object " + fileManagerObject.name + " value is: " + fileManagerObject.value + ", actual is: " + self.read_value_from_file(setting_name)
        assert fileManagerObject.filepath == self.filepath_from_value(setting_name), "FM Object " + fileManagerObject.name + " filepath is: " + fileManagerObject.filepath + ", actual is: " + self.filepath_from_value(setting_name)
        assert fileManagerObject.filename == self.filename_from_value(setting_name), "FM Object " + fileManagerObject.name + " filename is: " + fileManagerObject.filename + ", actual is: " + self.filename_from_value(setting_name)

    # Tests the value, filepath, and filename for all fileManager objects
    def test_value_filepath_filename(self):
        self.value_filepath_filename_test(self.Simulation_obj.setting_path, 'setting_path')
        self.value_filepath_filename_test(self.Simulation_obj.input_path, 'input_path')
        self.value_filepath_filename_test(self.Simulation_obj.output_path, 'output_path')
        self.value_filepath_filename_test(self.Simulation_obj.decision_path, 'decision')
        self.value_filepath_filename_test(self.Simulation_obj.meta_time, 'meta_time')
        self.value_filepath_filename_test(self.Simulation_obj.meta_attr, 'meta_attr')
        self.value_filepath_filename_test(self.Simulation_obj.meta_type, 'meta_type')
        self.value_filepath_filename_test(self.Simulation_obj.meta_force, 'meta_force')
        self.value_filepath_filename_test(self.Simulation_obj.meta_localpar, 'meta_localpar')
        self.value_filepath_filename_test(self.Simulation_obj.OUTPUT_CONTROL, 'OUTPUT_CONTROL')
        self.value_filepath_filename_test(self.Simulation_obj.meta_index, 'meta_index')
        self.value_filepath_filename_test(self.Simulation_obj.meta_basinpar, 'meta_basinpar')
        self.value_filepath_filename_test(self.Simulation_obj.meta_basinvar, 'meta_basinvar')
        self.value_filepath_filename_test(self.Simulation_obj.local_attr, 'local_attr')
        self.value_filepath_filename_test(self.Simulation_obj.local_par, 'local_par')
        self.value_filepath_filename_test(self.Simulation_obj.basin_par, 'basin_par')
        self.value_filepath_filename_test(self.Simulation_obj.forcing_list, 'forcing_list')
        self.value_filepath_filename_test(self.Simulation_obj.initial_cond, 'initial_cond')
        self.value_filepath_filename_test(self.Simulation_obj.para_trial, 'para_trial')
        self.value_filepath_filename_test(self.Simulation_obj.output_prefix, 'output_prefix')

    # Tests text contents for each fileManagerOption
    def test_file_text(self):
        return

