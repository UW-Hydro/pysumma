from setuptools import setup, find_packages

setup(name='pysumma',
      version='0.0.3',
      description='an Object-Oriented Python wrapper for SUMMA model',
      url='https://github.com/uva-hydroinformatics/pysumma.git',
      author='YoungDon Choi',
      author_email='yc5ef@virginia.edu',
      license='BSD-3-Clause',
      packages=find_packages(),
      install_requires=[
          'numpy',
          'xarray>=0.10.9',
          'matplotlib',
          'pandas',
          'geopandas',
          'shapely',
          'seaborn',
          'hs_restclient==1.3.4',
          'distributed',
          'fiona',
          'netcdf4'
          ],
      include_package_data=True,
      test_suite='pysumma.tests')
