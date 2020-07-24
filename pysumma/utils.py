import itertools
import os
import shutil
from urllib.request import urlretrieve
import subprocess

def product_dict(**kwargs):
    """
    Take a set of dictionary arguments and generate a new set of
    dictionaries that have all combinations of values for each key.
    """
    keys, vals = kwargs.keys(), kwargs.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))


class ChainDict(dict):
    """
    A dictionary which instead of overwriting on existing keys,
    will instead store the values in a list.
    """
    def __setitem__(self, key, val):
        newval = [val]
        if key in list(self.keys()):
            oldval = self.__getitem__(key)
            newval = list(set(oldval + newval))
        dict.__setitem__(self, key, newval)
