.. _configuration.rst:

Interfaces to configuration files
*********************************

SUMMA model setups require a number of configuration files and data sources to run.
pysumma provides interfaces to each of these files in a standardized fashion, allowing you to quickly manipulate existing SUMMA configurations.
For more information about the in depth details of each of the required inputs for SUMMA see the `SUMMA documentation on input <https://summa.readthedocs.io/en/latest/input_output/SUMMA_input/>`_
This page shows some basic examples of how you can interact with these configuration objects as well as extremely concise descriptions of what each object does.
For more detailed information about each of the objects you can browse our API documentation `here <api.rst>`_.


Text based files
================
All of the text-based input files are implemented around a base object named the ``OptionContainer``.
In turn, each specific option within these text-based inputs are implemented as an ``Option``.
Most of the code for this grouping of option types are in these base classes.
Specifics of the implementations are in each file's specific class.

The generic way to interact with these types of files is similar to how you would interact with a Python dictionary.
It is possible to list all of the available attributes for each of these configuration types by using the ``list_options()`` method.
As an example we will first show basic usage with the ``FileManager`` class.
The other classes are shown in more condensed forms only to show the various differences between them.

File manager
------------
The filemanager tells SUMMA where to find each of the other required inputs.
It can be thought of the entry point to a SUMMA simulation.
The pysumma ``FileManager`` object stores each of these paths as well as provides an interface to the datastructres for easier manipulation.

``FileManager`` objects are instantiated by providing the path to them as well as the file name as separate arguments.
The ``FileManager`` contains references to all of the other configuration files through the various attributes.
See the `API documentation <api.rst>`_ for more information about what attributes are available.

::

    import pysumma as ps
    fm = ps.FileManager('./summa_setup_template', 'file_manager.txt')


Then, you can see what is in it simply by printing it out:

::

    print(fm)

    > controlVersion          'SUMMA_FILE_MANAGER_V3.0.0'
    > simStartTime            '2002-10-01 00:00'
    > simEndTime              '2003-05-31 00:00'
    > tmZoneInfo              'localTime'
    > settingsPath            '/pool0/data/andrbenn/dana_3_test/.pysumma/_test/settings/'
    > forcingPath             './forcings/'
    > outputPath              './output/'
    > decisionsFile           'decisions.txt'
    > outputControlFile       'output_control.txt'
    > globalHruParamFile      '../params/local_param_info.txt'
    > globalGruParamFile      '../params/basin_param_info.txt'
    > attributeFile           '../params/local_attributes.nc'
    > trialParamFile          '../params/parameter_trial.nc'
    > forcingListFile         '../forcings/forcing_file_list.txt'
    > initConditionFile       '../params/initial_conditions.nc'
    > outFilePrefix           'template_output'
    > vegTableFile            'VEGPARM.TBL'
    > soilTableFile           'SOILPARM.TBL'
    > generalTableFile        'GENPARM.TBL'
    > noahmpTableFile         'MPTABLE.TBL'

To see how to access each of these specific options you can use the ``list_options`` method.
Then, each of these keys can be accessed directly similarly to how is done with python dictionaries.
This can be used to inspect the values of each option as well as modify their values.

::

    print(fm['outputPrefix'])

    > 'test'    ! output_prefix

    fm['outputPrefix'] = 'tutorial'

    print(fm['output_prefix'])

    > 'tutorial'    ! output_prefix


Decisions
---------
The decisions file contains the specification of the various physics options to use.
It also contains the run times and other algorithmic control options.
See `the SUMMA documentation <https://summa.readthedocs.io/en/latest/input_output/SUMMA_input/#infile_model_decisions>`_ for a more complete description of the decisions.

Instantiation of ``Decisions`` objects is similar to that of the other ``ObjectContainers``.
Once instantiated you can inspect the available decisions and the options available for each of them as follows.

::

    dec = ps.Decisions('.', 'decisions.txt')
    print(dec['snowLayers'])

    > snowLayers    CLM_2010             ! choice of method to combine and sub-divide snow layers

    print(dec.list_options())

    > ['soilCatTbl', 'vegeParTbl', 'soilStress', 'stomResist',
    >  'fDerivMeth', 'LAI_method', 'f_Richards', 'groundwatr',
    >  'hc_profile', 'bcUpprTdyn', 'bcLowrTdyn', 'bcUpprSoiH',
    >  'bcLowrSoiH', 'veg_traits', 'canopyEmis', 'snowIncept',
    >  'windPrfile', 'astability', 'canopySrad', 'alb_method',
    >  'compaction', 'snowLayers', 'thCondSnow', 'thCondSoil',
    >  'spatial_gw', 'subRouting', 'num_method']

    print(dec['snowLayers'])

    > snowLayers    CLM_2010             ! choice of method to combine and sub-divide snow layers

    print(dec['snowLayers'].available_options)

    > ['jrdn1991', 'CLM_2010']

    dec['snowLayers'] = 'jrdn1991'

Forcing file list
-----------------
The forcing file list contains a listing of each of the forcing files available for use as SUMMA input.
To instantiate the `ForcingList` you will have to specify the path that is set as the ``input_path`` in your ``FileManager``. Below we show using the ``FileManager`` (``fm``) to do so.
Once instantiated you can also use the `ForcingList` object to inspect the forcing files themselves.

::

    ff = ps.ForcingList('.', 'forcingFileList.1hr.txt', fm['input_path'])
    print(ff)

    >> 'forcing_file.nc'

    print(ff.open_forcing_data())

    >> [
    >>  <xarray.Dataset>
    >>  Dimensions:    (hru: 671, time: 744)
    >>  Coordinates:
    >>    * time       (time) datetime64[ns] 1980-01-01 ... 1980-01-31T23:00:00
    >>  Dimensions without coordinates: hru
    >>  Data variables:
    >>      LWRadAtm   (time, hru) float32 ...
    >>      SWRadAtm   (time, hru) float32 ...
    >>      airpres    (time, hru) float32 ...
    >>      airtemp    (time, hru) float32 ...
    >>      data_step  timedelta64[ns] ...
    >>      hruId      (hru) int64 ...
    >>      pptrate    (time, hru) float32 ...
    >>      spechum    (time, hru) float32 ...
    >>      windspd    (time, hru) float32 ...
    >> ]

Output control
--------------
The output control file contains a listing of all of the variables desired to be written to output,
along with how often and whether any aggregation needs to be done before writeout.
Because there are many available output variables that you can choose from we do not exhaustively list them.
The format of the output control file mirrors the way that it is described in the
`SUMMA docs <https://summa.readthedocs.io/en/latest/input_output/SUMMA_input/#output-control-file>`_.

::

    oc = ps.OutputControl('.', 'output_control.txt')
    print(oc)

    >> ! varName             | outFreq | sum | inst | mean | var | min | max | mode
    >> pptrate               | 1       | 0   | 1    | 0    | 0   | 0   | 0   | 0
    >> airtemp               | 1       | 0   | 1    | 0    | 0   | 0   | 0   | 0
    >> scalarSWE             | 1       | 0   | 1    | 0    | 0   | 0   | 0   | 0
    >> scalarRainPlusMelt    | 1       | 0   | 1    | 0    | 0   | 0   | 0   | 0
    >> scalarTotalET         | 1       | 0   | 1    | 0    | 0   | 0   | 0   | 0
    >> scalarTotalRunoff     | 1       | 0   | 1    | 0    | 0   | 0   | 0   | 0
    >> scalarSurfaceRunoff   | 1       | 0   | 1    | 0    | 0   | 0   | 0   | 0
    >> scalarTotalSoilWat    | 1       | 0   | 1    | 0    | 0   | 0   | 0   | 0
    >> scalarAquiferStorage  | 1       | 0   | 1    | 0    | 0   | 0   | 0   | 0
    >> scalarAquiferBaseflow | 1       | 0   | 1    | 0    | 0   | 0   | 0   | 0
    >> scalarNetRadiation    | 1       | 0   | 1    | 0    | 0   | 0   | 0   | 0
    >> scalarLatHeatTotal    | 1       | 0   | 1    | 0    | 0   | 0   | 0   | 0
    >> scalarSenHeatTotal    | 1       | 0   | 1    | 0    | 0   | 0   | 0   | 0

    print(oc['scalarTotalRunoff'].statistic)

    >> instant

    oc['scalarTotalRunoff'] = [24, 1, 0, 0, 0, 0, 0, 0]
    print(oc['scalarTotalRunoff'].statistic)

    >> sum


GlobalParams
--------------------
The GlobalParams object listing of global parameters. Spatially dependent parameters are specified
in the parameter trial NetCDF file. Values which are specified in the local parameter info file will be overwritten
by those specified in the parameter trial file.
As with the output control file, there are many parameters which can be specified, so we omit them for brevity.
Additionally, we currently do not have descriptions of what each of the parameters represent - the best way to figure
this out currently is by looking at the SUMMA source code directly.

::

    lpi = ps.GlobalParams('.', 'global_param_info.txt')
    print(lpi.list_options())

    >> ['upperBoundHead', 'lowerBoundHead', 'upperBoundTheta', 'lowerBoundTheta',
    >>  'upperBoundTemp', 'lowerBoundTemp', 'tempCritRain', 'tempRangeTimestep',
    >>  ...
    >>  'zmaxLayer1_lower', 'zmaxLayer2_lower', 'zmaxLayer3_lower', 'zmaxLayer4_lower',
    >>  'zmaxLayer1_upper', 'zmaxLayer2_upper', 'zmaxLayer3_upper', 'zmaxLayer4_upper']

    lpi['tempCritRain'] = 273.3

NetCDF based files
==================
The following input files are NetCDF-based and therefore, should be interacted with via ``xarray`` when using pysumma:

 - Parameter trial (Spatially distributed parameters)
 - Basin parameters
 - Local attributes
 - Initial conditions

