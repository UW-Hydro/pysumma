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

    # Replaces the fileManager.txt placeholders with the paths/values for this system
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

    # Test the setting_path, input_path, and output_path FM objects (they represent paths, not files)
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

        # Save the old path values
        old_setting_path_value = self.Simulation_obj.setting_path.value
        old_input_path_value = self.Simulation_obj.input_path.value
        old_output_path_value = self.Simulation_obj.output_path.value

        # Set new values for the path variables
        new_setting_path_value = self.Simulation_obj.setting_path.value + "settingsample/"
        new_input_path_value = self.Simulation_obj.input_path.value + "inputsample/"
        new_output_path_value = self.Simulation_obj.output_path.value + "outputsample/"
        self.Simulation_obj.setting_path.value = new_setting_path_value
        self.Simulation_obj.input_path.value = new_input_path_value
        self.Simulation_obj.output_path.value = new_output_path_value

        # Did ModelOutput change them in the file?
        self.assertEqual(self.read_value_from_file('setting_path'), new_setting_path_value)
        self.assertEqual(self.read_value_from_file('input_path'), new_input_path_value)
        self.assertEqual(self.read_value_from_file('output_path'), new_output_path_value)

        # Change the values back
        self.Simulation_obj.setting_path.value = old_setting_path_value
        self.Simulation_obj.input_path.value = old_input_path_value
        self.Simulation_obj.output_path.value = old_output_path_value

        # Are the values updated correctly?
        self.assertEqual(self.read_value_from_file('setting_path'), old_setting_path_value)
        self.assertEqual(self.read_value_from_file('input_path'), old_input_path_value)
        self.assertEqual(self.read_value_from_file('output_path'), old_output_path_value)

    def test_FM_ModelOutput_obj(self):
        # Make sure that the ModelOutput object can read from the master file
        self.assertNotEqual([], self.Simulation_obj.modeloutput_obj.read_master_file())

        # Add a variable that's already in the file
        with self.assertRaises(ValueError):
            self.Simulation_obj.modeloutput_obj.add_variable('pptrate')

        # Add a valid variable and make sure it's in the file
        self.Simulation_obj.modeloutput_obj.add_variable('aquiferScaleFactor')
        self.assertIn('aquiferScaleFactor', self.Simulation_obj.modeloutput_obj.read_variables_from_file())

        # Remove that variable, make sure it isn't in the file
        self.Simulation_obj.modeloutput_obj.remove_variable('aquiferScaleFactor')
        self.assertNotIn('aquiferScaleFactor', self.Simulation_obj.modeloutput_obj.read_variables_from_file())

