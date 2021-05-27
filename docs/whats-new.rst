What's new
===========

.. _whats_new_develop

Develop version
---------------

Enhancements
~~~~~~~~~~~~
- Improve usability of Ostrich calibration by adding validation of options before runtime
- Improve usability of Ostrich calibration by allowing testing of the runscript
- Improve usability of Ostrich calibration by adding helper functions to read in metrics and parameter logs
- Improve usability of Ostrich calibration by attempting to infer the python executable even when running inside of an environment.
- Filter for multiple output files when calibrating.
- Convert path for observed data to absolute path implicitly when calibrating.
- Allow for user specified cost functions during calibration.
- Added a helper method to the Simulation object which makes it wasy to change/modify forcing datasets

Bug fixes
~~~~~~~~~
- Fixes a bug in the Ostrich run script that assumes an `hruIndex` variable in the parameter dataset.
- Provides an up to date `var_lookup.f90` which contains the correct variable definitions for newer versions of SUMMA
