from osgeo import gdal
import pandas as pd
import os
import numpy as np
import json
import pkg_resources
from .create_local_attribute import LocalAttributes

PARAMETER = pkg_resources.resource_filename(
        __name__, 'meta/parameter_ic.json')
with open(PARAMETER, 'r') as f:
    parameter_ic = json.load(f)

ssurgo_soil_db = pkg_resources.resource_filename(
        __name__, 'meta/ssurgo_soils_db.csv')

class ParamTrial(object):

    def __init__(self, filepath):
        self.filepath = filepath

    def tif_to_dataframe(self, path):
        raster = gdal.Open(path)
        rasterArray = raster.ReadAsArray()
        df = pd.DataFrame(rasterArray)
        return df

    def tif_to_dataframe_one_col(self, path, col_name):
        raster = gdal.Open(path)
        rasterArray = raster.ReadAsArray()
        df = pd.DataFrame(rasterArray)
        one_col = pd.concat([pd.DataFrame(df.loc[:,[i]].values, columns=[col_name]) for i in range(len(df.columns))], ignore_index=True)
        return one_col

    def delete_number(self, df, number):
        df.replace(number, np.nan, inplace=True)
        df_new = df.dropna().astype('int64')
        return df_new

    def merge_mukey_soil_depth(self, df, soil_depth_df):
        mukey_depth = df.merge(soil_depth_df, on='MUKEY')
        return mukey_depth

    def gru_hru_dim_parameter_trial(self, gru_name, dir_grassdata):
        SSURGO_soil_depth = pd.read_csv(ssurgo_soil_db)
        la = LocalAttributes(dir_grassdata)
        gru_mukey_1_col = la.tif_to_dataframe_one_col(os.path.join(dir_grassdata, gru_name +"_mukey.tif"), "MUKEY")
        gru_mukey_1_col.replace(-2147483648, np.nan, inplace=True)
        gru_mukey_1_col = gru_mukey_1_col.dropna().astype('int64')
        gru_mukey_depth = gru_mukey_1_col.merge(SSURGO_soil_depth, on='MUKEY')
        gru_mukey_layer = gru_mukey_depth[['nSoil']]
        gru_mukey_layer['nSoil'].unique().max()
        gru_parameter_trial_hru = gru_mukey_layer.assign(**{'frozenPrecipMultip': parameter_ic["frozenPrecipMultip"], 'theta_mp': parameter_ic["theta_mp"], 
                                                     'theta_sat': parameter_ic["theta_sat"], 'theta_res': parameter_ic["theta_res"], 
                                                     'vGn_alpha': parameter_ic["vGn_alpha"], 'vGn_n': parameter_ic["vGn_n"],
                                                     'f_impede': parameter_ic["f_impede"], 'k_soil': parameter_ic["k_soil"], 
                                                     'k_macropore': parameter_ic["k_macropore"], 'critSoilWilting': parameter_ic["critSoilWilting"], 
                                                     'critSoilTranspire': parameter_ic["critSoilTranspire"], 'winterSAI': parameter_ic["winterSAI"],
                                                     'summerLAI': parameter_ic["summerLAI"], 'heightCanopyTop': parameter_ic["heightCanopyTop"],
                                                     'heightCanopyBottom': parameter_ic["heightCanopyBottom"], 'kAnisotropic': parameter_ic["kAnisotropic"],
                                                     'zScale_TOPMODEL': parameter_ic["zScale_TOPMODEL"], 'qSurfScale': parameter_ic["qSurfScale"],
                                                     'fieldCapacity': parameter_ic["fieldCapacity"]                                                     
                                                     })
        return gru_parameter_trial_hru, gru_mukey_depth

    def hru_dim_parameter_trial_csv(self, gru_parameter_trial_hru, csv_name='parameter_trial_hru.csv'):
        hru_values = np.arange(len(gru_parameter_trial_hru))
        hru_values = hru_values + 1 
        gru_parameter_trial_hru['hru'] = hru_values
        gru_parameter_trial_hru['nSoil'] = gru_parameter_trial_hru['nSoil'].max()
        gru_parameter_trial_hru.to_csv(csv_name, index=False)