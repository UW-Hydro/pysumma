from setuptools import setup, find_packages

setup(name='pysumma',
      version='2.0.0',
      description='an Object-Oriented Python wrapper for SUMMA model',
      url='https://github.com/uva-hydroinformatics/pysumma.git',
      author='YoungDon Choi',
      author_email='choiyd1115@gmail.com',
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
          'fiona',
          'netcdf4'
          ],
      include_package_data=True,
      test_suite='pysumma.tests')
