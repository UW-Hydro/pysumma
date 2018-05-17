from setuptools import setup, find_packages

setup(name='pysumma',
      version = '0.1',
      description = 'an Object-Oriented Python wrapper for SUMMA model',
      url = 'https://github.com/UW-Hydro/pysumma',
      author = 'YoungDon Choi',
      author_email = 'yc5ef@virginia.edu',
      license = 'BSD-3-Clause',
<<<<<<< HEAD
      packages=find_packages(),
=======
      packages=['pysumma'],
      install_requires=[
          'scipy',
          'xarray',
          'matplotlib'
          ],
      include_package_data=True,
      dat_files=[('pysumma', 'pysumma/var_lookup.f90')],
>>>>>>> 6391d7096f369b2e55c9631b1022a2713860b286
      test_suite = 'pysumma.tests')
