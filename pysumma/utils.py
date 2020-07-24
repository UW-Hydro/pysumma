import itertools
import os
import shutil
from urllib.request import urlretrieve
import subprocess
from hs_restclient import HydroShare


def install_test_cases_summa_web(save_filepath):
    """Download SUMMA TestCases from UCAR web site.
    TODO: however this is old version of SUMMA TestCases
    """
    url = ("https://ral.ucar.edu/sites/default/files/public/projects/"
           "structure-for-unifying-multiple-modeling-alternatives-summa/"
           "summatestcases-2.x.tar.gz")
    filepath = save_filepath + "summatestcases-2.x.tar.gz"
    urlretrieve(url, filepath)
    shutil.unpack_archive(filepath, extract_dir=os.path.dirname(filepath))
    cmd = ("cd {}/summaTestCases_2.x/; "
           "./installTestCases_local.sh").format(save_filepath)
    subprocess.run(cmd, shell=True)

def get_hs_resource(resource_id, file_path):
    hs = HydroShare()
    hs.getResource(resource_id, destination=file_path, unzip=True)

    # unpack the simulation archive and remove unncessary files
    hs_resource_dir = os.path.join(file_path, resource_id, resource_id, 'data/contents/')
    hs_resource = os.listdir(hs_resource_dir)
    shutil.unpack_archive(hs_resource_dir+hs_resource[0], extract_dir=file_path)
    cmd = "rm -rf " + os.path.join(file_path, resource_id)
    subprocess.run(cmd, shell=True)

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
