import os
import json
import pkg_resources
import xarray as xr

from pathlib import Path
from .option import BaseOption, OptionContainer
from .decisions import Decisions
from .output_control import OutputControl
from .local_param_info import LocalParamInfo
from .force_file_list import ForceFileList

# Option names for the file manager, this is just a list,
# as the order of these values matters. They may also not be
# explicitely writtn out in the given file.
METADATA_PATH = pkg_resources.resource_filename(
        __name__, 'meta/file_manager.json')
with open(METADATA_PATH, 'r') as f:
    FILEMANAGER_META = json.load(f)
OPTION_NAMES = FILEMANAGER_META['option_names']


class FileManagerOption(BaseOption):
    """Container for lines in a file manager file"""

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def set_value(self, new_value):
        self.value = new_value

    def __str__(self):
        return "{} '{}'".format(self.value, self.name)


class FileManager(OptionContainer):
    """
    The FileManager object provides an interface to
    a SUMMA file manager file.
    """

    def __init__(self, path, name):
        super().__init__(FileManagerOption, path, name)

    def set_option(self, key, value):
        o = self.get_option(key)
        o.set_value(value)

    def get_constructor_args(self, line):
        name, value = line.split('!')[0].strip().split('')
        return (name.strip(), value.strip(). replace("'", "").strip())

    @property
    def decisions(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('decisionsFile')
        self._decisions = Decisions(p1, p2)
        return self._decisions

    @property
    def output_control(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('outputDefFile')
        self._output_control = OutputControl(p1, p2)
        return self._output_control

    @property
    def local_param_info(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('hruParamFile')
        self._local_param_info = LocalParamInfo(p1, p2)
        return self._local_param_info

    @property
    def basin_param_info(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('gruParamFile')
        self._basin_param_info = LocalParamInfo(p1, p2)
        return self._basin_param_info

    @property
    def force_file_list(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('forcingList')
        p3 = self.get_value('forcingPath')
        self._force_file_list = ForceFileList(p1, p2, p3)
        return self._force_file_list

    @property
    def local_attributes(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('attributeFile')
        self._local_attrs = xr.open_dataset(p1 + p2)
        return self._local_attrs

    @property
    def parameter_trial(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('trialParamFile')
        self._param_trial = xr.open_dataset(p1 + p2)
        return self._param_trial

    @property
    def initial_conditions(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('initCondFile')
        self._init_cond = xr.open_dataset(p1 + p2)
        return self._init_cond

    @property
    def genparm(self):
        p1, p2 = self.get_value('settingsPath'), 'GENPARM.TBL'
        with open(p1 + p2, 'r') as f:
            self._genparm = f.readlines()
        return self._genparm

    @property
    def mptable(self):
        p1, p2 = self.get_value('settingsPath'), 'MPTABLE.TBL'
        with open(p1 + p2, 'r') as f:
            self._mptable = f.readlines()
        return self._mptable

    @property
    def soilparm(self):
        p1, p2 = self.get_value('settingsPath'), 'SOILPARM.TBL'
        with open(p1 + p2, 'r') as f:
            self._soilparm = f.readlines()
        return self._soilparm

    @property
    def vegparm(self):
        p1, p2 = self.get_value('settingsPath'), 'VEGPARM.TBL'
        with open(p1 + p2, 'r') as f:
            self._vegparm = f.readlines()
        return self._vegparm
