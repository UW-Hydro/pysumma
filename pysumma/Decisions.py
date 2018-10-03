import os
import re
import json
import pkg_resources
from .Option import BaseOption
from .Option import OptionContainer


METADATA_PATH = pkg_resources.resource_filename(
        __name__, 'metadata/decisions.json')
DECISION_META = json.load(METADATA_PATH)


class DecisionOption(BaseOption):
    """Container for lines in a decisions file"""

    def __init__(self, name, value):
        super().__init__(name)
        self.description = DECISION_META[name]['options']
        self.available_options = DECISION_META[name]['description']
        self.set_value(value)

    def set_value(self, new_value):
        datestring = r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}'
        if (self.name in ['simulStart', 'simulFinsh'] and
                re.match(datestring, new_value) is not None):
            self.value = new_value
        elif new_value in self.available_options:
            self.value = new_value
        else:
            raise ValueError(os.linesep.join([
                  'Invalid option given for decision: {}'.format(self.name),
                  'You gave a value of: {}'.format(new_value),
                  'Valid options include: {}'.format(self.available_options)]))

    def __repr__(self):
        return "{0}    {1: <20} ! {2}".format(
                self.name, self.value, self.description)


class Decisions(OptionContainer):
    """
    The Decisions object provides an interface to
    a SUMMA decisions file.
    """

    def __init__(self, path):
        super().__init__(path, DecisionOption)

    def set_option(self, key, value):
        try:
            o = self.get_option(key, strict=True)
            o.value = value
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
