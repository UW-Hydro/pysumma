import shutil
import os
from urllib.request import urlretrieve
import subprocess
from hs_restclient import HydroShare


# download SUMMA TestCases from ucar web site,
def install_test_cases_summa_web(save_filepath):
    url = ("https://ral.ucar.edu/sites/default/files/public/projects/"
           "structure-for-unifying-multiple-modeling-alternatives-summa/"
           "summatestcases-2.x.tar.gz")
    filepath = save_filepath + "summatestcases-2.x.tar.gz"
    urlretrieve(url, filepath)
    shutil.unpack_archive(filepath, extract_dir=os.path.dirname(filepath))
    cmd = "cd {}/summaTestCases_2.x/; ./installTestCases_local.sh".format(
        save_filepath)
    subprocess.run(cmd, shell=True)


# download SUMMA TestCase from HydroShare
def get_hs_resource(resource_id, file_path):
    hs = HydroShare()
    hs.getResource(resource_id, destination=file_path, unzip=True)

    # unpack the simulation archive and remove unncessary files
    hs_resource_dir = os.path.join(file_path, resource_id, resource_id, 'data/contents/')
    hs_resource = os.listdir(hs_resource_dir)
    shutil.unpack_archive(hs_resource_dir+hs_resource[0], extract_dir=file_path)
    shutil.rmtree(os.path.join(file_path, resource_id))
    return hs_resource[0].split(".")[0]
