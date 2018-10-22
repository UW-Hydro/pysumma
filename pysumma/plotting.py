import seaborn as sns
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Plotting:

	def __init__(self, filepath):
		self.filepath = filepath
		self.ds = self.open_netcdf()

	def open_netcdf(self):
		filepath = self.filepath
		output = xr.open_dataset(filepath)
		return output

	def ts_plot(self, variable, hru_num):
		x = self.ds.variables['time']
		y = self.ds.variables[variable]
		plt.xlabel('time')
		y_label = y.attrs['long_name'] + '(' + y.attrs['units'] + ')'
		plt.ylabel(y_label)
		plt.title('SUMMA Plot' '  ' + '(' + 'hru=%s' ')' % hru_num)
		plt.plot(x, y, label=variable)
		plt.legend(loc='best')

	def ts_plot_layer(self, variable, hru_num, layer_num):
		x = self.ds.variables['time']
		y = self.ds.variables[variable]
		layer_variable = np.array(y)
		col = layer_num-1
		time = self.ds.dims['time']
		time_arr = np.arange(time)
		y1 = layer_variable[time_arr, col]
		plt.xlabel('time')
		y_label = y.attrs['long_name'] + '(' + y.attrs['units'] + ')'
		plt.ylabel(y_label)
		plt.title('SUMMA Plot' '  ' + '(' + 'hru=%s' ')' % hru_num)
		plt.plot(x, y1, label=variable)
		plt.legend(loc='best')

	def heatmap_plot(self, variable, hru_num, layer_name):
		time_dims = self.ds.dims['time']
		layer_dims = self.ds.dims[layer_name]
		time = self.ds.variables['time'].data
		test = self.ds.variables[variable].data
		y = test.reshape(time_dims, hru_num, layer_dims)
		m, n, r = y.shape
		out_arr = np.column_stack((np.repeat(np.arange(m), n), y.reshape(m * n, -1)))
		out_df = pd.DataFrame(out_arr, columns=list(range(0, layer_dims+1)), index=time)
		out_df = out_df[list(range(1,layer_dims+1))]
		sns.heatmap(out_df.T)


	def heatmap_plot_selection(self, variable, hru_num, layer_name, start_layer, end_layer):
		time_dims = self.ds.dims['time']
		layer_dims = self.ds.dims[layer_name]
		time = self.ds.variables['time'].data
		test = self.ds.variables[variable].data
		y = test.reshape(time_dims, hru_num, layer_dims)
		m, n, r = y.shape
		out_arr = np.column_stack((np.repeat(np.arange(m), n), y.reshape(m * n, -1)))
		out_df = pd.DataFrame(out_arr, columns=list(range(0, layer_dims+1)), index=time)
		out_df = out_df[list(range(1, layer_dims + 1))]
		out = out_df[list(range(start_layer, end_layer+1))]
		sns.heatmap(out.T)