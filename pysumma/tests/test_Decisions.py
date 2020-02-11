import os.path
import unittest
from shutil import copyfile
from pysumma.Decisions import Decisions


class test_decisions_class(unittest.TestCase):
    my_path = os.getcwd()
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
        new_val = "ROSETTA"
        soil_cat_dataset.value = new_val
        new = self.get_value(soil_cat_dataset.name)
        self.assertEqual(new, new_val)

        new_val = "STAS"
        soil_cat_dataset.value = new_val
        self.assertEqual(soil_cat_dataset.value, new_val)
        new = self.get_value(soil_cat_dataset.name)
        self.assertEqual(new, new_val)

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
        new_val = 'qTopmodl'
        ground_para.value = new_val
        new = self.get_value(ground_para.name)
        self.assertEqual(new, new_val)

        new_val = 'bigBuckt'
        ground_para.value = new_val
        new = self.get_value(ground_para.name)
        self.assertEqual(new, new_val)

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
        new_val = 'presTemp'
        lowbond_therm.value = new_val
        new = self.get_value(lowbond_therm.name)
        self.assertEqual(new, new_val)

        new_val = 'zeroFlux'
        lowbond_therm.value = new_val
        new = self.get_value(lowbond_therm.name)
        self.assertEqual(new, new_val)

    def test_multiple_setting(self):

        soil_cat_dataset = self.Decisions_obj.soilCatTbl
        new_soil_cat_val = 'STAS'
        soil_cat_dataset.value = new_soil_cat_val
        self.assertEqual(new_soil_cat_val, soil_cat_dataset.value)
        new_soil_cat = self.get_value(soil_cat_dataset.name)
        self.assertEqual(new_soil_cat, new_soil_cat_val)

        new_soil_cat_val = 'ROSETTA'
        soil_cat_dataset.value = new_soil_cat_val
        new_soil_cat = self.get_value(soil_cat_dataset.name)
        self.assertEqual(new_soil_cat, new_soil_cat_val)

        thConSnow = self.Decisions_obj.thCondSnow
        old_thr_snow = thConSnow.value
        self.assertEqual("jrdn1991", old_thr_snow)
        new_thr_snow_val = "tyen1965"
        thConSnow.value = new_thr_snow_val
        new_thr_snow = self.get_value(thConSnow.name)
        self.assertEqual(new_thr_snow, new_thr_snow_val)

        new_soil_cat = self.get_value(soil_cat_dataset.name)
        self.assertEqual(new_soil_cat, new_soil_cat_val)

    def test_SetSoilCategoryDatasetMultiple(self):
        soil_cat_dataset = self.Decisions_obj.soilCatTbl
        old = soil_cat_dataset.value
        self.assertEqual(old, self.get_value(soil_cat_dataset.name))
        new = 'ROSETTA'
        soil_cat_dataset.value = new
        self.assertEqual(self.get_value(soil_cat_dataset.name), new)
        new = 'STAS'
        soil_cat_dataset.value = new
        self.assertEqual(self.get_value(soil_cat_dataset.name), new)


if __name__ == '__main__':
    unittest.main()
