from ModelOutput import ModelOutputManager, ModelOutput
from shutil import copyfile
import unittest
import os


class TestModelOutput(unittest.TestCase):
    my_path = os.path.abspath(os.path.dirname(__file__)) + '/meta/'
    filename = 'Model_Output.txt'
    filepath = os.path.join(my_path, filename)
    filename2 = 'tmp_{}'.format(filename)
    filepath2 = os.path.join(my_path, filename2)
    copyfile(filepath, filepath2)
    mo = ModelOutput(filepath2)

    def read_value_from_file(self, setting_name):
        with open(self.filepath2) as ModelOutput_file:
            for line in ModelOutput_file:
                if setting_name in line:
                    return line.split("|")[1].strip()

    def value_test(self, name, ModelOutputManagerObject):
        # Check to see if the name and value match between the file and the object
        assert ModelOutputManagerObject.name == name, "MO Object name is: " + ModelOutputManagerObject.name + ' but in the file is ' + name
        assert ModelOutputManagerObject.value == self.read_value_from_file(name), "MO Object value is: '" + \
                                                                                  ModelOutputManagerObject.value +\
                                                                                  "', but '" + self.read_value_from_file(name) \
                                                                                  + "' was in the file."
        # Change the value in the object
        ModelOutputManager.value = '2'

        # Check to see if the value is reflected in the file
        assert ModelOutputManagerObject.value == self.read_value_from_file(name), "MO Object " + ModelOutputManagerObject.name + " value is: '" + ModelOutputManagerObject.value + "', but '" + self.read_value_from_file(name) + "' was in the file."

    def test_ModelOutputParameters(self):
        self.value_test('nSnow', self.mo.nSnow)
        self.value_test('nSoil', self.mo.nSoil)
        self.value_test('pptrate', self.mo.pptrate)
        self.value_test('airtemp', self.mo.airtemp)
        self.value_test('scalarRainPlusMelt', self.mo.scalarRainPlusMelt)
        self.value_test('scalarSWE', self.mo.scalarSWE)
        self.value_test('scalarThroughfallSnow', self.mo.scalarThroughfallSnow)
        self.value_test('scalarThroughfallRain', self.mo.scalarThroughfallRain)
        self.value_test('scalarSnowSublimation', self.mo.scalarSnowSublimation)
        self.value_test('scalarInfiltration', self.mo.scalarInfiltration)
        self.value_test('scalarExfiltration', self.mo.scalarExfiltration)
        self.value_test('scalarSurfaceRunoff', self.mo.scalarSurfaceRunoff)
        self.value_test('scalarSurfaceTemp', self.mo.scalarSurfaceTemp)
        self.value_test('scalarSenHeatTotal', self.mo.scalarSenHeatTotal)
        self.value_test('scalarLatHeatTotal', self.mo.scalarLatHeatTotal)
        self.value_test('iLayerHeight', self.mo.iLayerHeight)
        self.value_test('iLayerLiqFluxSoil', self.mo.iLayerLiqFluxSoil)
        self.value_test('mLayerTemp', self.mo.mLayerTemp)
        self.value_test('mLayerDepth', self.mo.mLayerDepth)
        self.value_test('mLayerLiqFluxSoil', self.mo.mLayerLiqFluxSoil)
        self.value_test('mLayerVolFracIce', self.mo.mLayerVolFracIce)
        self.value_test('mLayerVolFracLiq', self.mo.mLayerVolFracLiq)
        self.value_test('mLayerVolFracWat', self.mo.mLayerVolFracWat)
        self.value_test('mLayerMatricHead', self.mo.mLayerMatricHead)
        self.value_test('basin__SurfaceRunoff', self.mo.basin__SurfaceRunoff)
        self.value_test('basin__ColumnOutflow', self.mo.basin__ColumnOutflow)
        self.value_test('basin__AquiferRecharge', self.mo.basin__AquiferRecharge)
        self.value_test('basin__AquiferStorage', self.mo.basin__AquiferStorage)
        self.value_test('basin__AquiferBaseflow', self.mo.basin__AquiferBaseflow)
        self.value_test('basin__AquiferTranspire', self.mo.basin__AquiferTranspire)
        self.value_test('averageInstantRunoff', self.mo.averageInstantRunoff)
        self.value_test('averageRoutedRunoff', self.mo.averageRoutedRunoff)


