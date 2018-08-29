import os
import re
from pysumma.Option import BaseOption
from pysumma.Option import OptionContainer

DECISION_OPTIONS = {
        'simulStart': ['YYYY-MM-DD hh:mm'],
        'simulFinsh': ['YYYY-MM-DD hh:mm'],
        'soilCatTbl': ['STAS', 'STAS-RUC', 'ROSETTA'],
        'vegeParTbl': ['USGS', 'MODIFIED_IGBP_MODIS_NOAH'],
        'soilStress': ['NoahType', 'CLM_Type', 'SiB_Type'],
        'stomResist': ['BallBerry', 'Jarvis', 'simpleResistance',
                       'BallBerryFlex', 'BallBerryTest'],
        'bbTempFunc': ['q10Func', 'Arrhenius'],
        'bbHumdFunc': ['humidLeafSurface', 'scaledHyperbolic'],
        'bbElecFunc': ['linear', 'linearJmax', 'quadraticJmax'],
        'bbCO2point': ['origBWB', 'Leuning'],
        'bbNumerics': ['NoahMPsolution', 'newtonRaphson'],
        'bbAssimFnc': ['colimitation', 'minFunc'],
        'bbCanIntg8': ['constantScaling', 'laiscaling'],
        'num_method': ['itertive', 'non_iter', 'itersurf'],
        'fDerivMeth': ['numericl', 'analytic'],
        'LAI_method': ['monTable', 'specified'],
        'cIntercept': ['sparseCanopy', 'storageFunc', 'notPopulatedYet'],
        'f_Richards': ['moisture', 'mixdform'],
        'groundwatr': ['qTopmodl', 'bigBuckt', 'noXplict'],
        'hc_profile': ['constant', 'pow_prof'],
        'bcUpprTdyn': ['presTemp', 'nrg_flux', 'zeroFlux'],
        'bcLowrTdyn': ['presTemp', 'zeroFlux'],
        'bcUpprSoiH': ['presHead', 'liq_flux'],
        'bcLowrSoiH': ['presHead', 'bottmPsi', 'drainage', 'zeroFlux'],
        'veg_traits': ['Raupach_BLM1994', 'CM_QJRMS1988', 'vegTypeTable'],
        'rootProfil': ['powerLaw', 'doubleExp'],
        'canopyEmis': ['simplExp', 'difTrans'],
        'snowIncept': ['stickySnow', 'lightSnow'],
        'windPrfile': ['exponential', 'logBelowCanopy'],
        'astability': ['standard', 'louisinv', 'mahrtexp'],
        'compaction': ['consettl', 'anderson'],
        'snowLayers': ['jrdn1991', 'CLM_2010'],
        'thCondSnow': ['tyen1965', 'melr1977', 'jrdn1991', 'smnv2000'],
        'thCondSoil': ['funcSoilWet', 'mixConstit', 'hanssonVZJ'],
        'canopySrad': ['noah_mp', 'CLM_2stream', 'UEB_2stream',
                       'NL_scatter', 'BeersLaw'],
        'alb_method': ['conDecay', 'varDecay'],
        'spatial_gw': ['localColumn', 'singleBasin'],
        'subRouting': ['timeDlay', 'qInstant'],
        'snowDenNew': ['hedAndPom', 'anderson', 'pahaut_76', 'constDens']
        }

DECISION_DESCRIPTIONS = {
        'simulStart': 'simulation start time',
        'simulFinsh': 'simulation end time',
        'soilCatTbl': 'soil-category dataset',
        'vegeParTbl': 'vegetation-category dataset',
        'soilStress': ('choice of function for the soil moisture '
                       'control on stomatal resistance'),
        'stomResist': 'choice of function for stomatal resistance',
        'bbTempFunc': ('Ball-Berry: leaf temperature controls on '
                       'photosynthesis + stomatal resistance'),
        'bbHumdFunc': 'Ball-Berry: humidity controls on stomatal resistance',
        'bbElecFunc': 'Ball-Berry: dependence of photosynthesis on PAR',
        'bbCO2point': ('Ball-Berry: use of CO2 compensation point '
                       'to calculate stomatal resistance'),
        'bbNumerics': 'Ball-Berry: iterative numerical solution method',
        'bbAssimFnc': 'Ball-Berry: controls on carbon assimilation',
        'bbCanIntg8': ('Ball-Berry: scaling of photosynthesis '
                       'from the leaf to the canopy'),
        'num_method': 'choice of numerical method',
        'fDerivMeth': 'choice of method to calculate flux derivatives',
        'LAI_method': 'choice of method to determine LAI and SAI',
        'cIntercept': 'choice of parameterization for canopy interceptio',
        'f_Richards': 'form of Richards\' equation',
        'groundwatr': 'choice of groundwater parameterization',
        'hc_profile': 'choice of hydraulic conductivity profile',
        'bcUpprTdyn': 'type of upper boundary condition for thermodynamics',
        'bcLowrTdyn': 'type of lower boundary condition for thermodynamics',
        'bcUpprSoiH': 'type of upper boundary condition for soil hydrology',
        'bcLowrSoiH': 'type of lower boundary condition for soil hydrology',
        'veg_traits': ('choice of parameterization for vegetation roughness '
                       'length and displacement height'),
        'rootProfil': 'choice of parameterization for the rooting profile',
        'canopyEmis': 'choice of parameterization for canopy emissivity',
        'snowIncept': 'choice of parameterization for snow interception',
        'windPrfile': 'choice of canopy wind profile',
        'astability': 'choice of stability function',
        'compaction': 'choice of compaction routine',
        'snowLayers': 'choice of method to combine and sub-divide snow layers',
        'thCondSnow': 'choice of thermal conductivity representation for snow',
        'thCondSoil': 'choice of thermal conductivity representation for soil',
        'canopySrad': 'choice of method for canopy shortwave radiation',
        'alb_method': 'choice of albedo representation',
        'spatial_gw': ('choice of method for spatial '
                       'representation of groundwater'),
        'subRouting': 'choice of method for sub-grid routing',
        'snowDenNew': 'choice of method for new snow density'
        }


class DecisionOption(BaseOption):
    """Container for lines in a decisions file"""

    def __init__(self, name, value):
        super().__init__(name)
        self.description = DECISION_DESCRIPTIONS[self.name]
        self.available_options = DECISION_OPTIONS[self.name]
        self.set_value(value)

    def set_value(self, new_value):
        datestring = r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}'
        if (self.name in ['simulStart', 'simulFinsh'] and
                re.match(datestring, new_value) is not None):
            self.value = new_value
        elif new_value in self.available_options:
            self.value = new_value
        else:
            raise ValueError(os.linesep.join([
                  'Invalid option given for decision: {}'.format(self.name),
                  'You gave a value of: {}'.format(new_value),
                  'Valid options include: {}'.format(self.available_options)]))

    def __repr__(self):
        return "{0}    {1: <20} ! {2}".format(self.name, self.value, self.description)


class Decisions(OptionContainer):
    """
    The Decisions object provides an interface to
    a SUMMA decisions file.
    """

    def __init__(self, path):
        super().__init__(path, DecisionOption)

    def set_option(self, key, value):
        try:
            o = self.get_option(key, strict=True)
            o.value = value
        except ValueError:
            if key in DECISION_OPTIONS.keys():
                self.options.append(DecisionOption(key, value))
            else:
                raise

    def get_constructor_args(self, line):
        decision, *value = line.split('!')[0].split()
        if isinstance(value, list):
            value = " ".join(value).replace("'", "")
        return decision, value
