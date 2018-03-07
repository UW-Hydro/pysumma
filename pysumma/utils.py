import shutil
import os
from urllib.request import urlretrieve
import subprocess


def install_test_cases(directory):
    url = "https://ral.ucar.edu/sites/default/files/public/projects/structure-for-unifying-multiple-modeling-alternatives-summa/summatestcases-2.x.tar.gz"
    filepath = directory + "summatestcases-2.x.tar.gz"
    urlretrieve(url, filepath)
    shutil.unpack_archive(filepath, extract_dir=os.path.dirname(filepath))

    cmd = "cd {}/summaTestCases_2.x/; ./installTestCases_local.sh".format(directory)
    subprocess.run(cmd, shell=True)

# dir = '/work/'

# install_test_cases(dir)

# install_local()
