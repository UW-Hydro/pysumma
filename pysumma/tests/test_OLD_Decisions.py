from pysumma.Decisions import Decisions # This is for testing in cmd window.
#from ..pysumma.Decisions import Decisions # This is for testing in this python code.
import unittest
import os.path
from shutil import copyfile

class test_decisions_class(unittest.TestCase):

    my_path = os.path.abspath(os.path.dirname(__file__))
    filename = 'Decision.txt'
    filepath = os.path.join(my_path, filename)
    filename2 = 'tmp_{}'.format(filename)
    filepath2 = os.path.join(my_path, filename2)
    copyfile(filepath, filepath2)
    Decisions_obj = Decisions(filepath2)


    def get_value(self, name):
        file_obj = open(self.filepath2, 'r')
        lines = file_obj.readlines()
        file_obj.close()
        for line in lines:
            if line.startswith(name):
                return line.split()[1]

    def test_GetSoilCategoryDataset(self):
        soil_cat_dataset = self.Decisions_obj.soilCatTbl
        self.assertEqual('soilCatTbl', soil_cat_dataset.name)
        self.assertEqual(self.get_value(soil_cat_dataset.name), soil_cat_dataset.value)
        self.assertEqual(['STAS', 'STAS-RUC', 'ROSETTA'], soil_cat_dataset.options)
        self.assertEqual('soil-category dateset', soil_cat_dataset.description)

    def test_SetSoilCategoryDataset(self):
        soil_cat_dataset = self.Decisions_obj.soilCatTbl
        old = soil_cat_dataset.value
        self.assertEqual(old, self.get_value(soil_cat_dataset.name))
        soil_cat_dataset.value = 'ROSETTA'
        new = soil_cat_dataset.value
        self.assertEqual(new, 'ROSETTA')

    def test_GetGroundwaterParameterization(self):
        ground_para = self.Decisions_obj.groundwatr
        self.assertEqual('groundwatr', ground_para.name)
        self.assertEqual(self.get_value(ground_para.name), ground_para.value)
        self.assertEqual(['qTopmodl', 'bigBuckt', 'noXplict'], ground_para.options)
        self.assertEqual('choice of groundwater parameterization', ground_para.description)

    def test_SetGroundwaterParameterization(self):
        ground_para = self.Decisions_obj.groundwatr
        old = ground_para.value
        self.assertEqual(old, self.get_value(ground_para.name))
        ground_para.value = 'qTopmodl'
        new = ground_para.value
        self.assertEqual(new, 'qTopmodl')

    def test_GetLowerBoundaryThermo(self):
        lowbond_therm = self.Decisions_obj.bcLowrTdyn
        self.assertEqual('bcLowrTdyn', lowbond_therm.name)
        self.assertEqual(self.get_value(lowbond_therm.name), lowbond_therm.value)
        self.assertEqual(['presTemp', 'zeroFlux'], lowbond_therm.options)
        self.assertEqual('type of lower boundary condition for thermodynamics', lowbond_therm.description)

    def test_SetLowerBoundaryThermo(self):
        lowbond_therm = self.Decisions_obj.bcLowrTdyn
        old = lowbond_therm.value
        self.assertEqual(old, self.get_value(lowbond_therm.name))
        lowbond_therm.value = 'presTemp'
        new = lowbond_therm.value
        self.assertEqual(new, self.get_value(lowbond_therm.name))

    def test_validate_value(self):
        validate_value2 = 'STAS1'
        with self.assertRaises(ValueError):
            self.Decisions_obj.soilCatTbl.value = validate_value2

if __name__ == '__main__':
    unittest.main()