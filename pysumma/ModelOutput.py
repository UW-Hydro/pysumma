from Option import Option


class ModelOutput:
    def __init__(self, filepath):
        self.filepath = filepath
        self.nSnow = ModelOutputManager('nSnow', self.filepath)
        self.nSoil = ModelOutputManager('nSoil', self.filepath)
        self.pptrate = ModelOutputManager('pptrate', self.filepath)
        self.airtemp = ModelOutputManager('airtemp', self.filepath)
        self.scalarRainPlusMelt = ModelOutputManager('scalarRainPlusMelt', self.filepath)
        self.scalarSWE = ModelOutputManager('scalarSWE', self.filepath)
        self.scalarThroughfallSnow = ModelOutputManager('scalarThroughfallSnow', self.filepath)
        self.scalarThroughfallRain = ModelOutputManager('scalarThroughfallRain', self.filepath)
        self.scalarSnowSublimation = ModelOutputManager('scalarSnowSublimation', self.filepath)
        self.scalarInfiltration = ModelOutputManager('scalarInfiltration', self.filepath)
        self.scalarExfiltration = ModelOutputManager('scalarExfiltration', self.filepath)
        self.scalarSurfaceRunoff = ModelOutputManager('scalarSurfaceRunoff', self.filepath)
        self.scalarSurfaceTemp = ModelOutputManager('scalarSurfaceTemp', self.filepath)
        self.scalarSenHeatTotal = ModelOutputManager('scalarSenHeatTotal', self.filepath)
        self.scalarLatHeatTotal = ModelOutputManager('scalarLatHeatTotal', self.filepath)
        self.iLayerHeight = ModelOutputManager('iLayerHeight', self.filepath)
        self.iLayerLiqFluxSoil = ModelOutputManager('iLayerLiqFluxSoil', self.filepath)
        self.mLayerTemp = ModelOutputManager('mLayerTemp', self.filepath)
        self.mLayerDepth = ModelOutputManager('mLayerDepth', self.filepath)
        self.mLayerLiqFluxSoil = ModelOutputManager('mLayerLiqFluxSoil', self.filepath)
        self.mLayerVolFracIce = ModelOutputManager('mLayerVolFracIce', self.filepath)
        self.mLayerVolFracLiq = ModelOutputManager('mLayerVolFracLiq', self.filepath)
        self.mLayerVolFracWat = ModelOutputManager('mLayerVolFracWat', self.filepath)
        self.mLayerMatricHead = ModelOutputManager('mLayerMatricHead', self.filepath)
        self.basin__SurfaceRunoff = ModelOutputManager('basin__SurfaceRunoff', self.filepath)
        self.basin__ColumnOutflow = ModelOutputManager('basin__ColumnOutflow', self.filepath)
        self.basin__AquiferStorage = ModelOutputManager('basin__AquiferStorage', self.filepath)
        self.basin__AquiferRecharge = ModelOutputManager('basin__AquiferRecharge', self.filepath)
        self.basin__AquiferBaseflow = ModelOutputManager('basin__AquiferBaseflow', self.filepath)
        self.basin__AquiferTranspire = ModelOutputManager('basin__AquiferTranspire', self.filepath)
        self.averageInstantRunoff = ModelOutputManager('averageInstantRunoff', self.filepath)
        self.averageRoutedRunoff = ModelOutputManager('averageRoutedRunoff', self.filepath)


class ModelOutputManager(Option):
    def __init__(self, name, filepath):
        super().__init__(name, filepath, key_position=0,value_position=2, delimiter=None)

    @property
    def value(self):
        return self.get_value()

    @value.setter
    def value(self, new_value):
        self.write_value(old_value=self.value, new_value=new_value)
