from setuptools import setup, find_packages

setup(name='pysumma',
      version = '0.1',
      description = 'This is pySUMMA',
      url = 'https://github.com/DavidChoi76/pysumma_alpha',
      author = 'YoungDon Choi',
      author_email = 'yc5ef@virginia.edu',
      license = 'MIT',
      packages=['pysumma'],
      test_suite = 'tests')
#      setup_requires=['pytest-runner', 'xarray'],
#      test_suite='pysumma.tests.Decisions_suite')
