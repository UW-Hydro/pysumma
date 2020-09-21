import pytest

import os, json, pkg_resources
import unittest
from pathlib import Path
from shutil import copyfile
from pysumma.decisions import Decisions, DecisionOption

my_path = Path(os.path.dirname(__file__)) / 'data'
filename = 'decisions.txt'
filepath = os.path.join(my_path, filename)
tmp_filename = 'tmp_{}'.format(filename)
tmp_filepath = os.path.join(my_path, tmp_filename)
copyfile(filepath, tmp_filepath)
test_decisions = Decisions(my_path, tmp_filepath)


@pytest.mark.parametrize('name, option1, option2, option3',
                         [("soilCatTbl", "STAS", "STAS-RUC", "ROSETTA")])
def test_GetSoilCategoryDataset(name, option1, option2, option3):
    soil_cat_dataset = DecisionOption(name, option1)
    assert name == soil_cat_dataset.name
    assert [option1, option2, option3] == soil_cat_dataset.available_options


@pytest.mark.parametrize('name, option1, option2, option3',
                         [("soilCatTbl", "STAS", "STAS-RUC", "ROSETTA")])
def test_SetSoilCategoryDataset(name, option1, option2, option3):
    soil_cat_dataset = DecisionOption(name, option1)
    new_value = option3
    soil_cat_dataset.value = new_value
    test_decisions.write()
    d_new_value = test_decisions[name].value
    assert new_value == d_new_value
