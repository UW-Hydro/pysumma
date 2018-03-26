from pysumma.ModelOutput import ModelOutput
import unittest
import random
from shutil import copyfile
import os


class TestModelOutput(unittest.TestCase):
    my_path = os.path.abspath(os.path.dirname(__file__)) + '/meta/'
    filename = 'Model_Output.txt'
    filepath = os.path.join(my_path, filename)
    filename2 = 'tmp_{}'.format(filename)
    filepath2 = os.path.join(my_path, filename2)
    copyfile(filepath, filepath2)
    mo = ModelOutput(filepath2)

    def read_vars(self):
        var_list = []
        with open(self.filepath2, 'r') as file:
            for line in file:
                if len(line.split("|")) > 1:
                    var_list.append(line.split("|")[0].strip())
        return var_list

    # Does ModelOutput read all the variables from the file?
    def test_1_read_variables(self):
        assert self.mo.read_variables_from_file() == self.read_vars()

    # Go through all possible variables-does ModelOutput correctly determine their status?
    def test_2_check_for_variables(self):
        vars_in_file = self.read_vars()
        for var in self.mo.var_choices:
            if var in vars_in_file:
                assert self.mo.check_for_variable(var) is True, "var: " + var + " should be in the file."
            else:
                assert self.mo.check_for_variable(var) is False, "var: " + var + " should not be in the file"

    # TODO: make the tests independent (add/delete in one method)
    # Upon adding every possible variable, does ModelOutput reflect the changes?
    def test_3_add_all_valid_variables(self):
        for i in range(0, len(self.mo.var_choices)):
            self.mo.add_variable(self.mo.var_choices[i])
            assert self.mo.var_choices[i] in self.read_vars()

     # Upon removing every variable in the
    def test_4_remove_all_valid_variables(self):
        for i in range(0, len(self.mo.var_choices)):
            self.mo.remove_variable(self.mo.var_choices[i])
            assert self.mo.read_variables_from_file() == self.read_vars()
            assert self.mo.var_choices[i] not in self.read_vars()

    # Testing a 'normal' situation-when someone adds just one variable to a file, checks it, then deletes it
    def test_5_pptrate(self):
        self.mo.add_variable('pptrate')
        assert self.mo.check_for_variable('pptrate') is True
        self.mo.add_variable('penguin')
        assert self.mo.read_variables_from_file() == ['pptrate']
        self.mo.remove_variable('nSoil')
        assert self.mo.read_variables_from_file() == ['pptrate']
        self.mo.remove_variable('pptrate')
        assert self.mo.read_variables_from_file() == []
        self.assertEqual("a", "a")
    # def test_add_invalid_variables(self):
    #
    # def test_add_duplicate_variables(self):
    #
    # def test_get_value_of_variable(self):
    #
    # def test_get_list_of_variable(self):
    #





