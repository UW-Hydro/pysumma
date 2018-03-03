from unittest import TestCase
from shutil import copyfile
import os
from pysumma.ProposedSimulation import Simulation


class test_simulation(TestCase):
    # Setting up test environment and creating Simulation object
    my_path = os.path.abspath(os.path.dirname(__file__))
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
        self.Simulation_obj.setting_path.value = self.filepath2
        print("Value after change back: " + self.Simulation_obj.setting_path.value)

        # Testing filepath
        assert self.Simulation_obj.setting_path.filepath == self.filepath2 + '/', \
                "setting_path filepath in Simulation_obj: " + self.Simulation_obj.setting_path.filepath

        # Testing filename
        assert self.Simulation_obj.setting_path.filename == '/', \
                "setting_path filename in Simulation_obj: " + self.Simulation_obj.setting_path.filename



        return

    def test_input_path(self):
        return

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

