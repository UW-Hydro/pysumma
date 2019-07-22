from setuptools import setup, find_packages

setup(name='pysumma',
      version='0.0.1',
      description='an Object-Oriented Python wrapper for SUMMA model',
      url='https://github.com/uva-hydroinformatics/pysumma.git',
      author='YoungDon Choi',
      author_email='yc5ef@virginia.edu',
      license='BSD-3-Clause',
      packages=find_packages(),
      install_requires=[
          'numpy==1.16.1',
          'xarray==0.10.7',
          'matplotlib==2.2.4',
          'ipyleaflet==0.9.2',
          'jupyterthemes==0.20.0',
          'geopandas==0.4.0',
          'pandas==0.24.1',
          'seaborn==0.9.0',
          'netCDF4==1.4.2',
          'hs_restclient==1.3.3'
          ],
      include_package_data=True,
      dat_files=[('pysumma', 'pysumma/var_lookup.f90')],
      test_suite='pysumma.tests')
