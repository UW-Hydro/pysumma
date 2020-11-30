import versioneer
from setuptools import setup, find_packages


setup(name='pysumma',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='A python wrapper for SUMMA',
      url='https://github.com/UW-Hydro/pysumma.git',
      author='YoungDon Choi, Andrew Bennett',
      author_email='choiyd1115@gmail.com, andrbenn@uw.edu',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'xarray>=0.15.0',
          'pandas',
          'netcdf4>=1.2.5',
          'numpy>=1.11.2',
          'dask',
          'distributed',
          'toolz',
          'pytest',
          'matplotlib',
          'pandas',
          'hs_restclient'
          ],
       extras_require={'plotting': [
          'geopandas',
          'fiona',
          'cartopy',
          'shapely',
          'seaborn'
          ],},
      include_package_data=True,
      test_suite='pysumma.tests')
