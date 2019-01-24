from setuptools import setup, find_packages

setup(name='pysumma',
      version='0.1',
      description='an Object-Oriented Python wrapper for SUMMA model',
      url='https://github.com/DavidChoi76/pysumma.git',
      author='YoungDon Choi',
      author_email='yc5ef@virginia.edu',
      license='BSD-3-Clause',
      packages=find_packages(),
      install_requires=[
          'numpy==1.13.3',
          'xarray==0.10.0',
          'matplotlib==2.1.1',
          'ipyleaflet',
          'jupyterthemes==0.18.3',
          'geopandas',
          'cartopy',
          'shapely',
          'seaborn==0.8.1'
          ],
      include_package_data=True,
      test_suite='pysumma.tests')
