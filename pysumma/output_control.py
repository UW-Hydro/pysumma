import pkg_resources
from .option import BaseOption
from .option import OptionContainer


def read_master_file(master_file_filepath):
    """Get all varialbes from var_lookup file"""
    #TODO: This may be fragile, move this to utils and create a static
    #      version of this metadata. Then, we can use this function to
    #      repopulate a new version of the metadata as necessary
    out = []
    with open(master_file_filepath, 'r') as file:
        for line in file:
            if "::" in line and line.split('::')[1].split('=')[0] is not None:
                out.append(line.split('::')[1].split('=')[0].strip())

    return {'variables': out}


METADATA_PATH = pkg_resources.resource_filename(
        __name__, 'meta/var_lookup.f90')
OUTPUT_META = read_master_file(METADATA_PATH)


class OutputControlOption(BaseOption):

    def __init__(self, var=None, period=None, sum=0, instant=1,
                 mean=0, variance=0, min=0, max=0, mode=0):
        self.name = var
        self.period = int(period)
        self.sum = int(sum)
        self.instant = int(instant)
        self.mean = int(mean)
        self.variance = int(variance)
        self.min = int(min)
        self.max = int(max)
        self.mode = int(mode)
        self.validate()

    @property
    def statistic(self):
        """This could be improved"""
        if self.sum:
            return 'sum'
        elif self.instant:
            return 'instant'
        elif self.mean:
            return 'mean'
        elif self.variance:
            return 'variance'
        elif self.min:
            return 'min'
        elif self.max:
            return 'max'
        elif self.mode:
            return 'mode'

    def validate(self):
        total = (self.sum + self.instant + self.mean + self.variance
                 + self.min + self.max + self.mode)
        assert total == 1, "Only one output statistic is allowed!"

    def get_print_list(self):
        self.validate()
        plist = [self.name, self.period, self.sum, self.instant, self.mean,
                 self.variance, self.min, self.max, self.mode]
        return [str(p) for p in plist]

    def __str__(self):
        return " | ".join(self.get_print_list())


class OutputControl(OptionContainer):
    """
    The OutputControl object manages what output SUMMA will
    write out.  Each output variable is stored in the `options`
    list as an `OutputControlOption`.  These options are
    automatically populated on instantiation, and can be
    added or modified through the `set_option` method.
    """

    def __init__(self, path):
        """
        Instantiate the object and populate the
        values from the given filepath.
        """
        super().__init__(path, OutputControlOption)

    def set_option(self, name=None, period=None, sum=0, instant=1,
                   mean=0, variance=0, min=0, max=0, mode=0):
        """
        Change or create a new entry in the output control
        """
        try:
            o = self.get_option(name, strict=True)
            o.period = period
            o.sum = sum
            o.instant = instant
            o.mean = mean
            o.variance = variance
            o.min = min
            o.max = max
            o.mode = mode
        except ValueError:
            self.options.append(
                    OutputControlOption(name, period, sum, instant,
                                        mean, variance, min, max, mode))
            if name in OUTPUT_META['variables']:
                self.options.append(OutputControlOption(
                        name, period, sum, instant, mean,
                        variance, min, max, mode))
            else:
                raise

    def get_constructor_args(self, line):
        return line.split('!')[0].split('|')
