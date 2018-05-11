# pySUMMA                                        

The pySUMMA is an Object-Oriented Python wrapper for the manipulation, display and analysis of 
SUMMA model (Structure for Unifying Multiple Modeling Alternatives)

* [SUMMA web site at UCAR ](https://www.rap.ucar.edu/projects/summa)

## The pySUMMA is intended to provide

 - Get and set model parameters and method (fileManager and Decision file) 
 - Run SUMMA Model 
 - Visualize netcdf of SUMMA outputs
 - Operate pySUMMA with jupyter notebook environment 
 - Interact Hydorshare to download SUMMA TestCases and post the output of SUMMA 
 - Create UserInterface of Decision and filemanager file for User (in progress)
 - Automate model calibration or sensitivity analysis (Future work)


## Installation and Usage

#### pySUMMA requires Python 3.6 and following packages :

 - xarray 0.10.0 : N-D labeled arrays and datasets in python
 - numpy 1.13.3 : the fundamental package for scientific computing with Python
 - matplotlib 2.1.1 : a Python 2D plotting library 
 - seaborn 0.8.1 : statistical data visualization 
 - jupyterthemes 0.18.3 : select and install a Jupyter notebook theme
 - hs-restclient 1.2.12 : HydroShare REST API python client library
 - ipyleaflet 0.7.1 : A jupyter widget for dynamic Leaflet maps 
 - Linux Environment (VirtualBox 5.2.8)
   - [lubuntu-16.10 executable](https://www.hydroshare.org/resource/a5dbd5b198c9468387f59f3fefc11e22/)
   - [lubuntu-16.04.4 executable](https://www.hydroshare.org/resource/041671fbc8a544cd8a979af6c2227f92/)        

## Download and Install pySUMMA:

**1.)**  Download pySUMMA
```python
~/Downloads$ git clone https://github.com/uva-hydroinformatics/pysumma.git
```
        
**2.)**  change directory into pysumma folder same level with setup.py.
```python
~/Downloads/pysumma$ pip install .
```

## Examples of unit test :

**a unit test using unittest library**  

```python
~/Downloads/pysumma$ python setup.py test
```
## Examples of manipulating and running pySUMMA :

Refereed paper : Clark, M. P., B. Nijssen, J. D. Lundquist, D. Kavetski, D. E. Rupp, R. A. Woods, 
J. E. Freer, E. D. Gutmann, A. W. Wood, D. J. Gochis, R. M. Rasmussen, D. G. Tarboton, V. Mahat, 
G. N. Flerchinger, D. G. Marks, 2015b: A unified approach for process-based hydrologic modeling: 
Part 2. Model implementation and case studies. Water Resources Research, 
[doi:10.1002/2015WR017200](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1002/2015WR017200).

**(1)** [Modeling the Impact of Stomatal Resistance Parameterizations on Total Evapotranspiration 
         in the Reynolds Mountain East catchment using pySUMMA](https://github.com/uva-hydroinformatics/pysumma/blob/master/sopron_2018_notebooks/pySUMMA_Demo_Example_Fig7_Using_TestCase_from_Hydroshare.ipynb) 

**(2)** [Modeling the Impact of Root Distributions Parameterizations on Total Evapotranspiration 
         in the Reynolds Mountain East catchment using pySUMMA](https://github.com/uva-hydroinformatics/pysumma/blob/master/sopron_2018_notebooks/pySUMMA_Demo_Example_Fig8_left_Using_TestCase_from_Hydroshare.ipynb)

**(3)** [Modeling the Impact of Lateral Flow Parameterizations on Total Evapotranspiration in the 
         Reynolds Mountain East catchment using pySUMMA](https://github.com/uva-hydroinformatics/pysumma/blob/master/sopron_2018_notebooks/pySUMMA_Demo_Example_Fig8_right_Using_TestCase_from_Hydroshare.ipynb)

**(4)** [Modeling the Impact of Lateral Flow Parameterizations on Basin Wide Runoff in the Reynolds 
         Mountain East catchment using pySUMMA](https://github.com/uva-hydroinformatics/pysumma/blob/master/sopron_2018_notebooks/pySUMMA_Demo_Example_Fig9_Using_TestCase_from_Hydroshare.ipynb)

**(5)** [pySUMMA General Plot example](https://github.com/uva-hydroinformatics/pysumma/blob/master/sopron_2018_notebooks/pySUMMA_General_Plot_Example.ipynb)

#### The UML of pySUMMA
![Image of UML](https://github.com/uva-hydroinformatics/pysumma/blob/master/pySUMMA_UML.jpg)

## Reference of SUMMA

 - [Document](http://summa.readthedocs.io/en/latest/) : SUMMA documentation is available online and remains a work in progress.
 - [Source Code](https://github.com/NCAR/summa) : NCAR github
 
## Bugs
  Our issue tracker is at https://github.com/uva-hydroinformatics/pysumma/issues.
  Please report any bugs that you find.  Or, even better, fork the repository on
  GitHub and create a pull request.  All changes are welcome, big or small, and we
  will help you make the pull request if you are new to git
  (just ask on the issue).

## License
  Distributed with a MIT license; see LICENSE.txt::

  Copyright (C) 2017 pySUMMA Developers
  YoungDon Choi <yc5ef@virginia.edu>
