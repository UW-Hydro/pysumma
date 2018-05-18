from setuptools import setup, find_packages

setup(name='pysumma',
      version = '0.1',
      description = 'an Object-Oriented Python wrapper for SUMMA model',
      url = 'https://github.com/uva-hydroinformatics/pysumma',
      author = 'YoungDon Choi',
      author_email = 'yc5ef@virginia.edu',
      license = 'BSD-3-Clause',
      packages=find_packages(),
      install_requires=[
          'scipy',
          'xarray',
          'matplotlib'
          ],
      include_package_data=True,
      dat_files=[('pysumma', 'pysumma/var_lookup.f90')],
      test_suite = 'pysumma.tests')
