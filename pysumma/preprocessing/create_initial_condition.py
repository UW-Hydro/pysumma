from osgeo import gdal
import pandas as pd
import os
import numpy as np
import json
import pkg_resources
from .create_local_attribute import LocalAttributes

PARAMETER = pkg_resources.resource_filename(
        __name__, 'meta/hru_ic.json')
with open(PARAMETER, 'r') as f:
    hru_ic = json.load(f)

PARAMETER = pkg_resources.resource_filename(
        __name__, 'meta/mid_ic.json')
with open(PARAMETER, 'r') as f:
    mid_ic = json.load(f)

ssurgo_soil_db = pkg_resources.resource_filename(
        __name__, 'meta/ssurgo_soils_db.csv')

class InitialCondition(object):

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

    def gru_hru_dim_initial_condition(self, gru_name, dir_grassdata):
        SSURGO_soil_depth = pd.read_csv(ssurgo_soil_db)
        la = LocalAttributes(dir_grassdata)
        gru_mukey_1_col = la.tif_to_dataframe_one_col(os.path.join(dir_grassdata, gru_name +"_mukey.tif"), "MUKEY")
        gru_mukey_1_col.replace(-2147483648, np.nan, inplace=True)
        gru_mukey_1_col = gru_mukey_1_col.dropna().astype('int64')
        gru_mukey_depth = gru_mukey_1_col.merge(SSURGO_soil_depth, on='MUKEY')
        gru_mukey_layer = gru_mukey_depth[['nSoil']]
        gru_mukey_layer['nSoil'].unique().max()
        gru_initial_cond_hru = gru_mukey_layer.assign(**{'scalarv': hru_ic["scalarv"], 'scalarSnowAlbedo': hru_ic["scalarSnowAlbedo"], 
                                                     'scalarSnowDepth': hru_ic["scalarSnowDepth"], 'scalarSWE': hru_ic["scalarSWE"], 
                                                     'scalarSfcMeltPond': hru_ic["scalarSfcMeltPond"], 'scalarCanopyTemp': hru_ic["scalarCanopyTemp"],
                                                     'scalarCanopyLiq': hru_ic["scalarCanopyLiq"], 'scalarCanopyIce': hru_ic["scalarCanopyIce"], 
                                                     'scalarCanairTemp': hru_ic["scalarCanairTemp"], 'scalarAquiferStorage': hru_ic["scalarAquiferStorage"], 
                                                     'nSnow': hru_ic["nSnow"], 'dt_init': hru_ic["dt_init"]})
        return gru_initial_cond_hru, gru_mukey_depth

    def hru_dim_initial_condition_csv(self, initial_cond_hru, csv_name='initial_cond_hru.csv'):
        hru_values = np.arange(len(initial_cond_hru))
        hru_values = hru_values + 1 
        initial_cond_hru['hru'] = hru_values
        initial_cond_hru['nSoil'] = initial_cond_hru['nSoil'].max()
        initial_cond_hru.to_csv(csv_name, index=False)

    def ifc_dim_initial_condition(self, initial_cond_hru, gru_mukey_depth, csv_name='initial_cond_ifc.csv'):
        index_value = np.arange(0, len(initial_cond_hru), 1)
        mukey_depth = pd.concat(gru_mukey_depth)
        mukey_depth.index = index_value
        all_soil_depth = mukey_depth[['nSoil','SOL_Z0', 'SOL_Z1', 'SOL_Z2', 'SOL_Z3', 'SOL_Z4', 'SOL_Z5', 'SOL_Z6', 'SOL_Z7', 'SOL_Z8', 'SOL_Z9', 'SOL_Z10']]
        for i in range(all_soil_depth.shape[0]):
            if all_soil_depth['nSoil'].iloc[i] < all_soil_depth['nSoil'].max():
                while all_soil_depth['nSoil'].max() > all_soil_depth['nSoil'].iloc[i]:
                    all_soil_depth.iat[i,0] = all_soil_depth['nSoil'].iloc[i] + 1
                    all_soil_depth.iat[i,int(all_soil_depth['nSoil'].iloc[i]+1)] = all_soil_depth.iat[i,int(all_soil_depth['nSoil'].iloc[i])] + 0.01
        ifc = pd.DataFrame()
        for i in range(all_soil_depth.shape[0]):
            m_soil = all_soil_depth.loc[i, ]
            num = all_soil_depth['nSoil'][i]
            ifc_old = pd.DataFrame(m_soil[1:num+2].values)
            ifc = ifc.append(ifc_old, ignore_index=True)
        ifc['iLayerHeight']=ifc.values
        ifc = ifc[['iLayerHeight']]

        # hru number have to start from 1
        count = 0
        ifc['hru'] = 0
        for index, raster in ifc.iterrows():
            if ifc['iLayerHeight'].loc[index] == 0.00:
                count = count + 1
                ifc['hru'][index] = count
            else:
                ifc['hru'][index] = count
        
        initial_cond_ifc = ifc

        # hru number have to start from 1
        count = 0
        initial_cond_ifc['ifcToto'] = 0
        for index, raster in initial_cond_ifc.iterrows():
            if index == initial_cond_ifc.shape[0]-1:
                break
            elif initial_cond_ifc['hru'].loc[index] == initial_cond_ifc['hru'].loc[index+1]:
                count = count + 1
                initial_cond_ifc['ifcToto'][index] = count
            else:
                initial_cond_ifc['ifcToto'][index] = count+1
                count = 0
        initial_cond_ifc['ifcToto'][index] = count+1

        initial_cond_ifc.shape[0]
    
        initial_cond_ifc_sort = initial_cond_ifc.sort_values(by=['ifcToto', 'hru'])
        initial_cond_ifc_sort.to_csv(csv_name, index=False)
        return initial_cond_ifc_sort, all_soil_depth

    def mid_dim_initial_condition(self, all_soil_depth, csv_name='initial_cond_mid.csv'):
        mid = pd.DataFrame()
        for i in range(all_soil_depth.shape[0]):
            m_soil = all_soil_depth.loc[i, ]
            num = all_soil_depth['nSoil'][i]
            mid_old = pd.DataFrame(m_soil[1:num+2].values)
            midToto = mid_old.diff().loc[1:num]
            midToto['hru'] = i + 1
            mid = mid.append(midToto, ignore_index=True)
        mid['mLayerDepth'] = mid[0].values
        mid = mid[['hru', 'mLayerDepth']]
        # hru number have to start from 1
        count = 0
        mid['midToto'] = 0
        for index, raster in mid.iterrows():
            if index == mid.shape[0]-1:
                break
            elif mid['hru'].loc[index] == mid['hru'].loc[index+1]:
                count = count + 1
                mid['midToto'][index] = count
            else:
                mid['midToto'][index] = count+1
                count = 0
        mid['midToto'][index] = count+1
        initial_cond_mid = mid.assign(**{'mLayerVolFracLiq': mid_ic["mLayerVolFracLiq"], 'mLayerVolFracIce': mid_ic["mLayerVolFracIce"], 
                                        'mLayerTemp': mid_ic["mLayerTemp"], 'mLayerMatricHead': mid_ic["mLayerMatricHead"]})
        initial_cond_mid_sort = initial_cond_mid.sort_values(by=['midToto', 'hru'])
        initial_cond_mid_sort.to_csv(csv_name, index=False)
        return initial_cond_mid_sort