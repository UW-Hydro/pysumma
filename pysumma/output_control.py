from .option import BaseOption
from .option import OptionContainer

# TODO: FIXME: This metadata needs to be fixed
OUTPUT_META = {}


class OutputControlOption(BaseOption):

    def __init__(self, var=None, period=None, sum=0, instant=1,
                 mean=0, variance=0, min=0, max=0, mode=0):
        self.var = var
        self.period = int(period)
        self.sum = int(sum)
        self.instant = int(instant)
        self.mean = int(mean)
        self.variance = int(variance)
        self.min = int(min)
        self.max = int(max)
        self.mode = int(mode)
        self.validate()

    def set_option(self, key, value):
        try:
            o = self.get_option(key, strict=True)
            o.set_value(value)
        except ValueError:
            if key in OUTPUT_META.keys():
                self.options.append(OutputControlOption(key, value))
            else:
                raise

    def validate(self):
        total = (self.sum + self.instant + self.mean + self.variance
                 + self.min + self.max + self.mode)
        assert total == 1, "Only one output statistic is allowed!"

    def get_print_list(self):
        self.validate()
        plist = [self.var, self.period, self.sum, self.instant, self.mean,
                 self.variance, self.min, self.max, self.mode]
        return [str(p) for p in plist]

    def __repr__(self):
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

    def get_constructor_args(self, line):
        return line.split('!')[0].split('|')
