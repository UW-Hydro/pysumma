from osgeo import gdal
import pandas as pd
import os
import numpy as np

class LocalAttributes(object):

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

    def hru_id(self, df_format, df_format_col_name, hru_id_col_name="hruId"):
        #one_col = pd.concat([pd.DataFrame(df_format.loc[:,[i]].values, columns=[df_format_col_name]) for i in range(len(df_format.columns))], ignore_index=True)
        #one_col.head()
        count = 0
        df_format[hru_id_col_name] = 0
        for index, raster in df_format.iterrows():
            if df_format[df_format_col_name].loc[index] > 0:
                count = count + 1
                df_format[hru_id_col_name][index] = count
        else:
            pass

        return df_format

    def save_local_attribute(self, df_format, csv_name):
        local_attribute = df_format.dropna()
        local_attribute.to_csv(csv_name, index=False)
        return local_attribute

    def one_col_add(self, df_format, col_name, value=10):
        df_format[col_name] = value
        return df_format

    def down_hru_index(self, df_format, one_col, fdr, hru_id_col_name="hruId", downhruindex_col_name="downHRUindex"):
        hruid_array = one_col[hru_id_col_name].values.reshape(fdr.shape[1], fdr.shape[0])
        hruid = pd.DataFrame(hruid_array)
        hruid = hruid.T
        downHRUindex = pd.DataFrame(np.zeros((hruid.shape[0], hruid.shape[1])))
        downHRUindex.astype('int64').head()
        for index_r in range(fdr.shape[0]):
            for index_c in range(fdr.shape[1]):
                if fdr.loc[index_r, index_c] == 1 and index_r-1 >= 0 and index_c+1 >= 0:
                    downHRUindex.loc[index_r, index_c] = hruid.loc[index_r-1, index_c+1]
                elif fdr.loc[index_r, index_c] == 2 and index_r-1 >= 0 and index_c >= 0:
                    downHRUindex.loc[index_r, index_c] = hruid.loc[index_r-1, index_c]
                elif fdr.loc[index_r, index_c] == 3 and index_r-1 >= 0 and index_c-1 >= 0:
                    downHRUindex.loc[index_r, index_c] = hruid.loc[index_r-1, index_c-1]
                elif fdr.loc[index_r, index_c] == 4 and index_r >= 0 and index_c-1 >= 0:
                    downHRUindex.loc[index_r, index_c] = hruid.loc[index_r, index_c-1]
                elif fdr.loc[index_r, index_c] == 5 and index_r+1 >= 0 and index_c-1 >= 0:
                    downHRUindex.loc[index_r, index_c] = hruid.loc[index_r+1, index_c-1]
                elif fdr.loc[index_r, index_c] == 6 and index_r+1 >= 0 and index_c >= 0:
                    downHRUindex.loc[index_r, index_c] = hruid.loc[index_r+1, index_c]
                elif fdr.loc[index_r, index_c] == 7 and index_r+1 >= 0 and index_c+1 >= 0:
                    downHRUindex.loc[index_r, index_c] = hruid.loc[index_r+1, index_c+1]
                elif fdr.loc[index_r, index_c] == 8 and index_r >= 0 and index_c+1 >= 0:
                    downHRUindex.loc[index_r, index_c] = hruid.loc[index_r, index_c+1]
                elif fdr.loc[index_r, index_c] < 0 and index_r >= 0 and index_c+1 >= 0:
                    downHRUindex.loc[index_r, index_c] = -9999
                else:
                    downHRUindex.loc[index_r, index_c] = 0
        downHRUindex = downHRUindex.astype('int64')
        downHRUindex_one_col = pd.concat([pd.DataFrame(downHRUindex.loc[:,[i]].values, columns=[downhruindex_col_name]) for i in range(len(downHRUindex.columns))], ignore_index=True)
        df_format[downhruindex_col_name] = downHRUindex_one_col.values
        return df_format

    def lulc_index(self, lulc_df, option='USGS'):
        lulc = pd.DataFrame(np.zeros((lulc_df.shape[0], lulc_df.shape[1])), columns=['vegTypeIndex'])
        lulc = lulc.astype('int64')
        if option == "USGS" and "USGS-RUC":
            for index, raster in lulc_df.iterrows():
                if lulc_df['vegTypeIndex'].loc[index] == 11 and 12 and 13 and 14 and 15 and 16 and 17:
                    lulc['vegTypeIndex'][index] = 1
                elif lulc_df['vegTypeIndex'].loc[index] == 22 and 24:
                    lulc['vegTypeIndex'][index] = 4
                elif lulc_df['vegTypeIndex'].loc[index] == 21:
                    lulc['vegTypeIndex'][index] = 5
                elif lulc_df['vegTypeIndex'].loc[index] == 23:
                    lulc['vegTypeIndex'][index] = 7
                elif lulc_df['vegTypeIndex'].loc[index] == 32 and 33:
                    lulc['vegTypeIndex'][index] = 9
                elif lulc_df['vegTypeIndex'].loc[index] == 41:
                    lulc['vegTypeIndex'][index] = 11
                elif lulc_df['vegTypeIndex'].loc[index] == 42:
                    lulc['vegTypeIndex'][index] = 13
                elif lulc_df['vegTypeIndex'].loc[index] == 43:
                    lulc['vegTypeIndex'][index] = 15
                elif lulc_df['vegTypeIndex'].loc[index] == 51 and 52 and 53 and 54 and 72:
                    lulc['vegTypeIndex'][index] = 16
                elif lulc_df['vegTypeIndex'].loc[index] == 31 and 62:
                    lulc['vegTypeIndex'][index] = 17
                elif lulc_df['vegTypeIndex'].loc[index] == 61:
                    lulc['vegTypeIndex'][index] = 18
                elif lulc_df['vegTypeIndex'].loc[index] == 82:
                    lulc['vegTypeIndex'][index] = 20
                elif lulc_df['vegTypeIndex'].loc[index] == 81:
                    lulc['vegTypeIndex'][index] = 21
                elif lulc_df['vegTypeIndex'].loc[index] == 84:
                    lulc['vegTypeIndex'][index] = 22
                elif lulc_df['vegTypeIndex'].loc[index] == 71 and 74 and 75 and 76 and 77 and 83:
                    lulc['vegTypeIndex'][index] = 23
                elif lulc_df['vegTypeIndex'].loc[index] == 91 and 92:
                    lulc['vegTypeIndex'][index] = 24
                elif lulc_df['vegTypeIndex'].loc[index] == 73:
                    lulc['vegTypeIndex'][index] = 27
                else:
                    pass

        elif option == "MODIFIED_IGBP_MODIS_NOAH":
            for index, raster in lulc_df.iterrows():
                if lulc_df['vegTypeIndex'].loc[index] == 42:
                    lulc['vegTypeIndex'][index] = 2
                elif lulc_df['vegTypeIndex'].loc[index] == 41:
                    lulc['vegTypeIndex'][index] = 4
                elif lulc_df['vegTypeIndex'].loc[index] == 43:
                    lulc['vegTypeIndex'][index] = 5
                elif lulc_df['vegTypeIndex'].loc[index] == 61 and 62:
                    lulc['vegTypeIndex'][index] = 11
                elif lulc_df['vegTypeIndex'].loc[index] == 21 and 22:
                    lulc['vegTypeIndex'][index] = 12
                elif lulc_df['vegTypeIndex'].loc[index] == 11 and 12 and 13 and 14 and 16 and 17:
                    lulc['vegTypeIndex'][index] = 13
                elif lulc_df['vegTypeIndex'].loc[index] == 23 and 24 and 31 and 32 and 33:
                    lulc['vegTypeIndex'][index] = 14
                elif lulc_df['vegTypeIndex'].loc[index] == 91 and 92:
                    lulc['vegTypeIndex'][index] = 15
                elif lulc_df['vegTypeIndex'].loc[index] == 51 and 52 and 53 and 54:
                    lulc['vegTypeIndex'][index] = 17
                elif lulc_df['vegTypeIndex'].loc[index] == 84:
                    lulc['vegTypeIndex'][index] = 19
                elif lulc_df['vegTypeIndex'].loc[index] == 71 and 72 and 73 and 74 and 75 and 76 and 77 and 81 and 82 and 83:
                    lulc['vegTypeIndex'][index] = 20
                else:
                    pass
        return lulc
