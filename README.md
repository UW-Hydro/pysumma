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
 - Automate model calibration or sensitivity analysis (Future work)

## How to run pySUMMA on HydroShare 
 (Link YouTube: https://www.youtube.com/watch?v=pL-LNd474Tw)
 1) log in HydoShare(https://www.hydroshare.org)
 2) Start CUAHSI JupyterHub from APPS menu on HydroShare(https://www.hydroshare.org/apps/)
 3) Open "Welcome.ipynb" to download pySUMMA resources from HydroShare
  - run the code "1.How to connect with HydroShare"
  - change the code from "resid = os.environ['HS_RES_ID']" to "resid = 'c1bb4a12bff44bf08c5958cba7947348'". 
 4) You can see the list of Jupyter Notebooks and click one of Jupyter Notebook.
 5) Run one of Jupyter Notebooks.

### Examples of manipulating and running pySUMMA :

Refereed paper : Clark, M. P., B. Nijssen, J. D. Lundquist, D. Kavetski, D. E. Rupp, R. A. Woods, 
J. E. Freer, E. D. Gutmann, A. W. Wood, D. J. Gochis, R. M. Rasmussen, D. G. Tarboton, V. Mahat, 
G. N. Flerchinger, D. G. Marks, 2015b: A unified approach for process-based hydrologic modeling: 
Part 2. Model implementation and case studies. Water Resources Research, 
[doi:10.1002/2015WR017200](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1002/2015WR017200).

#### HydroShare resources 
**(Composite Resource)** [Jupyter Notebooks to demonstrate SUMMA Model at Reynolds Mountain East on HydroShare](https://www.hydroshare.org/resource/c1bb4a12bff44bf08c5958cba7947348/) 

**(Composite Resource)** [Procedure and Supplementary documents Collaborative hydrologic modeling on HydroShare](https://www.hydroshare.org/resource/184eea3d3412418a886db87ffdb510b6/)

**(Model Program)** [SUMMA 2.0.0 Sopron version (lubuntu-16.10)](https://www.hydroshare.org/resource/a5dbd5b198c9468387f59f3fefc11e22/)

**(Model Program)** [SUMMA 2.0.0 Sopron version (lubuntu-16.04.4)](https://www.hydroshare.org/resource/041671fbc8a544cd8a979af6c2227f92/)

**(Model Instance)** [Sensitivity to Stomatal Resistance Parameterization of SUMMA Model in Aspen stand at Reynolds Mountain East)](https://www.hydroshare.org/resource/e1a73bc4e7c34166895ff20ae53371f5/)

**(Model Instance)** [The Impact of Root Distributions Parameters of SUMMA Model in Aspen stand at Reynolds Mountain East)](https://www.hydroshare.org/resource/eed6f3faedad4c17992bb361bd492caa/)

**(Model Instance)** [The Impact of Lateral Flow Parameterizations on ET of SUMMA Model at Reynolds Mountain East)](https://www.hydroshare.org/resource/11d471b6096d4eaa81068256d281a919/)

**(Model Instance)** [The Impact of Lateral Flow Parameterizations on Runoff of SUMMA Model at Reynolds Mountain East)](https://www.hydroshare.org/resource/5d20a87ecc5b495097e073e4d5f58d0c/)

**(Model Instance)** [The Impact of the canopy shortwave radiation parameterizations of SUMMA Model at Reynolds Mountain East)](https://www.hydroshare.org/resource/0c4fd861a9694b2f9fcdf19eb33a6b54/)

**(Model Instance)** [The Impact of LAI parameter on the below canopy shortwave radiation of SUMMA Model at Reynolds Mountain East)](https://www.hydroshare.org/resource/2bedc3b88f3547d5b9b0ade7248dfdd5/)

**(Model Instance)** [The Impact of the canopy wind parameter for the exponential wind profile of SUMMA Model at Reynolds Mountain East)](https://www.hydroshare.org/resource/4064a7b014094f50aa63730e4a3ff976/)

**(Collection Resource)** [Test Cases of SUMMA modeling that include model instances and Jupyter notebooks for SUMMA 2nd Paper(2015))](https://www.hydroshare.org/resource/1b7a9af74daa4a449190f922b5db366e/)

## How to run pySUMMA locally 
 
### Installation and Usage

#### pySUMMA requires Python 3.6 and following packages :

 - xarray 0.10.7 : N-D labeled arrays and datasets in python
 - numpy 1.16.1 : the fundamental package for scientific computing with Python
 - matplotlib 3.0.2 : a Python 2D plotting library 
 - seaborn 0.9.0 : statistical data visualization 
 - jupyterthemes 0.20.0 : select and install a Jupyter notebook theme
 - hs-restclient 1.3.3 : HydroShare REST API python client library
 - ipyleaflet 0.9.2 : A jupyter widget for dynamic Leaflet maps 
 - Linux Environment (VirtualBox 5.2.8)
   - [lubuntu-16.10 executable](https://www.hydroshare.org/resource/a5dbd5b198c9468387f59f3fefc11e22/)
   - [lubuntu-16.04.4 executable](https://www.hydroshare.org/resource/041671fbc8a544cd8a979af6c2227f92/)        

### Download and Install pySUMMA:

**1.)**  Download pySUMMA
```python
~/Downloads$ git clone https://github.com/uva-hydroinformatics/pysumma.git
```
        
**2.)**  change directory into pysumma folder same level with setup.py.
```python
~/Downloads/pysumma$ pip install .
```

#### The UML of pySUMMA
![Image of UML](UML.jpg)

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
