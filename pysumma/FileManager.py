from .Option import BaseOption, OptionContainer

# Option names for the file manager, this is just a list,
# as the order of these values matters. They may also not be
# explicitely writtn out in the given file.
OPTION_NAMES = ['FILEMANAGER_VERSION', 'SETTINGS_PATH', 'INPUT_PATH',
                'OUTPUT_PATH', 'DECISIONS_PATH', 'META_TIME', 'META_ATTR',
                'META_TYPE', 'META_FORCE', 'META_LOCALPARAM',
                'OUTPUT_CONTROL', 'META_LOCALINDEX', 'META_BASINPARAM',
                'META_BASINMVAR', 'LOCAL_ATTRIBUTES', 'LOCAL_PARAM_INFO',
                'BASIN_PARAM_INFO', 'FORCING_FILE_LIST', 'MODEL_INIT_COND',
                'PARAMETER_TRIAL', 'OUTPUT_PREFIX']


class FileManagerOption(BaseOption):
    """Container for lines in a file manager file"""

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return "'{}'    ! {}".format(self.value, self.name)


class FileManager(OptionContainer):
    """
    The FileManager object provides an interface to
    a SUMMA file manager file.
    """

    def __init__(self, path):
        super().__init__(path, FileManagerOption)

    def get_constructor_args(self, line):
        return (OPTION_NAMES[self.opt_count],
                line.split('!')[0].replace("'", "").strip())
