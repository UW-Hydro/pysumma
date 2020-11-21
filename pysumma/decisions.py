import os
import re
import json
import pkg_resources
from .option import BaseOption
from .option import OptionContainer


METADATA_PATH = pkg_resources.resource_filename(
        __name__, 'meta/decisions.json')
with open(METADATA_PATH, 'r') as f:
    DECISION_META = json.load(f)


class DecisionOption(BaseOption):
    """Container for lines in a decisions file"""

    def __init__(self, name, value):
        super().__init__(name)
        self.description = DECISION_META[name]['description']
        self.available_options = DECISION_META[name]['options']
        self.set_value(value)

    def set_value(self, new_value):
        if new_value in self.available_options:
            self.value = new_value
        else:
            raise ValueError(os.linesep.join([
                'Invalid option given for decision: {}'.format(self.name),
                'You gave a value of: {}'.format(new_value),
                'Valid options include: {}'.format(self.available_options)]))

    def __str__(self):
        if self.name in ['simulStart', 'simulFinsh']:
            value = "'{}'".format(self.value)
        else:
            value = self.value
        return "{0}    {1: <20} ! {2}".format(
            self.name, value, self.description)


class Decisions(OptionContainer):
    """
    The Decisions object provides an interface to
    a SUMMA decisions file.
    """

    def __init__(self, dirpath, filepath=None):
        super().__init__(DecisionOption, dirpath, filepath)

    def set_option(self, key, value):
        try:
            o = self.get_option(key, strict=True)
            o.set_value(value)
        except ValueError:
            if key in DECISION_META.keys():
                self.options.append(DecisionOption(key, value))
            else:
                raise

    def get_constructor_args(self, line):
        decision, *value = line.split('!')[0].split()
        if isinstance(value, list):
            value = " ".join(value).replace("'", "")
        return decision, value
