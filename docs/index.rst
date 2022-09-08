.. pysumma documentation master file
.. _index:

pysumma
=======
pysumma is a Python wrapper for manipulating, running, managing, and analyzing
of SUMMA (Structure for Unifying Multiple Modeling Alternatives)

 `SUMMA web site at UCAR <https://www.rap.ucar.edu/projects/summa>`_

pysumma provides methods for:
 - Running SUMMA
 - Modifying SUMMA input files
 - Automatically parallelizing distributed and sensitivity analysis type experiments
 - Visualizing output

Installation
============

``pysumma`` can be installed from either ``conda`` or ``pip``. Installation using ``conda`` is preferred, because
it will also install a compatible version of SUMMA.

To install via ``conda`` use:

::

    conda install -c conda-forge pysumma

To install via ``pip`` use:

::

    pip install pysumma


Dependencies
------------

A conda environment is available for management of pysumma's dependencies.
You can create your own environment from this file by running:

::

    conda env create -f environment.yml

Then, you can activate this environment with ``conda activate pysumma``.
Before installing pysumma into this environment you may also wish to install it as a kernel in your Jupyter environments.
This can be accomplished by running:

::

    python -m ipykernel install --user --name=pysumma

With this environment active you can install pysumma this environment with the instructions below.

Installing pysumma from source
------------------------------

Installing pysumma from source can be useful for developing new features. This can be accomplished by
running:

::

    git clone https://github.com/UW-Hydro/pysumma.git
    cd pysumma
    python setup.py develop

Additional SUMMA References
===========================
 - `Documentation <http://summa.readthedocs.io/en/latest/>`_ : SUMMA documentation is available online and remains a work in progress.
 - `Source Code <https://github.com/NCAR/summa>`_ : NCAR github

Bugs
====
  Our issue tracker is at https://github.com/UW-Hydro/pysumma/issues.
  Please report any bugs that you find.  Or, even better, fork the repository on
  GitHub and create a pull request.  All changes are welcome, big or small, and we
  will help you make the pull request if you are new to git
  (just ask on the issue).

Sitemap
=======
.. toctree::
    :maxdepth: 3

    configuration
    tutorials
    plotting
    api
