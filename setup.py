from setuptools import setup, find_packages

setup(name='pysumma',
      version = '0.1',
      description = 'This is pySUMMA',
      url = 'https://github.com/UW-Hydro/pysumma',
      author = 'YoungDon Choi',
      author_email = 'yc5ef@virginia.edu',
      license = 'BSD-3-Clause',
      packages=['pysumma'],
      install_requires=[
          'scipy',
          'xarray',
          'matplotlib'
          ],
      include_package_data=True,
      dat_files=[('pysumma', 'pysumma/var_lookup.f90')],
      test_suite = 'pysumma.tests')
