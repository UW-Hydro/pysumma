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
          'numpy',
          'xarray>0.10.9',
          'matplotlib',
          'geopandas',
          'shapely',
          'seaborn'
          ],
      include_package_data=True,
      test_suite='pysumma.tests')
