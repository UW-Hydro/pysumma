import seaborn as sns
import xarray as xr
import matplotlib.pyplot as plt


class Plotting:
	colors = ["windows blue", "amber", "greyish", "faded green", "dusty purple"]
	sns.set_palette(sns.xkcd_palette(colors))

	def __init__(self, filepath):
		self.filepath = filepath
		self.ds = self.open_netcdf()

	def open_netcdf(self):
		filepath = self.filepath
		return xr.open_dataset(filepath)

	def plot_1d(self, variable):
		ax = self.ds[variable].plot()
		plt.ylabel('{} ({})'.format(self.ds[variable].long_name, self.ds[variable].units))
		plt.show()
		return ax

	def plot_1d_hru(self, hru_num, variable_num):
		ax = self.ds[variable_num][:,hru_num].plot()
		plt.ylabel('{} ({})'.format(self.ds[variable_num].long_name, self.ds[variable_num].units))
		plt.show()
		return ax

	def plot_1d_layer(self, variable):
		ax = self.ds[variable].plot()
		plt.show()
		return ax