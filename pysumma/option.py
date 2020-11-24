import os
from numbers import Number
from pathlib import Path

class BaseOption(object):
    """
    Base implementation for representing options in the various
    text based SUMMA configuration files. This class is meant to
    be extended rather than used directly.
    """

    compare_err = 'Cannot compare LocalParamOption to {}'

    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def __str__(self):
        return "{} : {}".format(self.name, self.value)

    def __eq__(self, other):
        if isinstance(other, Number) or isinstance(other, str):
            return self.value[0] == other
        elif isinstance(other, type(self)):
            return self.value[0] == other.value[0]
        else:
            raise TypeError(BaseOption.compare_err.format(type(other)))

    def __lt__(self, other):
        if isinstance(other, Number):
            return self.value[0] < other
        elif isinstance(other, type(self)):
            return self.value[0] < other.value[0]
        else:
            raise TypeError(BaseOption.compare_err.format(type(other)))

    def __le__(self, other):
        if isinstance(other, Number):
            return self.value[0] <= other
        elif isinstance(other, type(self)):
            return self.value[0] <= other.value[0]
        else:
            raise TypeError(BaseOption.compare_err.format(type(other)))

    def __gt__(self, other):
        if isinstance(other, Number):
            return self.value[0] > other
        elif isinstance(other, type(self)):
            return self.value[0] > other.value[0]
        else:
            raise TypeError(BaseOption.compare_err.format(type(other)))

    def __ge__(self, other):
        if isinstance(other, Number):
            return self.value[0] >= other
        elif isinstance(other, type(self)):
            return self.value[0] >= other.value[0]
        else:
            raise TypeError(BaseOption.compare_err.format(type(other)))

    def __ne__(self, other):
        if isinstance(other, Number) or isinstance(other, str):
            return self.value[0] != other
        elif isinstance(other, type(self)):
            return self.value[0] != other.value[0]
        else:
            raise TypeError(BaseOption.compare_err.format(type(other)))

    def __add__(self, other):
        if isinstance(other, Number):
            return self.value[0] + other
        elif isinstance(other, type(self)):
            return self.value[0] + other.value[0]
        else:
            raise TypeError(BaseOption.compare_err.format(type(other)))

    def __sub__(self, other):
        if isinstance(other, Number):
            return self.value[0] - other
        elif isinstance(other, type(self)):
            return self.value[0] - other.value[0]
        else:
            raise TypeError(BaseOption.compare_err.format(type(other)))

    def __mul__(self, other):
        if isinstance(other, Number):
            return self.value[0] * other
        elif isinstance(other, type(self)):
            return self.value[0] * other.value[0]
        else:
            raise TypeError(BaseOption.compare_err.format(type(other)))

    def __truediv__(self, other):
        if isinstance(other, Number):
            return self.value[0] / other
        elif isinstance(other, type(self)):
            return self.value[0] / other.value[0]
        else:
            raise TypeError(BaseOption.compare_err.format(type(other)))



class OptionContainer(object):
    """
    Base implementation for representing text based configuration
    files for SUMMA. This class is meant to be extended rather than
    used directly.
    """

    def __init__(self, optiontype, dir='.', name=None):
        """
        Instantiate the object and populate the
        values from the given filepath.
        """
        if not name:
            name = dir.split('/')[-1]
            dir = os.path.sep.join(dir.split('/')[0:-1])
        self.OptionType = optiontype
        self.opt_count = 0
        self.original_path = Path(dir)
        self.file_name = Path(name)
        self.header = []
        self.options = []
        self.read(os.path.abspath(self.original_path / self.file_name))

    def set_option(self):
        """This has to be implemented by subclasses"""
        raise NotImplementedError()

    def get_constructor_args(self, line):
        """
        This has to be implemented by subclasses

        The purpose of this method is to be able to easily pass
        arguments to the constructors of subclasses of BaseOption.
        The implementation will depend on what is considered an
        option.
        """
        raise NotImplementedError()

    def __str__(self):
        return os.linesep.join([str(o) for o in self.options])

    def read(self, path):
        """Read the configuration and populate the options"""
        with open(path, 'r') as f:
            self.original_contents = f.readlines()
        for line in self.original_contents:
            isnt_empty = len(''.join(map(lambda x: x.strip(), line.split() )))
            if line.startswith('!') and not self.opt_count and not isnt_empty:
                self.header.append(line)
            elif not line.startswith('!') and isnt_empty:
                self.options.append(self.OptionType(
                    *self.get_constructor_args(line)))
                self.opt_count += 1

    def write(self, path=None):
        """Write the configuration given the values of the options"""
        self.validate()
        if not path:
            path = self.original_path
        filepath = Path(os.path.abspath(Path(path / self.file_name)))
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            f.writelines(self.header)
            f.writelines((str(o) + '\n' for o in self.options))

    def get_option(self, name, strict=False):
        """Retrieve an option"""
        for o in self.options:
            if name == o.name:
                return o
        if strict:
            raise ValueError("Could not find option {}!".format(name))
        return None

    def get_value(self, name, strict=False):
        """Retrieve the value of a given option"""
        for o in self.options:
            if name == o.name:
                return o.value
        if strict:
            raise ValueError("Could not find option {}!".format(name))
        return None

    def remove_option(self, name, strict=False):
        """Remove an option"""
        for i, o in enumerate(self.options):
            if name == o.name:
                return self.options.pop(i)
        if strict:
            raise ValueError("Could not find option {}!".format(name))
        return None

    def list_options(self):
        """Return a list of all available option keys"""
        return [o.name for o in self.options]

    def clear(self):
        self.options = []

    def validate(self):
        """Ensure no options are repeated"""
        names = [o.name for o in self.options]
        assert len(names) == len(set(names)), 'Duplicate options not allowed!'

    def __getitem__(self, name):
        if name == 'options':
            object.__getattribute__(self, name)

        names = [o.name for o in self.options]
        if name in names:
            return self.get_option(name)
        else:
            object.__getitem__(self, name)

    def __setitem__(self, name, value):
        try:
            names = [o.name for o in self.options]
            if name in names:
                return self.set_option(name, value)
            else:
                object.__setitem__(self, name, value)
        except AttributeError:
            object.__setitem__(self, name, value)
