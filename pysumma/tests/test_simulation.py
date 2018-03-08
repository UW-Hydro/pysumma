from unittest import TestCase
from shutil import copyfile
import os
from pysumma.Simulation import Simulation


class TestSimulation(TestCase):
    # Create a new fileManager.txt file with the correct file paths for the system it's run on
    my_path = os.path.abspath(os.path.dirname(__file__))
    print("Path: " + my_path)
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
        if value.endswith('/'):
            return value
        else:
            return '/'.join(value.split('/')[:-1])

    def filename_from_value(self, setting_name):
        value = self.read_value_from_file(setting_name)
        return value.split('/')[-1]

    def value_filepath_filename_lineno_test(self, fileManagerObject, setting_name):
        assert fileManagerObject.name == setting_name, "FM Object name is: " + fileManagerObject.name
        assert fileManagerObject.value == self.read_value_from_file(setting_name)
        assert fileManagerObject.filepath == self.filepath_from_value(setting_name)
        assert fileManagerObject.filename == self.filename_from_value(setting_name)
        return

    def test_funct(self):
        print(self.filepath_from_value('setting_path'))
'''
    def test_setting_path(self):
        # Testing the FileManagerOption name
        assert self.Simulation_obj.setting_path.name == 'setting_path', \
                "setting_path name in Simulation_obj: " + self.Simulation_obj.setting_path.name

        # Testing the path value
        assert self.Simulation_obj.setting_path.value == self.read_value_from_file('setting_path'), \
                "setting_path value in Simulation_obj: " + self.Simulation_obj.setting_path.value

        # Changing the value
        self.Simulation_obj.setting_path.value = self.filepath2 + '/sample'

        # Testing the changed value
        assert self.Simulation_obj.setting_path.value == self.filepath2 + '/sample', \
                "setting_path changed value in Simulation_obj: " + self.Simulation_obj.setting_path.value

        # Changing the value back
        print("Value before change back: " + self.Simulation_obj.setting_path.value)
        self.Simulation_obj.setting_path.value = self.filepath2
        print("Value after change back: " + self.Simulation_obj.setting_path.value)

        # Testing filepath
        assert self.Simulation_obj.setting_path.filepath == self.filepath2 + '/', \
                "setting_path filepath in Simulation_obj: " + self.Simulation_obj.setting_path.filepath

        # Testing filename
        assert self.Simulation_obj.setting_path.filename == '/', \
                "setting_path filename in Simulation_obj: " + self.Simulation_obj.setting_path.filename

    def test_input_path(self):
        # Testing the FileManagerOption name
        assert self.Simulation_obj.input_path.name == 'input_path', \
            "input_path name in Simulation_obj: " + self.Simulation_obj.input_path.name

        # Testing the path value
        assert self.Simulation_obj.input_path.value == self.read_value_from_file('input_path'), \
            "input_path value in Simulation_obj: " + self.Simulation_obj.input_path.value

        # Changing the value
        self.Simulation_obj.input_path.value = self.filepath2 + '/sample'

        # Testing the changed value
        assert self.Simulation_obj.input_path.value == self.filepath2 + '/sample', \
            "input_path changed value in Simulation_obj: " + self.Simulation_obj.input_path.value

        # Changing the value back
        print("Value before change back: " + self.Simulation_obj.input_path.value)
        print("Filepath before change back: " + self.Simulation_obj.input_path.filepath)
        print("Filename before change back: " + self.Simulation_obj.input_path.filename)

        self.Simulation_obj.input_path.value = self.filepath2
        print("Value after change back: " + self.Simulation_obj.input_path.value)
        print("Filepath after change back: " + self.Simulation_obj.input_path.filepath)
        print("Filename after change back: " + self.Simulation_obj.input_path.filename)

        # Testing filepath
        assert self.Simulation_obj.input_path.filepath == self.filepath2 + '/', \
            "input_path filepath in Simulation_obj: " + self.Simulation_obj.input_path.filepath

        # Testing filename
        assert self.Simulation_obj.input_path.filename == '/', \
            "setting_path filename in Simulation_obj: " + self.Simulation_obj.input_path.filename
    def test_output_path(self):
        return

    def test_decision(self):
        return

    def test_meta_time(self):
        return

    def test_meta_attr(self):
        return

    def test_meta_force(self):
        return

    def test_meta_localpar(self):
        return
'''
