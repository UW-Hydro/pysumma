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
          'numpy==1.16.4',
          'xarray==0.12.3',
          'matplotlib==3.1.0',
          'pandas==0.24.2',
          'geopandas==0.5.1',
          'shapely',
          'seaborn==0.9.0',
          'cartopy==0.17.0',
          'jupyterthemes==0.20.0',
          'ipyleaflet==0.11.1',
          'hs_restclient==1.3.4',
          'distributed==2.1.0',
          'bokeh==1.2.0',
          'fiona==1.8.6',
          'netcdf4'
          ],
      include_package_data=True,
      test_suite='pysumma.tests')
