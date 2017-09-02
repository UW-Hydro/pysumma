'''Layer plotting for SUMMA output'''

import numpy as np
import xarray as xr
import itertools


def layers(ds, var):
    '''Plot a cross section of layers'''
    layers = ds.nLayers.values.astype('int')
    max_layers = np.max(layers)
    depths = np.empty((max_layers+1, len(ds.time)))
    depths[:] = np.nan
    vals = np.empty((max_layers, len(ds.time)))
    vals[:] = np.nan

    layer_refs = ['Snow', 'Soil', 'Toto']
    for ref in layer_refs:
        test_coord = 'ifc{}'.format(ref)
        if test_coord in ds['var'].dims:
            ifcStartIdx = ds['ifc{}StartIndex'.format(ref)]
            midStartIdx = ds['mid{}StartIndex'.format(ref)]
    else:
        raise ValueError("Dataset provided doesn't appear to have layers!")


    for i in range(len(ds.time.values)):
        start_ifc = int(ds.ifcTotoStartIndex[i]
