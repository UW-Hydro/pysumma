from setuptools import setup, find_packages

setup(name='pysumma',
      version='2.0.0',
      description='A python wrapper for SUMMA',
      url='https://github.com/UW-Hydro/pysumma.git',
      author='YoungDon Choi, Andrew Bennett',
      author_email='choiyd1115@gmail.com, andrbenn@uw.edu',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'numpy',
          'xarray>0.10.9',
          'matplotlib',
          'geopandas',
          'shapely',
          'seaborn',
          'pandas>=0.25',
          'distributed',
          'cartopy',
          'fiona',
          'netcdf4'
          ],
      include_package_data=True,
      test_suite='pysumma.tests')
