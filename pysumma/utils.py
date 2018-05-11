import shutil
import os
from urllib.request import urlretrieve
import subprocess
from hs_restclient import HydroShare

class utils():
    def install_test_cases_summa_web(save_filepath):
        url = "https://ral.ucar.edu/sites/default/files/public/projects/structure-for-unifying-multiple-modeling-alternatives-summa/summatestcases-2.x.tar.gz"
        filepath = save_filepath + "summatestcases-2.x.tar.gz"
        urlretrieve(url, filepath)
        shutil.unpack_archive(filepath, extract_dir=os.path.dirname(filepath))
        cmd = "cd {}/summaTestCases_2.x/; ./installTestCases_local.sh".format(save_filepath)
        subprocess.run(cmd, shell=True)

    def install_test_cases_hs(save_filepath):
        resource_id = 'a0105d479c334764ba84633c5b9c1c01'
        hs = HydroShare()
        hs.getResource(resource_id, destination = save_filepath, unzip = True)
        resource_name = 'summatestcases-2.x.tar.gz'
        testcase_filepath = save_filepath + '/' + resource_id + '/' + resource_id + '/data/contents/' + resource_name
        shutil.unpack_archive(testcase_filepath, extract_dir=os.path.dirname(testcase_filepath))
        cmd = "cd {}/summaTestCases_2.x/; ./installTestCases_local.sh".format(os.path.dirname(testcase_filepath))
        subprocess.run(cmd, shell=True)
        return  os.path.dirname(testcase_filepath)