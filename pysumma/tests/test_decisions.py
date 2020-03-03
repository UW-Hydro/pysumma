import pytest

import os, json, pkg_resources
import unittest
from shutil import copyfile
import pysumma.decisions as decisions

my_path = os.getcwd()
filename = 'decisions.txt'
filepath = os.path.join(my_path, filename)
tmp_filename = 'tmp_{}'.format(filename)
tmp_filepath = os.path.join(my_path, tmp_filename)
copyfile(filepath, tmp_filepath)
test_decisions = decisions.Decisions(my_path, tmp_filepath)

@pytest.mark.parametrize('name, option1, option2, option3',[("soilCatTbl", "STAS", "STAS-RUC", "ROSETTA")])
def test_GetSoilCategoryDataset(name, option1, option2, option3):
        soil_cat_dataset = decisions.DecisionOption(name, option1)
        assert name == soil_cat_dataset.name
        assert [option1, option2, option3] == soil_cat_dataset.available_options

@pytest.mark.parametrize('name, option1, option2, option3',[("soilCatTbl", "STAS", "STAS-RUC", "ROSETTA")])
def test_SetSoilCategoryDataset(name, option1, option2, option3):
        soil_cat_dataset = decisions.DecisionOption(name, option1)
        new_value = option3
        soil_cat_dataset.value = new_value
        test_decisions.write()
        d_new_value = test_decisions[name].value
        assert new_value == d_new_value

@pytest.mark.parametrize('name, value, description',[("simulStart", "2010-10-01 00:00", ['YYYY-MM-DD hh:mm'])])
def test_GetSimulStartDataset(name, value, description):
        sim_start_dataset = decisions.DecisionOption(name, value)
        assert name == sim_start_dataset.name
        assert description == sim_start_dataset.available_options

@pytest.mark.parametrize('name, value, new_date',[("simulStart", "2010-10-01 00:00", "2010-10-01 00:00")])
def test_SetSimulStartDataset(name, value, new_date):
        sim_start_dataset = decisions.DecisionOption(name, value)
        new_value = new_date
        sim_start_dataset.value = new_value
        test_decisions.write()
        d_new_value = test_decisions[name].value
        assert new_value == d_new_value