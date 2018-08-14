

class OutputControl(object):
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
        self.original_path = path
        self.header = []
        self.options = []
        self.read(path)

    def read(self, path):
        """Read the output control file and load data"""
        with open(path, 'r') as f:
            self.original_contents = f.readlines()
        opt_count = 0
        for linum, line in enumerate(self.original_contents):
            if line.startswith('!') and not opt_count:
                self.header.append(line)
            elif not line.startswith('!'):
                opt_count += 1
                self.options.append(OutputControlOption(
                    *[l.strip() for l in line.split('|')]))

    def write(self, path=None):
        """Write the configured output control file"""
        self.validate()
        if not path:
            path = self.original_path
        with open(path, 'w') as f:
            f.writelines(self.header)
            f.writelines((o.__repr__() + '\n' for o in self.options))

    def set_option(self, var=None, period=None, sum=0, instant=1,
                   mean=0, variance=0, min=0, max=0, mode=0):
        """
        Change or create a new entry in the output control
        """
        try:
            o = self.get_option(var, strict=True)
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
                    OutputControlOption(var, period, sum, instant,
                                        mean, variance, min, max, mode))

    def get_option(self, name, strict=False):
        """Look for an existing option"""
        for o in self.options:
            if name == o.var:
                return o
        if strict:
            raise ValueError("Could not find option {}!".format(name))
        return None

    def validate(self):
        """Make sure no duplicate options exist"""
        names = [o.var for o in self.options]
        assert len(names) == len(set(names)), 'Duplicate options not allowed!'


class OutputControlOption(object):

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
