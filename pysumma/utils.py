import shutil
import os
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


def install_test_cases_hs(save_filepath):
    '''download SUMMA TestCase from HydroShare
    which is sopron version of SUMMA TestCases'''
    resource_id = 'a0105d479c334764ba84633c5b9c1c01'
    hs = HydroShare()
    hs.getResource(resource_id, destination=save_filepath, unzip=True)
    resource_name = 'summatestcases-2.x.tar.gz'
    filepath = os.path.join(save_filepath, resource_id, resource_id,
                            'data/contents', resource_name)
    shutil.unpack_archive(filepath,
                          extract_dir=os.path.dirname(filepath))
    cmd = ("cd {}/summaTestCases_2.x/;"
           "./installTestCases_local.sh").format(os.path.dirname(filepath))
    subprocess.run(cmd, shell=True)
    return os.path.dirname(filepath)


def download_executable_lubuntu_hs(save_filepath):
    '''This method is necessary, when user wants to
    run SUMMA with local execution file.'''
    resource_id = 'a5dbd5b198c9468387f59f3fefc11e22'
    hs = HydroShare()
    hs.getResource(resource_id, destination=save_filepath, unzip=True)
    resource_name = 'summa-master.zip'
    filepath = os.path.join(save_filepath, resource_id, resource_id,
                            'data/contents', resource_name)
    shutil.unpack_archive(filepath, extract_dir=os.path.dirname(filepath))
    executable = os.path.join(save_filepath, resource_id, resource_id,
                              'data/contents/summa-master/bin')
    return os.path.dirname(executable)


def download_model_instance_sopron(resource_id):
    path = os.path.join(os.getcwd(), resource_id, resource_id, 'data/contents')
    hs = HydroShare()
    hs.getResource(resource_id, destination=os.getcwd(), unzip=True)

    # unpack the simulation archive and remove unncessary files
    Model_Instance_Name = os.listdir(path)[0]
    shutil.unpack_archive(path + Model_Instance_Name+'.zip',
                          extract_dir=os.getcwd())
    cmd = "rm -rf " + resource_id
    subprocess.run(cmd, shell=True)
    cmd = ('cd ' + Model_Instance_Name.split('.')[0]
           + '/; chmod +x ./installTestCases_local.sh')
    subprocess.run(cmd, shell=True, stderr=subprocess.STDOUT)
    cmd = ('cd ' + Model_Instance_Name.split('.')[0]
           + '/; ./installTestCases_local.sh')
    subprocess.run(cmd, shell=True, stderr=subprocess.STDOUT)
    return Model_Instance_Name.split('.')[0]


def download_model_instance(resource_id):
    path = os.path.join(os.getcwd(), resource_id, resource_id, 'data/contents')
    hs = HydroShare()
    hs.getResource(resource_id, destination=os.getcwd(), unzip=True)

    # unpack the simulation archive and remove unncessary files
    Model_Instance_Name = os.listdir(path)[0]
    shutil.unpack_archive(path + Model_Instance_Name+'.zip',
                          extract_dir=os.getcwd())
    cmd = "rm -rf " + resource_id
    subprocess.run(cmd, shell=True)
    return Model_Instance_Name.split('.')[0]
