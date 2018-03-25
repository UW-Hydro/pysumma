'''Spatial plotting for SUMMA output'''

import shapely
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
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
        patches.set_clim(np.percentile(da.values, [2,98]))
    return patches

def spatial(da, gdf, da_coord='hru', gdf_coord=None, proj=ccrs.Mercator(), robust=False, colorbar=True):
    '''Make a spatial plot'''
    # Preprocess the data
    if not gdf_coord:
        gdf_coord = da_coord
    gdf_crs = gdf.to_crs(crs=proj.proj4_params)
    # Check if coordinate datatypes are compatible
    try:
        gdf[gdf_coord][0] == da[da_coord].values[0]
    except:
        raise ValueError('Comparison datatypes do not agree!',
                'Check that the datatypes in the shapefile and'
                'output data match!')
    # Filter the data
    gdf_crs = gdf_crs[gdf_crs[gdf_coord].isin(da[da_coord].values)]
    da_sub = da.loc[{da_coord: gdf_crs[gdf_coord].values}]
    patches = gen_patches(da_sub, gdf_crs, robust)

    # Map plotting
    fig, ax = plt.subplots(nrows=1, ncols=1, subplot_kw=dict(projection=proj))
    ax.add_collection(patches)
    add_map_features(ax)
    ax.autoscale_view()

    # Colorbar plotting
    if isinstance(robust, list):
        minval, maxval = np.percentile(da.values, robust)
    elif robust:
        minval, maxval = np.percentile(da.values, [2, 98])
    else:
        minval, maxval = np.min(da.values), np.max(da.values)

    if colorbar:
        sm = plt.cm.ScalarMappable(norm=plt.Normalize(vmin=minval, vmax=maxval))
        sm._A = []
        cax = fig.add_axes([0.92, 0.2, 0.015, 0.6])
        cax.tick_params()
        cb = plt.colorbar(sm, cax=cax)
        cb.set_label(da.name)
    return fig, ax
