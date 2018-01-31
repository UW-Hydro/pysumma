import seaborn as sns
import xarray as xr
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

class Plotting:

	colors = ["windows blue", "amber", "greyish", "faded green", "dusty purple"]
	sns.set_palette(sns.xkcd_palette(colors))

	def __init__(self, filepath):
		self.filepath = filepath

	def open_netcdf(self):
		filepath = self.filepath
		ds = xr.open_dataset(filepath)
		print(ds)
		return ds

	def plot_1d(self, ds, varibale_num):
		var_dict= dict(ds.data_vars)
		var_list_key = list(var_dict.keys())[varibale_num]
		plot = ds[var_list_key].plot()
		plt.ylabel('{} ({})'.format(ds[var_list_key].long_name, ds[var_list_key].units))
		plt.show()
		return plt.show()

	def plot_1d_hru(self, ds, hru_num, varibale_num):
		var_dict= dict(ds.data_vars)
		var_list_key = list(var_dict.keys())[varibale_num]
		plot = ds[var_list_key][:,hru_num].plot()
		plt.ylabel('{} ({})'.format(ds[var_list_key].long_name, ds[var_list_key].units))
		plt.show()
		return plt.show()

	def plot_1d_layer(self, ds, hru_num, varibale_num_Y, start_index_X): #='mLayerVolFracWat', start_index='midTotoStartIndex'
		var_dict= dict(ds.data_vars)
		var_list_key_Y = list(var_dict.keys())[varibale_num_Y]
		plot = ds[var_list_key_Y][:,hru_num].plot()
		timestep = 2207
		layers = ds.nLayers[timestep].values[0]  # extract the number of layers associated with the first timestep
		var_list_key_X = list(var_dict.keys())[start_index_X]
		startIndex = ds[var_list_key_X][timestep].values[0] - 1  # - 1 since the SUMMA indices are 1-based and python indices are 0-based
		endIndex = startIndex + layers
		ds[var_list_key_Y][startIndex:endIndex, 0].plot(label='t = {: 2d}'.format(timestep))
		plt.ylabel('{} ({})'.format(ds[var_list_key_Y].long_name, ds[var_list_key_Y].units))
		plt.show()
		return plt.show()

	def plot_2d(self, ds, hru_num, varibale_num_Y, varibale_num_X, midto):
		var_dict= dict(ds.data_vars)
		var_list_key_Y = list(var_dict.keys())[varibale_num_Y]
		var_list_key_X = list(var_dict.keys())[varibale_num_X]

		for timestep in [99, 999, 1999]:
			layers = ds.nLayers[timestep].values[0]  # extract the number of layers associated with the first timestep
			var_list_key = list(var_dict.keys())[midto]
			startIndex = ds[var_list_key][timestep].values[0] - 1  # - 1 since the SUMMA indices are 1-based and python indices are 0-based
			endIndex = startIndex + layers
			plot = plt.plot(ds[var_list_key_X][startIndex:endIndex],
							ds[var_list_key_Y][startIndex:endIndex,0],
							label='t = {: 2d}'.format(timestep+1))
		plt.ylabel('{} ({})'.format(ds[var_list_key_Y].long_name, ds[var_list_key_Y].units))
		plt.xlabel('{} ({})'.format(ds[var_list_key_X].long_name, ds[var_list_key_X].units))
		plt.legend(loc=3)
		plt.show()
		return plt.show()

#		def Plot_2D_layer(self, ds, hru_num, varibale_num_Y, varibale_num_X, midto):





# path = 'D:\\pysumma\\pysumma_alpha\\pysumma\\pysumma\\'
# filename = 'BasinRunoff_1dRichards.nc'
#
# Text = Plotting(filepath)
# Text_Info = Text.Open_netcdf()
# Attribute = dict(Text_Info.attrs)
# Dimensions = Text_Info.dims
# Data_variables = Text_Info.data_vars
#
# variable_1D = [['basin__SurfaceRunoff','2'],['basin__ColumnOutflow','3'], ['basin__AquiferStorage','4'],
# 			   ['basin__AquiferRecharge', '5'], ['basin__AquiferBaseflow', '6'],['basin__AquiferTranspire','7'],
# 			   ['averageInstantRunoff', '8'], ['averageRoutedRunoff', '9']]
#
# variable_1D_hru = [['pptrate','0'],['airtemp','1'], ['nSnow','10'], ['nSoil','11'],
#                    ['nLayers','12'],['midSoilStartIndex','13'], ['midTotoStartIndex','14'], ['ifcSoilStartIndex','15'],
#                    ['ifcTotoStartIndex','16'],['scalarSWE','17'],['scalarSurfaceTemp','23'],['scalarSenHeatTotal','27'],
#                    ['scalarLatHeatTotal','28'],['scalarSnowSublimation','29'],['scalarThroughfallSnow','30'],
#                    ['scalarThroughfallRain','31'],['scalarRainPlusMelt','32'],['scalarInfiltration','33'],
#                    ['scalarExfiltration','34'],['scalarSurfaceRunoff','35']]
#
# variable_1D_layer = [['mLayerTemp','18'],['mLayerVolFracIce','19'], ['mLayerVolFracLiq','20'], ['mLayerVolFracWat','21'],
#                    ['mLayerMatricHead','22'],['mLayerDepth','24'], ['mLayerHeight','25'], ['iLayerHeight','26'],
#                    ['iLayerLiqFluxSoil','36'],['mLayerLiqFluxSoil','37']]
#
# plot_1D = Text.Plot_1D(Text_Info, 8)
# plt.show()
#
# plot_1D_hru = Text.Plot_1D_hru(Text_Info, 0, 17)
# plt.show()
#
# plot_1D_layer = Text.Plot_1D_layer(Text_Info, 0, 21, 14)
# plt.show()
#
# plot_2D = Text.Plot_2D(Text_Info, 0, 21, 25, 14)
# plt.show()