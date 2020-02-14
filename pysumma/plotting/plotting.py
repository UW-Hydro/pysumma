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

	def ts_plot(self, variable, hru_num=0):
		x = self.ds.variables['time']
		y = self.ds.variables[variable][:,hru_num]
		name = self.ds.variables[variable].attrs['long_name']
		plt.figure(figsize=(15, 5))
		plt.plot(x, y, color='grey', linestyle='solid', markersize=0)

		# Get the current axis of the plot and
		# set the x and y-axis labels
		ax = plt.gca()
		ax.set_ylabel(y.attrs['long_name'] + '(' + y.attrs['units'] + ')')
		ax.set_xlabel('Date')
		ax.grid(True)

		# Set the title
		hru_num = hru_num + 1
		ax.set_title("SUMMA %s Plot (hru=%s))" % (name, hru_num))

	def ts_plot_layer(self, variable, layer_num, hru_num=0):
		x = self.ds.variables['time']
		y = self.ds.variables[variable][:,hru_num]
		name = self.ds.variables[variable].attrs['long_name']

		layer_variable = np.array(y)
		col = layer_num-1
		time = self.ds.dims['time']
		time_arr = np.arange(time)
		y1 = layer_variable[time_arr, col]

		plt.figure(figsize=(15, 5))
		plt.plot(x, y1, color='grey', linestyle='solid', markersize=0)

		ax = plt.gca()
		ax.set_ylabel(y.attrs['long_name'] + '(' + y.attrs['units'] + ')')
		ax.set_xlabel('Date')
		ax.grid(True)

		# Set the title
		hru_num = hru_num + 1
		layer_num = layer_num + 1
		ax.set_title("SUMMA %s Plot (layer_num=%s)(hru=%s))"  % (name, layer_num, hru_num))


	def heatmap_plot(self, variable, layer_name, hru_num=0):
		Plotting.heatmap_plot_selection(self, variable, layer_name, -1, -1, hru_num)


	def heatmap_plot_selection(self, variable, layer_name, start_layer, end_layer, hru_num=1, ):
		time_dims = self.ds.dims['time']
		layer_dims = self.ds.dims[layer_name]
		time = self.ds.variables['time'].data
		test = self.ds.variables[variable].data[:,:,hru_num]
		y = test.reshape(time_dims, 1, layer_dims)
		m, n, r = y.shape
		out_arr = np.column_stack((np.repeat(np.arange(m), n), y.reshape(m * n, -1)))
		out_df = pd.DataFrame(out_arr, columns=list(range(0, layer_dims + 1)), index=time)
		out_df = out_df[list(range(1, layer_dims + 1))]
		out_df.replace(-9999.0, np.nan, inplace=True)
		out_df_dropped = out_df.dropna(how="all", axis="columns")
		out_df_dropped = out_df_dropped[list(range(1, len(out_df_dropped.columns)))]
		if start_layer is not -1:
			out_df_dropped = out_df_dropped[list(range(start_layer, min(len(out_df_dropped.columns), end_layer + 1)))]
		plt.figure(figsize=(15, 5))
		ax = plt.gca()
		ax.set_ylabel('Layer')
		sns.heatmap(out_df_dropped.T)