import copy
from .option import BaseOption
from .option import OptionContainer


class LocalParamOption(BaseOption):

    def __init__(self, name, default, low, high):
        super().__init__(name)
        self.set_value([default, low, high])

    def set_value(self, new_value):
        self.value = new_value

    def __repr__(self):
        return ("{:25s} | {:>12.4f} | {:>12.4f} | {:>12.4f}".format(
            self.name, self.value[0], self.value[1], self.value[2]))


class LocalParamInfo(OptionContainer):

    def __init__(self, path):
        super().__init__(path, LocalParamOption)

    def set_option(self, key, value):
        o = self.get_option(key)
        o.set_value(value)

    def read(self, path):
        """Read the configuration and populate the options"""
        fmt_string = "'(a25,1x,3(a1,1x,f12.4,1x))'"
        with open(path, 'r') as f:
            self.original_contents = f.readlines()
        for line in self.original_contents:
            if line.startswith('!') and not self.opt_count:
                self.header.append(line)
            elif (not line.startswith('!') and
                    not line.split('!')[0].startswith(fmt_string)):
                self.options.append(self.OptionType(
                    *self.get_constructor_args(line)))
                self.opt_count += 1

    def get_constructor_args(self, line):
        param, *value = line.split('|')
        default, low, high = map(lambda x: float(x.strip().replace('d', 'e')),
                                 value)
        return param.strip(), default, low, high
