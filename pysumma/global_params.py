from decimal import Decimal

from .option import BaseOption
from .option import OptionContainer


class GlobalParamOption(BaseOption):

    def __init__(self, name, default, low, high):
        super().__init__(name)
        self.set_value([default, low, high])

    def set_value(self, new_value):
        assert len(new_value) == 3
        self.value = new_value

    def __str__(self):
        def _to_string(val):
            too_small = val < 0.0001 and val != 0
            too_big = val > 9999.99
            if too_big or too_small:
                return ('{:.1E}'.format(Decimal(val))
                                .replace('e', 'd')
                                .replace('E', 'd'))
            else:
                return '{:>12.4f}'.format(val)
        return ("{:25s} | {:>12s} | {:>12s} | {:>12s}".format(
            self.name, *map(_to_string, self.value)))


class GlobalParams(OptionContainer):

    fmt_strings = ["'(a25,1x,3(a1,1x,f12.4,1x))'",
                   "'(a25,1x,a1,1x,3(f12.4,1x,a1,1x))'"]

    def __init__(self, dirpath, filepath=None):
        super().__init__(GlobalParamOption, dirpath, filepath)

    def set_option(self, key, value):
        if not isinstance(value, list):
            value = [value] * 3
        try:
            o = self.get_option(key)
            o.set_value(value)
        except AttributeError as e:
            self.options.append(GlobalParamOption(key, *value))

    def read(self, path):
        """Read the configuration and populate the options"""
        with open(path, 'r') as f:
            self.original_contents = f.readlines()
        for line in self.original_contents:
            isnt_empty = len(''.join(map(lambda x: x.strip(), line.split() )))
            if ((line.startswith('!') and not self.opt_count and not isnt_empty)
                    or line.split('!')[0].strip() in self.fmt_strings):
                self.header.append(line)
            elif not line.startswith('!') and isnt_empty:
                self.options.append(self.OptionType(
                    *self.get_constructor_args(line)))
                self.opt_count += 1

    def get_constructor_args(self, line):
        param, *value = line.split('|')
        default, low, high = map(lambda x: float(x.strip().replace('d', 'e')),
                                 value)
        return param.strip(), default, low, high
