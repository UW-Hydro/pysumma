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

	def plot_1d(self, ds, variable_num):
		var_dict= dict(ds.data_vars)
		var_list_key = list(var_dict.keys())[variable_num]
		plot = ds[var_list_key].plot()
		plt.ylabel('{} ({})'.format(ds[var_list_key].long_name, ds[var_list_key].units))
		plt.show()
		return plt.show()

	def plot_1d_hru(self, ds, hru_num, variable_num):
		var_dict= dict(ds.data_vars)
		var_list_key = list(var_dict.keys())[variable_num]
		plot = ds[var_list_key][:,hru_num].plot()
		plt.ylabel('{} ({})'.format(ds[var_list_key].long_name, ds[var_list_key].units))
		plt.show()
		return plt.show()

	def plot_1d_layer(self, ds, hru_num, variable_num_Y, start_index_X, timestep):
		#='mLayerVolFracWat', start_index='midTotoStartIndex'
		var_dict= dict(ds.data_vars)
		var_list_key_Y = list(var_dict.keys())[variable_num_Y]
		plot = ds[var_list_key_Y][:,hru_num].plot()
		# extract the number of layers associated with the first timestep
		layers = ds.nLayers[timestep].values[0]
		var_list_key_X = list(var_dict.keys())[start_index_X]
		# - 1 since the SUMMA indices are 1-based and python indices are 0-based
		start_index = ds[var_list_key_X][timestep].values[0] - 1
		endIndex = start_index + layers
		ds[var_list_key_Y][start_index:endIndex, 0].plot(label='t = {: 2d}'.format(timestep))
		plt.ylabel('{} ({})'.format(ds[var_list_key_Y].long_name, ds[var_list_key_Y].units))
		plt.show()
		return plt.show()

	def plot_2d(self, ds, hru_num, variable_num_Y, variable_num_X, midto, timesteps):
		var_dict= dict(ds.data_vars)
		var_list_key_Y = list(var_dict.keys())[variable_num_Y]
		var_list_key_X = list(var_dict.keys())[variable_num_X]

		for timestep in timesteps:
			# extract the number of layers associated with the first timestep
			layers = ds.nLayers[timestep].values[0]  
			var_list_key = list(var_dict.keys())[midto]
			start_index = ds[var_list_key][timestep].values[0] - 1  # - 1 since the SUMMA indices are 1-based and python indices are 0-based
			endIndex = start_index + layers
			plot = plt.plot(ds[var_list_key_X][start_index:endIndex],
							ds[var_list_key_Y][start_index:endIndex,0],
							label='t = {: 2d}'.format(timestep+1))
		plt.ylabel('{} ({})'.format(ds[var_list_key_Y].long_name, ds[var_list_key_Y].units))
		plt.xlabel('{} ({})'.format(ds[var_list_key_X].long_name, ds[var_list_key_X].units))
		plt.legend(loc=3)
		plt.show()
		return plt.show()
