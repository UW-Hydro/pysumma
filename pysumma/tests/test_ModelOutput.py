from pysumma.ModelOutput import ModelOutput
import unittest
import random
from shutil import copyfile
from random import randint
import os


class TestModelOutput(unittest.TestCase):
    my_path = os.path.abspath(os.path.dirname(__file__)) + '/meta/'
    filename = 'Model_Output.txt'
    filepath = os.path.join(my_path, filename)
    filename2 = 'tmp_{}'.format(filename)
    filepath2 = os.path.join(my_path, filename2)
    copyfile(filepath, filepath2)
    mo = ModelOutput(filepath2, 'pysumma/var_lookup.f90')

    def read_vars(self):
        var_list = []
        with open(self.filepath2, 'r') as file:
            for line in file:
                if len(line.split("|")) > 1:
                    var_list.append(line.split("|")[0].strip())
        return var_list

    # Does ModelOutput read all the variables from the file?
    def test_read_variables(self):
        self.assertEqual(self.mo.read_variables_from_file(), self.read_vars())

    def test_add_remove_mLayerdPsi_dTheta(self):
        self.mo.add_variable('mLayerdPsi_dTheta')
        list_with_mLayerdPsi_dTheta = self.mo.read_variables_from_file()
        self.assertEqual(list_with_mLayerdPsi_dTheta, self.read_vars())
        self.mo.remove_variable('mLayerdPsi_dTheta')
        self.assertNotEqual(list_with_mLayerdPsi_dTheta, self.read_vars())
        self.mo.add_variable('mLayerdPsi_dTheta')

    def test_add_invalid_variable(self):
        with self.assertRaises(Exception):
            self.mo.add_variable('pptrate')

    def test_add_duplicate_variable(self):
        with self.assertRaises(Exception):
            self.mo.add_variable('pptrate')

    def test_add_multiple_variables(self):
        vars = []
        for i in range(0, 50):
            vars.append(self.mo.var_choices[randint(0, len(self.mo.var_choices) - 1)])
            if vars[i] not in self.mo.read_variables_from_file():
                self.mo.add_variable(vars[i])

        # Test to make sure the variables are all added
        for var in vars:
            self.assertIn(var, self.mo.read_variables_from_file())
            self.assertIn(var, self.read_vars())

        self.mo.clear_variables()

    def test_remove_all_variables_individually(self):
        vars = []
        for i in range(0, 15):
            vars.append(self.mo.var_choices[randint(0, len(self.mo.var_choices) - 1)])
            if vars[i] not in self.mo.read_variables_from_file():
                self.mo.add_variable(vars[i])

        for variable in self.mo.read_variables_from_file():
            self.mo.remove_variable(variable)
        self.assertEqual(self.mo.read_variables_from_file(), [])

    def test_clear_variables(self):
        vars = []
        for i in range(0, 15):
            vars.append(self.mo.var_choices[randint(0, len(self.mo.var_choices) - 1)])
            if vars[i] not in self.mo.read_variables_from_file():
                self.mo.add_variable(vars[i])

        self.mo.clear_variables()
        self.assertEqual([], self.mo.read_variables_from_file())

    # TODO: make the tests independent (add/delete in one method)




