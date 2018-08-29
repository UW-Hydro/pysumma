import os


class BaseOption(object):
    """
    Base implementation for representing options in the various
    text based SUMMA configuration files. This class is meant to
    be extended rather than used directly.
    """

    def __init__(self, name):
        self.name = name


class OptionContainer(object):
    """
    Base implementation for representing text based configuration
    files for SUMMA. This class is meant to be extended rather than
    used directly.
    """

    def __init__(self, path, optiontype):
        """
        Instantiate the object and populate the
        values from the given filepath.
        """
        self.OptionType = optiontype
        self.opt_count = 0
        self.original_path = path
        self.header = []
        self.options = []
        self.read(path)

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

    def __repr__(self):
        return os.linesep.join([o.__repr__() for o in self.options])

    def read(self, path):
        """Read the configuration and populate the options"""
        with open(path, 'r') as f:
            self.original_contents = f.readlines()
        for line in self.original_contents:
            if line.startswith('!') and not self.opt_count:
                self.header.append(line)
            elif not line.startswith('!'):
                self.options.append(self.OptionType(
                    *self.get_constructor_args(line)))
                self.opt_count += 1

    def write(self, path=None):
        """Write the configuration given the values of the options"""
        self.validate()
        if not path:
            path = self.original_path
        with open(path, 'w') as f:
            f.writelines(self.header)
            f.writelines((o.__repr__() + '\n' for o in self.options))

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
        for i, o in self.options:
            if name == o.name:
                return self.options.pop(i)
        if strict:
            raise ValueError("Could not find option {}!".format(name))
        return None

    def validate(self):
        """Ensure no options are repeated"""
        names = [o.var for o in self.options]
        assert len(names) == len(set(names)), 'Duplicate options not allowed!'
