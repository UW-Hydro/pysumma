#!/usr/bin/env python

try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(name='summa_plot',
      version='0.0.1',
      description='SUMMA Plotting Library',
      url='https://github.com/arbennett/summa_plot',
      author='Andrew Bennett',
      author_email='bennett.andr@gmail.com',
      packages=['summa_plot'],
      install_requires=['xarray', 'geopandas'],
      keywords=[],
      tests_require=['pytest'],)
