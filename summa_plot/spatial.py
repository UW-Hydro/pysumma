'''Spatial plotting for SUMMA output'''

import shapely
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
from cartopy.feature import NaturalEarthFeature
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon

from .utils import add_map_features


def gen_patches(da, geodf, robust=False):
    '''Simplify polygons and generate a PatchCollection for faster plotting'''
    vals = []
    patches = []
    for val, shp in zip(da.values, geodf.geometry):
        if isinstance(shp, shapely.geometry.MultiPolygon):
            for sub in shp:
                patches.append(Polygon(np.asarray(sub.exterior)))
                vals.append(val)
        else:
            patches.append(Polygon(np.asarray(shp.exterior)))
            vals.append(val)
    vals = np.array(vals)
    patches = PatchCollection(patches)
    patches.set_array(vals)
    if isinstance(robust, list):
        patches.set_clim(np.percentile(da.values, robust))
    elif robust:
        patches.set_clim(np.percentile(da.values, [2, 98]))
    return patches


def spatial(data_array, geodf, simplify_level=500, proj=ccrs.Mercator(),
            robust=False, colorbar=True, colormap='viridis'):
    '''Make a spatial plot'''
    # Preprocess the data
    geodf_crs = geodf.to_crs(crs=proj.proj4_params)
    patches = gen_patches(data_array, geodf_crs, simplify_level, robust, colormap)
    # Map plotting
    fig, ax = plt.subplots(nrows=1, ncols=1, subplot_kw=dict(projection=proj))
    ax.add_collection(patches)
    add_map_features(ax)
    ax.autoscale_view()

    # Colorbar plotting
    if isinstance(robust, list):
        minval, maxval = np.percentile(data_array.values, robust)
    elif robust:
        minval, maxval = np.percentile(data_array.values, [2, 98])
    else:
        minval, maxval = np.min(data_array.values), np.max(data_array.values)

    if colorbar:
        sm = plt.cm.ScalarMappable(norm=plt.Normalize(vmin=minval, vmax=maxval))
        sm._A = []
        cax = fig.add_axes([0.92, 0.2, 0.015, 0.6])
        cax.tick_params()
        cb = plt.colorbar(sm, cax=cax)
        cb.set_label(data_array.name)
    return fig, ax
