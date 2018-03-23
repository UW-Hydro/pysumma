import shutil
import os
from urllib.request import urlretrieve
import subprocess
from hs_restclient import HydroShare, HydroShareAuthBasic

class utils():

    def __init__(self, hs):
        self.hs = hs

    def install_test_cases(self, directory):
        url = "https://ral.ucar.edu/sites/default/files/public/projects/structure-for-unifying-multiple-modeling-alternatives-summa/summatestcases-2.x.tar.gz"
        filepath = directory + "summatestcases-2.x.tar.gz"
        urlretrieve(url, filepath)
        shutil.unpack_archive(filepath, extract_dir=os.path.dirname(filepath))
        cmd = "cd {}/summaTestCases_2.x/; ./installTestCases_local.sh".format(directory)
        subprocess.run(cmd, shell=True)

    def install_test_cases_hs(self, resource_id, save_filepath):
        self.hs.getResource(resource_id, destination = save_filepath, unzip = True)
        resource_name = 'summatestcases-2.x.tar.gz'
        testcase_filepath = save_filepath + '/' + resource_id + '/' + resource_id + '/data/contents/' + resource_name
        shutil.unpack_archive(testcase_filepath, extract_dir=os.path.dirname(testcase_filepath))
        cmd = "cd {}/summaTestCases_2.x/; ./installTestCases_local.sh".format(os.path.dirname(testcase_filepath))
        subprocess.run(cmd, shell=True)
        return  os.path.dirname(testcase_filepath)