# pySUMMA

**an Object-Oriented Python wrapper for SUMMA model (Structure for Unifying Multiple Modeling Alternatives)**

## Overview

**pySUMMA is an Object-Oriented Python wrapper for the manipulation, display and
  analysis of SUMMA model**


## Goals

**pySUMMA is intended to provide**

 - Get and set model parameters(Decision and fileManager file) (in progress)
 - Run SUMMA Model (in progress)
 - Visualize netCDF outputs (in progress)
 - Automate model calibration or sensitivity studies (Future work)
 - Operate pysumma with jupyter notebook environment in Hydroshare (Future work)

## Installation and Usage

**pySUMMA requires Python 3.6 and following packages : **

 - seaborn 0.8.1 : statistical data visualization
 - xarray 0.10.0 : N-D labeled arrays and datasets in python
 - numpy 1.13.3 : the fundamental package for scientific computing with Python
 - matplotlib 2.1.1 : a Python 2D plotting library 
 - Cartopy 0.15.1 : a library providing cartographic tools.
 - Shapely 1.6.3 : a package for creation, manipulation, and analysis of planar geometry    
                   objects based on GEOS.
 - jupyterthemes 0.18.3
 - pyproj 1.9.5.1 : an interface to the PROJ.4 library for cartographic transformations.
 - GDAL 2.2.3 : (Geospatial Data Abstraction Library), a translator library for raster  
           geospatial data formats.
 - Fiona 1.7.11(required GDAL) : OGR's neater API
 - geopandas 0.3.0 (required numpy, pandas, shapely, fiona, six, pyproj) 
 - Linux Environment (VirtualBox 5.1.32, lubuntu-16-10)              

## Download pysumma_alpha and summa_testcase :

**1.)**  open VirtualBox

**2.)**  open Terminal

**3.)**  change directory to Downloads folder and download pysumma_alpha
```python
~/Downloads$ git clone http://github.com/DavidChoi76/pysumma_alpha
```
**4.)**  open web browser(https://ral.ucar.edu/projects/summa) and download summa_testcase(summaTestCases_2x.tar.gz)       
           
**5.)**  change directory to '~/Downloads/summaTestCases_2x and installTestCases
```python
~/Downloads/summaTestCases_2x$ ./installTestCases_local.sh
```

## Examples of installation :

**installation of pysumma**  
**1.)**  change directory into pysumma folder same level with setup.py.
```python
~/Downloads/pysumma_alpha/pysumma$ pip install .
```

## Examples of unit test :

**a unit test using unittest library**  

```python
~/Downloads/pysumma_alpha/pysumma$ python setup.py test
```

## Examples of manipulating summa model :

**(1) manipulating file Manager file.**  

**1.)**  import Simulation Module
```python
>>> from pysumma.Simulation import Simulation
```
**2.)**  read file Manager text file and create S attribute
```python
>>> S = Simulation('/home/hydro/Downloads/summaTestCases_2.x/settings/wrrPaperTestCases/figure01/summa_fileManager_riparianAspenCLM2stream.txt')
```
**3.)**  make attribute of setting_path, and get filepath and name
```python
>>> S.setting_path.filepath
   "/summaTestCases_2.x/settings/"
>>> S.setting_path.name
   "setting_path" 
```
**4.)**  make attribute of Decision, and get filepath and name
```python
>>> S.decision_path.filepath
   "wrrPaperTestCases/figure09/"
>>> S.decision_path.filename
   "summa_zDecisions_riparianAspenCLM2stream.txt"
>>> S.decision_path.name
   "decision"
```   
**5.)**  change decision file name when users need to change decision file name
```python
>>> decision.filename = "Decision.py"
```   
**(2) manipulating Decision text file.**  

**1.)**  read Decision text file and create D attribute
```python
>>> D = S.decision_obj
```
**2.)**  get default simulation start date and time
```python
>>> D.simulStart.value
   "2005-07-01 00:00"
```
**3.)**  set and write simulation start time in Decision text file
```python
>>> D.simulStart.value = "2006-07-01 00:00"
```
**4.)**  get default simulation finish date and time
```python
>>> D.simulFinsh.value
   "2008-09-30 00:00"
```
**5.)**  set and write simulation finish time in Decision text file
```python
>>> sim_finish_time.value = "2007-09-30 00:00"
```
**6.)**  get abstract method name, default value, available options and description of each method
```python
>>> D.soilCatTbl.name
   "soilCatTbl"
>>> D.soilCatTbl.value
   "STAS"
>>> D.soilCatTbl.options
   "['STAS', 'STAS-RUC', 'ROSETTA']"
>>> D.soilCatTbl.description
   "soil-category dateset"
```
**7.)**  select option and write selected option in Decision.txt
```python
>>> D.soilCatTbl.value = 'STAS-RUC'
```

**(3) running summa model.**  

**1.)**  create S.executable attribute and get summa executable file
```python
>>> S.executable = "/home/hydro/Downloads/summa-master/bin/summa.exe"
```
**2.)**  set suffix for output filename
```python
>>> S.run_suffix = "pysumma_demo"
```
**3.)**  run summa model
```python
>>> S.execute()
```

**(4) Displaying summa output.**  

** plotting line plot with variables(1D, 2D)** 

**1.)**  import Plotting Module
```python
>>> from pysumma.Plotting import Plotting
>>> from jupyterthemes import jtplot
>>> import matplotlib.pyplot as plt
>>> jtplot.figsize(x=10, y=10)
```
**2.)**  read netCDF file
```python
>>> P = Plotting(S.output_path.filepath + S.output_prefix.value+'_' + D.simulStart.value[0:4] + '-' + D.simulFinsh.value[0:4] + '_' + S.run_suffix + '_1.nc')
```
**3.)**  open and read netCDF file and create P_info attribute
```python
>>> P_info = P.open_netcdf()
```
**4.)**  Display 1D (netCDF, variable[basin__AquiferRecharge]) with time series
```python
variable = [['basin__SurfaceRunoff','2'],['basin__ColumnOutflow','3'], 
            ['basin__AquiferStorage','4'],['basin__AquiferRecharge', '5'], 
            ['basin__AquiferBaseflow', '6'],['basin__AquiferTranspire','7'],
	    ['averageInstantRunoff', '8'], ['averageRoutedRunoff', '9']]
```
```python
>>> P.plot_1d(P_info, 5)
>>> plt.show()
```
**5.)**  Display 1D_hru (netCDF, hru, variable[scalarSWE]) with time series
```python
variable_num_Y = [['pptrate','0'],['airtemp','1'], ['nSnow','10'], ['nSoil','11'],
                  ['nLayers','12'],['midSoilStartIndex','13'], ['midTotoStartIndex','14'], 
                  ['ifcSoilStartIndex','15'],['ifcTotoStartIndex','16'],['scalarSWE','17'],
                  ['scalarSurfaceTemp','23'],['scalarSenHeatTotal','27'],
                  ['scalarLatHeatTotal','28'],['scalarSnowSublimation','29'],
                  ['scalarThroughfallSnow','30'],['scalarThroughfallRain','31'],
                  ['scalarRainPlusMelt','32'],['scalarInfiltration','33'],
                  ['scalarExfiltration','34'],['scalarSurfaceRunoff','35']]
```
```python
>>> P.plot_1d_hru(P_info, 0, 17)
>>> plt.show()
```
**6.)**  Display 1D_layer (netCDF, hru, variable[iLayerHeight], layer time[midTotoStartIndex]) with time series
```python
variable_num_Y = [['mLayerTemp','18'],['mLayerVolFracIce','19'], ['mLayerVolFracLiq','20'], 
                  ['mLayerVolFracWat','21'],['mLayerMatricHead','22'],['mLayerDepth','24'], 
                  ['mLayerHeight','25'], ['iLayerHeight','26'],['iLayerLiqFluxSoil','36'],
                  ['mLayerLiqFluxSoil','37']]
layer_time = [['midSoilStartIndex','13'], ['midTotoStartIndex','14'], 
              ['ifcSoilStartIndex','15'], ['ifcTotoStartIndex','16']]             
```
```python
>>> P.plot_1d_layer(P_info, 0, 26, 14)
>>> plt.show()
```

** Display plot from summa_plot repository created by andrew bennett from UW ** 

**1.)**  import layers
```python
>>> from pysumma.layers import layers
>>> import xarray as xr
>>> import geopandas as gp
```
**2.)**  display output of variables related layers such as snow and soil using layers.py
```python
>>> ds = xr.open_dataset(S.output_path.filepath + S.output_prefix.value+'_' + D.simulStart.value[0:4] + '-' + D.simulFinsh.value[0:4] + '_' + S.run_suffix + '_1.nc').isel(hru=0)
>>> layers(ds.isel(time=slice(0,500)), 'mLayerVolFracWat')
>>> plt.show()
```


## Bugs
  Our issue tracker is at https://github.com/DavidChoi76/pysumma_alpha0/issues.
  Please report any bugs that you find.  Or, even better, fork the repository on
  GitHub and create a pull request.  All changes are welcome, big or small, and we
  will help you make the pull request if you are new to git
  (just ask on the issue).

## License
  Distributed with a MIT license; see LICENSE.txt::

  Copyright (C) 2017 pySUMMA Developers
  YoungDon Choi <yc5ef@virginia.edu>
