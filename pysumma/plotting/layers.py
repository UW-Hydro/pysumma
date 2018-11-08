'''Layer plotting for SUMMA output'''

import numpy as np
import xarray as xr
import matplotlib as mpl
import matplotlib.pyplot as plt
import itertools


def layers(ds, var, cmap='viridis'):
    '''Plot a cross section of layers'''
    # midsoil number 8, row : time, column : hru number , value the number of midsoil layer
    layers = ds.nLayers.values.astype('int')
    # midToto number 13
    max_layers = np.amax(layers)
    # ifcToto number 14, row: time, column : 14 
    depths = np.empty((max_layers+1, len(ds.time)))
    depths[:] = np.nan
    # midToto number 13, row: time, column : 13
    vals = np.empty((max_layers, len(ds.time)))
    vals[:] = np.nan

    # Look for the right dimension
    layer_refs = ['Snow', 'Soil', 'Toto']
    for ref in layer_refs:
        test_coord = 'mid{}AndTime'.format(ref)
        if test_coord in ds[var].dims:
            ifcStartIdx = ds['ifc{}StartIndex'.format(ref)].values
            midStartIdx = ds['mid{}StartIndex'.format(ref)].values
            break
    else:
        raise ValueError("Dataset provided doesn't appear to have layers!")

    # Unpack values for depth and desired variable
    for i in range(len(ds['time'].values)):
        start_ifc = int(ifcStartIdx[i]) - 1
        start_mid = int(midStartIdx[i]) - 1
        end_ifc = start_ifc + int(layers[i]) + 1
        end_mid = start_mid + int(layers[i])
        depths[0:layers[i]+1, i] = -ds['iLayerHeight'][start_ifc:end_ifc]
        vals[0:layers[i], i] = ds[var][start_mid:end_mid]

    colors = plt.get_cmap(cmap)
    norm = mpl.colors.Normalize(np.nanmin(vals), np.nanmax(vals))
    prev = depths[0]

    # Center bars on time
    times = ds['time'].values
    times = times - 0.5*(times[1] - times[0])
    width = (times[1]-times[0])/np.timedelta64(1, 'D')
    # Plot at each depth
    for d, v in zip(depths[1:], vals):
        plt.bar(times, prev-d, width=width, color=colors(norm(v)), bottom=d, edgecolor='none')
        prev = d
    sm = plt.cm.ScalarMappable(cmap=colors, norm=norm)
    sm._A = []
    plt.colorbar(sm)
    return plt.gcf(), plt.gca()
