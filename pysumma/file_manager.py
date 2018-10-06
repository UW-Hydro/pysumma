import json
import pkg_resources

from .option import BaseOption, OptionContainer

# Option names for the file manager, this is just a list,
# as the order of these values matters. They may also not be
# explicitely writtn out in the given file.
METADATA_PATH = pkg_resources.resource_filename(
        __name__, 'meta/file_manager.json')
with open(METADATA_PATH, 'r') as f:
    FILEMANAGER_META = json.load(f)
OPTION_NAMES = FILEMANAGER_META['OPTION_NAMES']


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
