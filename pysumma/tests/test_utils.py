import shutil
import os
import unittest
import subprocess
from hs_restclient import HydroShare


class test_utils_class(unittest.TestCase):
    resource_id='e1a73bc4e7c34166895ff20ae53371f5'
    path = os.getcwd() + '/' + resource_id + '/' + resource_id + '/data/contents/'
    hs = HydroShare()
    hs.getResource(resource_id, destination=os.getcwd(), unzip=True)

    # unpack the simulation archive and remove unncessary files
    Model_Instance_Name = os.listdir(path)[0]
    shutil.unpack_archive(path + Model_Instance_Name, extract_dir=os.getcwd())
    cmd = "rm -rf " + resource_id
    subprocess.run(cmd, shell=True)
    #self.Model_Instance_Name = Model_Instance_Name

    def test_download_model_instance(self):
        model_instance = 'SummaModel_ReynoldsAspenStand_StomatalResistance_sopron'
        #self.assertEqual(get_model_instance(resource_id), model_instance_name)
        self.assertEqual(self.Model_Instance_Name.split('.')[0], model_instance)
        
if __name__ == '__main__':
    unittest.main()