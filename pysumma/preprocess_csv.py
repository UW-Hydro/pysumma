import pandas as pd
from netCDF4 import Dataset, date2num
from datetime import datetime, timedelta


def read_param_trial_csv(path, name):
    # Create a netCDF file
    param_trial = Dataset(path.split(path.split('/')[-1])[0]+'settings/'+name,
                          "w", format="NETCDF3_CLASSIC")
    # Read csv file using Panda
    param_trial_data = pd.read_csv(path, sep=',')
    # Create Dimension in a netCDF file
    # set param_trial_variables
    param_trial_variables = ['k_soil', 'kAnisotropic', 'qSurfScale',
                             'summerLAI', 'theta_mp', 'theta_res',
                             'theta_sat', 'vGn_alpha', 'vGn_n', 'winterSAI',
                             'zScale_TOPMODEL', 'critSoilTranspire',
                             'critSoilWilting', 'f_impede', 'fieldCapacity',
                             'frozenPrecipMultip', 'heightCanopyBottom',
                             'heightCanopyTop', 'k_macropore']

    for var_name in param_trial_variables:
        data = param_trial.createVariable(var_name, "f8", ("hru",))
        data[:] = param_trial_data[[var_name]].values

    param_trial.close()


def read_init_cond_csv(hru_path, ifcToto_path, midToto_path, name):
    # Create a netCDF file
    initial_cond = Dataset(
        hru_path.split(hru_path.split('/')[-1])[0]+'settings/'+name,
        "w", format="NETCDF3_CLASSIC")
    # Read csv file using Panda
    hru_initial_cond = pd.read_csv(hru_path, sep=',')
    ifcToto_initial_cond = pd.read_csv(ifcToto_path, sep=',')
    midToto_initial_cond = pd.read_csv(midToto_path, sep=',')

    # set initial_condition_variables
    hru_initial_cond_variables = ['nSnow', 'nSoil']
    scalarv_initial_cond_variables = ["dt_init", "scalarCanopyIce",
                                      "scalarCanopyLiq", "scalarCanairTemp",
                                      "scalarCanopyTemp", "scalarSnowAlbedo",
                                      "scalarSWE", "scalarSnowDepth",
                                      "scalarSfcMeltPond",
                                      "scalarAquiferStorage"]
    ifcToto_initial_cond_variables = ["iLayerHeight"]
    midToto_initial_cond_variables = ["mLayerDepth", "mLayerTemp",
                                      "mLayerVolFracIce", "mLayerVolFracLiq"]
    midSoil_initial_cond_variables = ["mLayerMatricHead"]

    for var_name in hru_initial_cond_variables:
        data = initial_cond.createVariable(var_name, "i4", ("hru",))
        data[:] = hru_initial_cond[[var_name]].values

    for var_name in scalarv_initial_cond_variables:
        data = initial_cond.createVariable(var_name, "f8", ("scalarv", "hru",))
        data[:] = hru_initial_cond[[var_name]].values

    for var_name in ifcToto_initial_cond_variables:
        data = initial_cond.createVariable(var_name, "f8", ("ifcToto", "hru",))
        data[:] = ifcToto_initial_cond[[var_name]].values

    for var_name in midToto_initial_cond_variables:
        data = initial_cond.createVariable(var_name, "f8", ("midToto", "hru",))
        data[:] = midToto_initial_cond[[var_name]].values

    for var_name in midSoil_initial_cond_variables:
        data = initial_cond.createVariable(var_name, "f8", ("midSoil", "hru",))
        data[:] = midToto_initial_cond[[var_name]].values

    initial_cond.close()


def read_local_attrs_csv(localattri_path, name):
    # Create a netCDF file
    loca_attri = Dataset(
        localattri_path.split(
            localattri_path.split('/')[-1])[0]+'settings/'+name,
        "w", format="NETCDF3_CLASSIC")
    # Read csv file using Panda
    loca_attri_data = pd.read_csv(localattri_path, sep=',')

    # set local_attribute_variables
    local_attri_int_variables = ["downHRUindex", "soilTypeIndex",
                                 "vegTypeIndex", "slopeTypeIndex",
                                 "hruId", "hru2gruId"]
    local_attri_long_variables = ["mHeight", "contourLength", "tan_slope",
                                  "elevation", "longitude", "latitude",
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
        data[:] = loca_attri_data[[var_name]][0:1].values

    loca_attri.close()


def forcingdata_from_csv(forcing_path, localattri_path, name,
                         start_date_time, time_step='3600.0'):
    # Create a netCDF file
    forcing = Dataset(forcing_path.split(
        forcing_path.split('/')[-1])[0]+'data/forcingData/'+name,
        "w", format="NETCDF3_CLASSIC")
    # Read csv file using Panda
    forcing_data = pd.read_csv(forcing_path, sep=',')
    loca_attri_data = pd.read_csv(localattri_path, sep=',')
    # Create Dimension in a netCDF file
    time = forcing.createDimension("time", None)

    # set local_attribute_variables
    local_attri_int_variables = ["hruId"]
    local_attri_long_variables = ["longitude", "latitude"]

    for var_name in local_attri_int_variables:
        data = forcing.createVariable(var_name, "i4", ("hru",))
        # creat Description
        data[:] = loca_attri_data[[var_name]].values

    for var_name in local_attri_long_variables:
        data = forcing.createVariable(var_name, "f8", ("hru",))
        # creat Description
        data[:] = loca_attri_data[[var_name]].values

    time = forcing.createVariable("time", "f8", ("time"))
    time.units = 'days since ' + start_date_time
    time.long_name = "Observation time"
    time.calendar = "standard"
    dates = []
    for n in range(int(len(forcing_data) / len(loca_attri_data))):
        dates.append(datetime(int(start_date_time[0:4]),
                              int(start_date_time[5:7]),
                              (int(start_date_time[8:10]))
                              + n * timedelta(days=1)))  # hours=1
    time[:] = date2num(dates, units=time.units, calendar=time.calendar)

    data_step = forcing.createVariable("data_step", "f8", )
    data_step.units = 'days'
    data_step.long_name = "data step length in days"
    data_step[:] = time_step

    LWRadAtm = forcing.createVariable("LWRadAtm", "f8", ("time", "hru",),
                                      fill_value=-999.0)
    LWRadAtm.units = 'W m-2'
    LWRadAtm.long_name = "downward longwave radiation at the upper boundary"
    LWRadAtm.v_type = 'scalarv'
    LWRadAtm_one = forcing_data[['LWRadAtm']].values
    LWRadAtm_many = LWRadAtm_one.reshape(
        int(len(forcing_data))).reshape(
            int(len(forcing_data) / len(loca_attri_data)),
        int(len(loca_attri_data)))
    LWRadAtm[:] = LWRadAtm_many

    SWRadAtm = forcing.createVariable("SWRadAtm", "f8", ("time", "hru",),
                                      fill_value=-999.0)
    SWRadAtm.units = 'W m-2'
    SWRadAtm.long_name = "downward shortwave radiation at the upper boundary"
    SWRadAtm.v_type = 'scalarv'
    SWRadAtm_one = forcing_data[['SWRadAtm']].values
    SWRadAtm_many = SWRadAtm_one.reshape(
        int(len(forcing_data))).reshape(
            int(len(forcing_data) / len(loca_attri_data)),
        int(len(loca_attri_data)))
    SWRadAtm[:] = SWRadAtm_many

    airpres = forcing.createVariable("airpres", "f8", ("time", "hru",),
                                     fill_value=-999.0)
    airpres.units = 'Pa'
    airpres.long_name = "air pressure at the measurement height"
    airpres.v_type = 'scalarv'
    airpres_one = forcing_data[['airpres']].values
    airpres_many = airpres_one.reshape(
        int(len(forcing_data))).reshape(
            int(len(forcing_data) / len(loca_attri_data)),
        int(len(loca_attri_data)))
    airpres[:] = airpres_many

    airtemp = forcing.createVariable("airtemp", "f8", ("time", "hru",),
                                     fill_value=-999.0)
    airtemp.units = 'K'
    airtemp.long_name = "air temperature at the measurement height"
    airtemp.v_type = 'scalarv'
    airtemp_one = forcing_data[['airtemp']].values
    airtemp_many = airtemp_one.reshape(
        int(len(forcing_data))).reshape(
            int(len(forcing_data) / len(loca_attri_data)),
        int(len(loca_attri_data)))
    airtemp[:] = airtemp_many

    pptrate = forcing.createVariable("pptrate", "f8", ("time", "hru",),
                                     fill_value=-999.0)
    pptrate.units = 'kg m-2 s-1'
    pptrate.long_name = "Precipitation rate"
    pptrate.v_type = 'scalarv'
    pptrate_one = forcing_data[['pptrate']].values
    pptrate_many = pptrate_one.reshape(
        int(len(forcing_data))).reshape(
            int(len(forcing_data) / len(loca_attri_data)),
        int(len(loca_attri_data)))
    pptrate[:] = pptrate_many

    spechum = forcing.createVariable("spechum", "f8", ("time", "hru",),
                                     fill_value=-999.0)
    spechum.units = 'g g-1'
    spechum.long_name = "specific humidity at the measurement heigh"
    spechum.v_type = 'scalarv'
    spechum_one = forcing_data[['spechum']].values
    spechum_many = spechum_one.reshape(
        int(len(forcing_data))).reshape(
            int(len(forcing_data) / len(loca_attri_data)),
        int(len(loca_attri_data)))
    spechum[:] = spechum_many

    windspd = forcing.createVariable("windspd", "f8", ("time", "hru",),
                                     fill_value=-999.0)
    windspd.units = 'm s-1'
    windspd.long_name = "wind speed at the measurement height"
    windspd.v_type = 'scalarv'
    windspd_one = forcing_data[['windspd']].values
    windspd_many = windspd_one.reshape(
        int(len(forcing_data))).reshape(
            int(len(forcing_data) / len(loca_attri_data)),
        int(len(loca_attri_data)))
    windspd[:] = windspd_many

    forcing.close()
