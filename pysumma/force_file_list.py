import os
import xarray as xr

from .option import BaseOption
from .option import OptionContainer


class ForcingOption(BaseOption):

    def __init__(self, name):
        super().__init__(name)
        self.set_value(name)

    def set_value(self, new_value):
        self.value = new_value

    @property
    def path(self):
        return self.name.replace("'", "")

    @path.setter
    def path(self, value):
        self.set_value(value)

    def __str__(self):
        return "'{}'".format(self.name.split('/')[-1])


class ForcingList(OptionContainer):

    prefix: str = ''

    def __init__(self, dirpath, filepath=None, force_file_prefix_path=None):
        if not filepath:
            filepath = dirpath.split('/')[-1]
            dirpath = os.path.sep.join(dirpath.split('/')[0:-1])
        if not force_file_prefix_path:
            force_file_prefix_path = dirpath
        self.prefix = str(force_file_prefix_path)
        super().__init__(ForcingOption, dirpath, filepath)

    def set_option(self, key, value):
        o = self.get_option(key)
        o.set_value(value)

    def get_constructor_args(self, line):
        file_name = line.replace("'", "")
        return (os.path.join(self.prefix, file_name.strip()), )

    @property
    def forcing_paths(self):
        return [o.path for o in self.options]

    @property
    def forcing_data(self):
        return [o.value for o in self.options]

    def open_forcing_data(self):
        return [xr.open_dataset(o) for o in self.forcing_data]
