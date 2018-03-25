from pysumma.ModelOutput import ModelOutput
from shutil import copyfile
import unittest
import os



class TestModelOutput(unittest.TestCase):
    my_path = os.path.abspath(os.path.dirname(__file__)) + '/meta/'
    filename = 'Model_Output.txt'
    filepath = os.path.join(my_path, filename)
    filepath2 = os.path.join(my_path, filename)
    mo = ModelOutput(filepath2)
    print("filepath: " + filepath + '\n')

    def read_vars(self):
        var_list = []
        with open(self.filepath, 'r') as file:
            for line in file:
                if len(line.split("|")) > 1:
                    var_list.append(line.split("|")[0].strip())
        return var_list

    def test_read_variables(self):
        print(str(self.read_vars()))
    # def test_add_valid_variable(self):
    #
    # def test_remove_variable(self):
    #
    # def test_check_for_variables(self):
    #
    # def test_add_invalid_variables(self):
    #
    # def test_add_duplicate_variables(self):
    #
    # def test_get_value_of_variable(self):
    #
    # def test_get_list_of_variable(self):
    #





