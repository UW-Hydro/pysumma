What's new
===========

.. _whats_new_develop

Develop version
---------------

Enhancements
~~~~~~~~~~~~
- Plot soil made default in ``psp.layers``
- Make 'local' the default run option in ``Simulation`` based classes
- Add ``_repr_html_`` to ``OptionContainer`` classes to make viewing easier in notebooks
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
- Removes duplicate scripts for water and energy balance plots
- Fixes a typo in merging the output spatially distributed runs which omitted GRU based variables
- Fixes a bug in the Ostrich run script that assumes an ``hruIndex`` variable in the parameter dataset.
- Provides an up to date ``var_lookup.f90`` which contains the correct variable definitions for newer versions of SUMMA
