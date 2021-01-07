from osgeo import gdal
import pandas as pd
import os
import numpy as np


class LocalAttributes(object):

    def __init__(self, filepath):
        self.filepath = filepath

    def tif_to_dataframe(self, path):
        """Method to change a tif file to Pandas Dataframe

        Args:
            path (text): set a tif file of local attribute

        Returns:
            [DataFrame]: DataFrame,the same shape with TIF file, column is longitude, row is latitude
        """
        raster = gdal.Open(path)
        rasterArray = raster.ReadAsArray()
        df = pd.DataFrame(rasterArray)
        return df

    def tif_to_dataframe_one_col(self, path, col_name):
        """Method to a tif file to one column of DataFrame

        Args:
            path (text): set a tif file of local attribute
            col_name (text): set a column name of DataFrame

        Returns:
            [DataFrame]: DataFrame with one column
        """
        raster = gdal.Open(path)
        rasterArray = raster.ReadAsArray()
        df = pd.DataFrame(rasterArray)
        one_col = pd.concat([pd.DataFrame(df.loc[:, [i]].values, columns=[
                            col_name]) for i in range(len(df.columns))], ignore_index=True)
        return one_col

    def hru_id(self, df_format, df_format_col_name, null_num=255, hru_id_col_name="hruId", start_num=0):
        """Numbering unique value(hru_id) in each cell of raster

        Args:
            df_format (dataframe): output of tif_to_dataframe_one_col method
            df_format_col_name (str): set a column name of DataFrame
            null_num (int, optional): set null values. Defaults to 255.
            hru_id_col_name (str, optional): set a name of hur_id column. Defaults to "hruId".
            start_num (int, optional): set the start number of hru_id. Defaults to 0.

        Returns:
            [Dataframe]: dataframe with one vaible with hruId
        """
        count = start_num
        df_format[hru_id_col_name] = 0
        for index, raster in df_format.iterrows():
            if df_format[df_format_col_name].loc[index] != null_num:
                count = count + 1
                df_format[hru_id_col_name][index] = count
            else:
                pass

        return df_format

    def save_local_attribute(self, df_format, csv_name):
        """[summary]

        Args:
            df_format ([type]): [description]
            csv_name ([type]): [description]

        Returns:
            [type]: [description]
        """
        local_attribute = df_format.dropna()
        local_attribute.to_csv(csv_name, index=False)
        return local_attribute

    def one_col_add(self, df_format, col_name, value=10):
        df_format[col_name] = value
        return df_format

    def down_hru_index(self, df_format, fdr, hru_id_col_name="hruId", downhruindex_col_name="downHRUindex"):
        hruid_array = df_format[hru_id_col_name].values.reshape(
            fdr.shape[1], fdr.shape[0])
        hruid = pd.DataFrame(hruid_array)
        hruid = hruid.T
        downHRUindex = pd.DataFrame(np.zeros((hruid.shape[0], hruid.shape[1])))
        downHRUindex.astype('int64').head()
        for index_r in range(fdr.shape[0]):
            for index_c in range(fdr.shape[1]):
                if fdr.loc[index_r, index_c] == 1 and index_r-1 >= 0 and index_c+1 >= 0:
                    downHRUindex.loc[index_r,
                                     index_c] = hruid.loc[index_r-1, index_c+1]
                elif fdr.loc[index_r, index_c] == 2 and index_r-1 >= 0 and index_c >= 0:
                    downHRUindex.loc[index_r,
                                     index_c] = hruid.loc[index_r-1, index_c]
                elif fdr.loc[index_r, index_c] == 3 and index_r-1 >= 0 and index_c-1 >= 0:
                    downHRUindex.loc[index_r,
                                     index_c] = hruid.loc[index_r-1, index_c-1]
                elif fdr.loc[index_r, index_c] == 4 and index_r >= 0 and index_c-1 >= 0:
                    downHRUindex.loc[index_r,
                                     index_c] = hruid.loc[index_r, index_c-1]
                elif fdr.loc[index_r, index_c] == 5 and index_r+1 >= 0 and index_c-1 >= 0:
                    downHRUindex.loc[index_r,
                                     index_c] = hruid.loc[index_r+1, index_c-1]
                elif fdr.loc[index_r, index_c] == 6 and index_r+1 >= 0 and index_c >= 0:
                    downHRUindex.loc[index_r,
                                     index_c] = hruid.loc[index_r+1, index_c]
                elif fdr.loc[index_r, index_c] == 7 and index_r+1 >= 0 and index_c+1 >= 0:
                    downHRUindex.loc[index_r,
                                     index_c] = hruid.loc[index_r+1, index_c+1]
                elif fdr.loc[index_r, index_c] == 8 and index_r >= 0 and index_c+1 >= 0:
                    downHRUindex.loc[index_r,
                                     index_c] = hruid.loc[index_r, index_c+1]
                elif fdr.loc[index_r, index_c] < 0 and index_r >= 0 and index_c+1 >= 0:
                    downHRUindex.loc[index_r, index_c] = -9999
                else:
                    downHRUindex.loc[index_r, index_c] = 0
        downHRUindex = downHRUindex.astype('int64')
        downHRUindex_one_col = pd.concat([pd.DataFrame(downHRUindex.loc[:, [i]].values, columns=[
                                         downhruindex_col_name]) for i in range(len(downHRUindex.columns))], ignore_index=True)
        df_format[downhruindex_col_name] = downHRUindex_one_col.values
        return df_format

    def lulc_index(self, lulc_df, option='USGS'):
        lulc = pd.DataFrame(
            np.zeros((lulc_df.shape[0], lulc_df.shape[1])), columns=['vegTypeIndex'])
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

    def gru_local_attributes(self, gru_name, gru_num, dir_grassdata, hru_start_num, hru_area, contour_length=10, slopeTypeIndex=1, vegTypeIndex_option='USGS'):
        gru_drain = self.tif_to_dataframe(os.path.join(dir_grassdata, gru_name +"_drain.tif"))
        gru_drain_1_col = self.tif_to_dataframe_one_col(os.path.join(dir_grassdata, gru_name +"_drain.tif"), "fdr")
        # numbering unique value(hruid) in each cell of rasters
        gru_drain_1_col = self.hru_id(gru_drain_1_col, 'fdr', null_num=255, hru_id_col_name="hruId", start_num=hru_start_num)
        # create 'contourLength'
        gru_drain_1_col = self.one_col_add(gru_drain_1_col, 'contourLength', value=contour_length)
        # create 'downHRUindex'
        downHRUindex = self.down_hru_index(gru_drain_1_col, gru_drain, hru_id_col_name="hruId", downhruindex_col_name="downHRUindex")
        # create 'elevation'
        dem_one_col = self.tif_to_dataframe_one_col(os.path.join(dir_grassdata, gru_name +"_dem.tif"), "elevation")
        gru = self.one_col_add(downHRUindex, 'elevation', value=dem_one_col.values)
        # create 'hru', 'gruId', and 'hru2gruId'
        gru = self.one_col_add(gru, 'gruId', value=gru_num)
        gru = self.one_col_add(gru, 'hru2gruId', value=gru_num)
        # create 'HRUarea'
        gru = self.one_col_add(gru, 'HRUarea', value=hru_area)
        # create 'latitude' and 'longitude" (need to change to lon, lat)
        latitude_one_col = self.tif_to_dataframe_one_col(os.path.join(dir_grassdata, gru_name +"_ymap.tif"), "latitude")
        longitude_one_col = self.tif_to_dataframe_one_col(os.path.join(dir_grassdata, gru_name +"_xmap.tif"), "longitude")
        gru = self.one_col_add(gru, 'latitude', value=latitude_one_col.values)
        gru = self.one_col_add(gru, 'longitude', value=longitude_one_col.values)
        # create 'mHeight'
        gru = self.one_col_add(gru, 'mHeight', value=gru['elevation'] + 2)
        # create 'slopeTypeIndex'
        gru = self.one_col_add(gru, 'slopeTypeIndex', value=slopeTypeIndex)
        # create 'tan_slope'
        tan_slope_one_col = self.tif_to_dataframe_one_col(os.path.join(dir_grassdata, gru_name +"_slope.tif"), "slope")
        gru = self.one_col_add(gru, 'tan_slope', value=tan_slope_one_col.values)
        # create 'soilTypeIndex' (Ask Laurence soil_id meaning)
        soil_array_one_col = self.tif_to_dataframe_one_col(os.path.join(dir_grassdata, gru_name +"_soil_id.tif"), "soilTypeIndex")
        gru = self.one_col_add(gru, 'soilTypeIndex', value=soil_array_one_col.values)
        # create 'vegTypeIndex'
        nlcd_one_col = self.tif_to_dataframe_one_col(os.path.join(dir_grassdata, gru_name +"_NLCD.tif"), "vegTypeIndex")
        vegTypeIndex = self.lulc_index(nlcd_one_col, option=vegTypeIndex_option)
        gru = self.one_col_add(gru, 'vegTypeIndex', value=vegTypeIndex.values)
        gru = gru.drop('fdr', 1)
        gru = gru.dropna()
        return gru
