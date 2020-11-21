# pysumma

| pysumma Links & Badges              |                                                                             |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pysumma Documentation      | [![Documentation Status](http://readthedocs.org/projects/pysumma/badge/?version=develop)](http://pysumma.readthedocs.io/en/develop/?badge=develop) |
| Travis-CI Build           | [![Build Status](https://travis-ci.org/UW-pysumma/pysumma.png)](https://travis-ci.org/UW-Hydro/pysumma) |

pysumma is a Python wrapper for manipulating, running, managing, and analyzing
of SUMMA (Structure for Unifying Multiple Modeling Alternatives)
* [SUMMA web site at UCAR ](https://www.rap.ucar.edu/projects/summa)

pysumma provides methods for:
 - Running SUMMA
 - Modifying SUMMA input files
 - Automatically parallelizing distributed and sensitivity analysis type experiments
 - Calibration via OSTRICH
 - Visualizing output

# Installation

## Dependencies
A conda environment is available for management of pysumma's dependencies.
You can create your own environment from this file by running:
```
conda env create -f environment.yml
```

Then, you can activate this environment with `conda activate pysumma`.
Before installing pysumma into this environment you may also wish to install it as a kernel in your Jupyter environments.
This can be accomplished by running:

```
python -m ipykernel install --user --name=pysumma
```

With this environment active you can install pysumma this environment with the instructions below.

## Installing pysumma
Currently we only support building pysumma from source. This can be accomplished by
running:
```
git clone https://github.com/UW-Hydro/pysumma.git
cd pysumma
python setup.py install
```

If you plan on helping to develop pysumma you may wish to use the following to install
```
git clone https://github.com/UW-Hydro/pysumma.git
cd pysumma
python setup.py develop
```

# Additional SUMMA References
 - [Document](http://summa.readthedocs.io/en/latest/) : SUMMA documentation is available online and remains a work in progress.
 - [Source Code](https://github.com/NCAR/summa) : NCAR github

# Bugs
  Our issue tracker is at https://github.com/UW-Hydro/pysumma/issues.
  Please report any bugs that you find.  Or, even better, fork the repository on
  GitHub and create a pull request.  All changes are welcome, big or small, and we
  will help you make the pull request if you are new to git
  (just ask on the issue).

# How to run pySUMMA on HydroShare
 (Link YouTube: https://www.youtube.com/watch?v=pL-LNd474Tw)
 1) log in HydoShare(https://www.hydroshare.org)
 2) Start CUAHSI JupyterHub from APPS menu on HydroShare(https://www.hydroshare.org/apps/)
 3) Open "Welcome.ipynb" to download pySUMMA resources from HydroShare
  - run the code "1.How to connect with HydroShare"
  - change the code from "resid = os.environ['HS_RES_ID']" to "resid = 'c1bb4a12bff44bf08c5958cba7947348'".
 4) You can see the list of Jupyter Notebooks and click one of Jupyter Notebook.
 5) Run one of Jupyter Notebooks.
