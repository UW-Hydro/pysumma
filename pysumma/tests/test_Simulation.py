from unittest import TestCase
from shutil import copyfile
import os
from pysumma.Simulation import Simulation


class TestSimulation(TestCase):
    # Create a new fileManager.txt file with the correct file paths for the system it's run on
    my_path = os.path.abspath(os.path.dirname(__file__))
    filename = 'fileManager.txt'
    filepath = os.path.join(my_path, filename)
    filename2 = 'tmp_{}'.format(filename)
    filepath2 = os.path.join(my_path, filename2)
    copyfile(filepath, filepath2)

    with open(filepath2, 'r') as infile:
        text = infile.readlines()
    out_text = []
    for line in text:
        if '{file version}' in line:
            line = line.replace('{file version}', "'SUMMA FILE_MANAGER_V1.0'")
        if '{settings path}' in line:
            line = line.replace('{settings path}', "'" + my_path + "/'")
        if '{input path}' in line:
            line = line.replace('{input path}', "'" + my_path + "/'")
        if '{output path}' in line:
            line = line.replace('{output path}', "'" + my_path + "/'")
        out_text.append(line)
    with open(filepath2, 'w') as outfile:
        outfile.writelines(out_text)
    Simulation_obj = Simulation(filepath2)


    # Setting up test environment and creating Simulation object
    filepath2 = my_path + '/tmp_fileManager.txt'
    print("filepath2: " + filepath2)
    Simulation_obj = Simulation(filepath2)

    def read_value_from_file(self, setting_name):
        with open(self.filepath2) as fileManager_file:
            for line in fileManager_file:
                if setting_name in line:
                    return line.split("!")[0].strip().strip("'")

    def get_filepath_from_value(self, setting_name):
        value = self.read_value_from_file(setting_name)
        if not value.endswith('/'):
            return "/".join(value.split('/')[:-1]) + "/"
        else:
            return value

    def get_filename_from_value(self, setting_name):
        value = self.read_value_from_file(setting_name)
        return value.split('/')[-1]

    def read_text_from_file(self, setting_name):
        with open(self.read_value_from_file(setting_name)) as file:
            return ''.join(file.readlines())

    #  Test the setting_path, input_path, and output_path FM objects (they represent paths, not files)
    def test_path_FM_objects(self):
        # Are the names, values, filepaths, and filenames correct upon FileManagerOption object instantiation?
        fileManagerObject = self.Simulation_obj.setting_path
        setting_name = 'setting_path'
        self.assertEqual(fileManagerObject.name, setting_name)
        self.assertEqual(fileManagerObject.value, self.read_value_from_file(setting_name))
        self.assertEqual(fileManagerObject.filepath, self.get_filepath_from_value(setting_name))
        self.assertEqual(fileManagerObject.filename, self.get_filename_from_value(setting_name))

        fileManagerObject = self.Simulation_obj.input_path
        setting_name = 'input_path'
        self.assertEqual(fileManagerObject.name, setting_name)
        self.assertEqual(fileManagerObject.value, self.read_value_from_file(setting_name))
        self.assertEqual(fileManagerObject.filepath, self.get_filepath_from_value(setting_name))
        self.assertEqual(fileManagerObject.filename, self.get_filename_from_value(setting_name))

        fileManagerObject = self.Simulation_obj.output_path
        setting_name = 'output_path'
        self.assertEqual(fileManagerObject.name, setting_name)
        self.assertEqual(fileManagerObject.value, self.read_value_from_file(setting_name))
        self.assertEqual(fileManagerObject.filepath, self.get_filepath_from_value(setting_name))
        self.assertEqual(fileManagerObject.filename, self.get_filename_from_value(setting_name))


        # Change the value of the paths in the fileManagerOption objects, and save the old ones
        old_setting_path_value = self.Simulation_obj.setting_path.value
        old_input_path_value = self.Simulation_obj.input_path.value
        old_output_path_value = self.Simulation_obj.output_path.value

        new_setting_path_value = self.Simulation_obj.setting_path.value + "settingsample/"
        new_input_path_value = self.Simulation_obj.input_path.value + "inputsample/"
        new_output_path_value = self.Simulation_obj.output_path.value + "outputsample/"
        self.Simulation_obj.setting_path.value = new_setting_path_value
        self.Simulation_obj.input_path.value = new_input_path_value
        self.Simulation_obj.output_path.value = new_output_path_value
        self.assertEqual(self.read_value_from_file('setting_path'), new_setting_path_value)
        self.assertEqual(self.read_value_from_file('input_path'), new_input_path_value)
        self.assertEqual(self.read_value_from_file('output_path'), new_output_path_value)



        # Change the values back
        self.Simulation_obj.setting_path.value = old_setting_path_value
        self.Simulation_obj.input_path.value = old_input_path_value
        self.Simulation_obj.output_path.value = old_output_path_value

        # Are the values, filepaths, and filenames updated correctly?
        self.assertEqual(self.read_value_from_file('setting_path'), old_setting_path_value)
        self.assertEqual(self.read_value_from_file('input_path'), old_input_path_value)
        self.assertEqual(self.read_value_from_file('output_path'), old_output_path_value)


    # Tests the value, filepath, and filename for all fileManager objects
    # def test_file_FM_objects(self):
    #     self.name_value_filepath_filename_test(self.Simulation_obj.decision_path, 'decision')
    #
    #     self.name_value_filepath_filename_test(self.Simulation_obj.meta_time, 'meta_time')
    #     self.name_value_filepath_filename_test(self.Simulation_obj.meta_attr, 'meta_attr')
    #     self.name_value_filepath_filename_test(self.Simulation_obj.meta_type, 'meta_type')
    #     self.name_value_filepath_filename_test(self.Simulation_obj.meta_force, 'meta_force')
    #     self.name_value_filepath_filename_test(self.Simulation_obj.meta_localpar, 'meta_localpar')
    #     self.name_value_filepath_filename_test(self.Simulation_obj.OUTPUT_CONTROL, 'OUTPUT_CONTROL')
    #     self.name_value_filepath_filename_test(self.Simulation_obj.meta_index, 'meta_index')
    #     self.name_value_filepath_filename_test(self.Simulation_obj.meta_basinpar, 'meta_basinpar')
    #     self.name_value_filepath_filename_test(self.Simulation_obj.meta_basinvar, 'meta_basinvar')
    #
    #     self.name_value_filepath_filename_test(self.Simulation_obj.local_attr, 'local_attr')
    #     self.name_value_filepath_filename_test(self.Simulation_obj.local_par, 'local_par')
    #     self.name_value_filepath_filename_test(self.Simulation_obj.basin_par, 'basin_par')
    #     self.name_value_filepath_filename_test(self.Simulation_obj.forcing_list, 'forcing_list')
    #     self.name_value_filepath_filename_test(self.Simulation_obj.initial_cond, 'initial_cond')
    #     self.name_value_filepath_filename_test(self.Simulation_obj.para_trial, 'para_trial')
    #
    #     self.name_value_filepath_filename_test(self.Simulation_obj.output_prefix, 'output_prefix')
    #
    #
