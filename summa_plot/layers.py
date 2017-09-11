'''Layer plotting for SUMMA output'''

import numpy as np
import xarray as xr
import matplotlib as mpl
import matplotlib.pyplot as plt
import itertools


def layers(ds, var, cmap='viridis'):
    '''Plot a cross section of layers'''
    layers = ds.nLayers.values.astype('int')
    max_layers = np.amax(layers)
    depths = np.empty((max_layers+1, len(ds.time)))
    depths[:] = np.nan
    vals = np.empty((max_layers, len(ds.time)))
    vals[:] = np.nan

    layer_refs = ['Snow', 'Soil', 'Toto']
    for ref in layer_refs:
        test_coord = 'mid{}AndTime'.format(ref)
        if test_coord in ds[var].dims:
            ifcStartIdx = ds['ifc{}StartIndex'.format(ref)].values
            midStartIdx = ds['mid{}StartIndex'.format(ref)].values
            break
    else:
        raise ValueError("Dataset provided doesn't appear to have layers!")

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
    times = ds['time'].values
    times = times - 0.5*(times[1] - times[0])
    width = (times[1]-times[0])/np.timedelta64(1, 'D')
    #plt.bar(times, prev, color=colors(vals[0]))
    for d, v in zip(depths[1:], vals):
        plt.bar(times, prev-d, width=width, color=colors(norm(v)), bottom=d, edgecolor='none')
        prev = d
    sm = plt.cm.ScalarMappable(cmap=colors, norm=norm)
    sm._A = []
    plt.colorbar(sm)
    return plt.gcf(), plt.gca()
