pysumma is a Python wrapper for manipulating, running, managing, and analyzing
of SUMMA (Structure for Unifying Multiple Modeling Alternatives)
* [SUMMA web site at UCAR ](https://www.rap.ucar.edu/projects/summa)

pysumma provides methods for:
 - Running SUMMA
 - Modifying SUMMA input files
 - Automatically parallelizing distributed and sensitivity analysis type experiments
 - Visualizing output

# Installation
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
