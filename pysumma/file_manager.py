import json
import pkg_resources
import xarray as xr

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

    def __repr__(self):
        return "'{}'    ! {}".format(self.value, self.name)


class FileManager(OptionContainer):
    """
    The FileManager object provides an interface to
    a SUMMA file manager file.
    """

    def __init__(self, path):
        super().__init__(path, FileManagerOption)

    def set_option(self, key, value):
        o = self.get_option(key)
        o.set_value(value)

    def get_constructor_args(self, line):
        return (OPTION_NAMES[self.opt_count],
                line.split('!')[0].replace("'", "").strip())

    @property
    def decisions(self):
        p = self.get_value('settings_path') + self.get_value('decisions_path')
        return Decisions(p)

    @property
    def output_control(self):
        p = self.get_value('settings_path') + self.get_value('output_control')
        return OutputControl(p)

    @property
    def local_param_info(self):
        p = (self.get_value('settings_path')
             + self.get_value('local_param_info'))
        return LocalParamInfo(p)

    @property
    def basin_param_info(self):
        p = (self.get_value('settings_path')
             + self.get_value('basin_param_info'))
        return LocalParamInfo(p)

    @property
    def force_file_list(self):
        p1 = (self.get_value('settings_path')
              + self.get_value('forcing_file_list'))
        p2 = self.get_value('input_path')
        return ForceFileList(p1, p2)

    @property
    def local_attributes(self):
        p = (self.get_value('settings_path')
             + self.get_value('local_attributes'))
        return xr.open_dataset(p)

    @property
    def parameter_trial(self):
        p = (self.get_value('settings_path')
             + self.get_value('parameter_trial'))
        return xr.open_dataset(p)
