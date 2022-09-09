import pandas as pd
from netCDF4 import Dataset, num2date, date2num
import numpy as np
from datetime import datetime, timedelta


def InitialCond_from_csv(hru_path, ifcToto_path, midToto_path, name):
    """Create initial conditons netcdf from csv file

    Args:
        hru_path (csv file): A CSV file with variables using hru Dimensions
        ifcToto_path (csv file): A CSV file with variables using ifcToto Dimensions
        midToto_path (csv file): tA CSV file with variables using midToto Dimensions
        name (text): Set the name of netcdf (ex. initial_conditions.nc)
    """

    # Create a netCDF file
    initial_cond = Dataset(name, "w", format="NETCDF3_CLASSIC")
    # Read csv file using Panda
    hru_initial_cond = pd.read_csv(hru_path, sep=',')
    ifcToto_initial_cond = pd.read_csv(ifcToto_path, sep=',')
    midToto_initial_cond = pd.read_csv(midToto_path, sep=',')

    # Create Dimension in a netCDF file
    hru = initial_cond.createDimension("hru", len(hru_initial_cond.index))
    scalarv = initial_cond.createDimension("scalarv", 1)
    ifcToto = initial_cond.createDimension("ifcToto", len(ifcToto_initial_cond.index)/len(hru_initial_cond.index))
    midToto = initial_cond.createDimension("midToto", len(midToto_initial_cond.index)/len(hru_initial_cond.index))
    midSoil = initial_cond.createDimension("midSoil", len(midToto_initial_cond.index)/len(hru_initial_cond.index))

    # set initial_condition_variables
    hru_initial_cond_variables = ['nSnow', 'nSoil']
    scalarv_initial_cond_variables = ["dt_init", "scalarCanopyIce", "scalarCanopyLiq", "scalarCanairTemp",
                                      "scalarCanopyTemp", "scalarSnowAlbedo", "scalarSWE", "scalarSnowDepth",
                                      "scalarSfcMeltPond", "scalarAquiferStorage"]
    ifcToto_initial_cond_variables = ["iLayerHeight"]
    midToto_initial_cond_variables = ["mLayerDepth", "mLayerTemp", "mLayerVolFracIce", "mLayerVolFracLiq"]
    midSoil_initial_cond_variables = ["mLayerMatricHead"]

    for var_name in hru_initial_cond_variables:
        data = initial_cond.createVariable(var_name, "i4", ("hru",))
        data[:] = hru_initial_cond[[var_name]].values

    for var_name in scalarv_initial_cond_variables:
        data = initial_cond.createVariable(var_name, "f8", ("scalarv", "hru",))
        data[:] = hru_initial_cond[[var_name]].values

    for var_name in ifcToto_initial_cond_variables:
        data = initial_cond.createVariable(var_name, "f8", ("ifcToto", "hru",))
        data[:] = ifcToto_initial_cond[[var_name]].values.reshape(int(len(ifcToto_initial_cond.index)/len(hru_initial_cond.index)), int(len(hru_initial_cond.index)))

    for var_name in midToto_initial_cond_variables:
        data = initial_cond.createVariable(var_name, "f8", ("midToto", "hru",))
        data[:] = midToto_initial_cond[[var_name]].values.reshape(int(len(midToto_initial_cond.index)/len(hru_initial_cond.index)), int(len(hru_initial_cond.index)))

    for var_name in midSoil_initial_cond_variables:
        data = initial_cond.createVariable(var_name, "f8", ("midSoil", "hru",))
        data[:] = midToto_initial_cond[[var_name]].values.reshape(int(len(midToto_initial_cond.index)/len(hru_initial_cond.index)), int(len(hru_initial_cond.index)))

    initial_cond.close()


def LocalAttribute_from_csv(localattri_path, name):
    """Create local attributes netcdf from csv file

    Args:
        localattri_path (csv file): A CSV file with local attributes
        name (text): Set the name of netcdf (ex. local_attributes.nc)
    """

    # Create a netCDF file
    loca_attri = Dataset(name, "w", format="NETCDF3_CLASSIC")

    # Read csv file using Panda
    loca_attri_data = pd.read_csv(localattri_path, sep=',')
    # Create Dimension in a netCDF file
    hru = loca_attri.createDimension("hru", len(loca_attri_data.index))
    gru = loca_attri.createDimension("gru", loca_attri_data['gruId'].nunique())

    # set local_attribute_variables
    local_attri_int_variables = ["downHRUindex", "soilTypeIndex", "vegTypeIndex", "slopeTypeIndex",
                                 "hruId", "hru2gruId"]
    local_attri_long_variables = ["mHeight", "contourLength", "tan_slope", "elevation", "longitude", "latitude",
                                  "HRUarea"]
    local_attri_gru_variables = ["gruId"]

    for var_name in local_attri_int_variables:
        data = loca_attri.createVariable(var_name, "i4", ("hru",))
        # creat Description
        data.long_name = ""
        data.units = ''
        data.v_type = ''
        data[:] = loca_attri_data[[var_name]].values

    for var_name in local_attri_long_variables:
        data = loca_attri.createVariable(var_name, "f8", ("hru",))
        # creat Description
        data.long_name = ""
        data.units = ''
        data[:] = loca_attri_data[[var_name]].values

    for var_name in local_attri_gru_variables:
        data = loca_attri.createVariable(var_name, "i4", ("gru",))
        # creat Description
        data.long_name = ""
        data.units = ''
        data.v_type = ''
        data[:] = loca_attri_data[var_name].unique()

    loca_attri.close()

def ParamTrial_from_csv(csv_path, name):
    """Create parameter trial netcdf from csv file

    Args:
        hru_path (csv file): A CSV file with variables using hru Dimensions
        name (text): Set the name of netcdf (ex. param_trial.nc)
    """

    # Create a netCDF file
    parameter_trial = Dataset(name, "w", format="NETCDF3_CLASSIC")
    # Read csv file using Panda
    hru_parameter_trial = pd.read_csv(csv_path, sep=',')

    # Create Dimension in a netCDF file
    hru = parameter_trial.createDimension("hru", len(hru_parameter_trial.index))
    #scalarv = parameter_trial.createDimension("scalarv", 1)

    # set initial_condition_variables
    scalarv_initial_cond_variables = ["frozenPrecipMultip", "theta_mp", "theta_sat", "theta_res", "vGn_alpha", "vGn_n", "f_impede", "k_soil",
                                      "k_macropore", "critSoilWilting", "critSoilTranspire", "winterSAI", "summerLAI", "heightCanopyTop",
                                      "heightCanopyBottom", "kAnisotropic", "zScale_TOPMODEL", "qSurfScale", "fieldCapacity"]

    for var_name in scalarv_initial_cond_variables:
        data = parameter_trial.createVariable(var_name, "f8", ("hru",))
        data[:] = hru_parameter_trial[[var_name]].values

    parameter_trial.close()
