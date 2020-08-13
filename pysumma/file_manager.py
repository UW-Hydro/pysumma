import os
import json
import pkg_resources
import xarray as xr

from pathlib import Path
from .option import BaseOption, OptionContainer
from .decisions import Decisions
from .output_control import OutputControl
from .global_params import GlobalParams
from .force_file_list import ForcingList

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
        return "{} '{}'".format(self.name.ljust(36), self.value)


class FileManager(OptionContainer):
    """
    The FileManager object provides an interface to
    a SUMMA file manager file.
    """

    def __init__(self, path, name):
        super().__init__(FileManagerOption, path, name)
        assert self.get_value('controlVersion') == 'SUMMA_FILE_MANAGER_V3.0.0'

    def set_option(self, key, value):
        o = self.get_option(key)
        o.set_value(value)

    def get_constructor_args(self, line):
        name, *value = line.split('!')[0].strip().split()
        if isinstance(value, list):
            value = " ".join(value).replace("'", "")
        return (name.strip(), value.strip().replace("'", "").strip())

    @property
    def decisions(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('decisionsFile')
        self._decisions = Decisions(p1, p2)
        return self._decisions

    @property
    def output_control(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('outputControlFile')
        self._output_control = OutputControl(p1, p2)
        return self._output_control

    @property
    def global_hru_params(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('globalHruParamFile')
        self._hru_params = GlobalParams(p1, p2)
        return self._hru_params

    @property
    def global_gru_params(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('globalGruParamFile')
        self._gru_params = GlobalParams(p1, p2)
        return self._gru_params

    @property
    def force_file_list(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('forcingListFile')
        p3 = self.get_value('forcingPath')
        self._force_file_list = ForcingList(p1, p2, p3)
        return self._force_file_list

    @property
    def local_attributes(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('attributeFile')
        with xr.open_dataset(p1 + p2) as self._local_attrs:
        	self._local_attrs.load()
        return self._local_attrs.load()

    @property
    def trial_params(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('trialParamFile')
        with xr.open_dataset(p1 + p2) as self._trial_params:
        	self._trial_params.load()
        return self._trial_params.load()

    @property
    def initial_conditions(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('initConditionFile')
        with xr.open_dataset(p1 + p2) as self._init_cond:
        	self._init_cond.load()
        return self._init_cond.load()

    @property
    def genparm(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('generalTableFile')
        with open(p1 + p2, 'r') as f:
            self._genparm = f.readlines()
        return self._genparm

    @property
    def mptable(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('noahmpTableFile')
        with open(p1 + p2, 'r') as f:
            self._mptable = f.readlines()
        return self._mptable

    @property
    def soilparm(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('soilTableFile')
        with open(p1 + p2, 'r') as f:
            self._soilparm = f.readlines()
        return self._soilparm

    @property
    def vegparm(self):
        p1 = self.get_value('settingsPath')
        p2 = self.get_value('vegTableFile')
        with open(p1 + p2, 'r') as f:
            self._vegparm = f.readlines()
        return self._vegparm
