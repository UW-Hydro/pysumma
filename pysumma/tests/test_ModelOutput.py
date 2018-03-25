from pysumma.ModelOutput import ModelOutput
import unittest
import random
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

    # Does ModelOutput read all the variables from the file?
    def test_read_variables(self):
        assert self.mo.read_variables_from_file() == self.read_vars()

    # Does ModelOutput accurately check for the variable?
    def test_check_for_variables(self):
        for var in self.read_vars():
            pass
        # TODO: check for every variable in the file, then check for variables not in the file (all others in mo.var_list

    # Upon adding every possible variable, does ModelOutput reflect the changes?
    # def test_add_all_valid_variables(self):
    #     for i in range(0, len(self.mo.var_choices)):
    #         self.mo.write_variable_to_file(self.mo.var_choices[i])
    #         assert self.mo.var_choices[i] in self.read_vars()

    # Upon removing
    # def test_remove_all_valid_variables(self):
    #     for i in range(0, len(self.mo.var_choices)):
    #         self.mo.remove_variable(self.mo.var_choices[i])
    #         assert self.mo.var_choices[i] not in self.read_vars()

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





