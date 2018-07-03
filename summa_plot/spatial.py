'''Spatial plotting for SUMMA output'''

import shapely
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
from cartopy.feature import NaturalEarthFeature
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon


def add_map_features(ax, states_provinces=True, country_borders=True,
                     land=True, ocean=True, lake=False):
    '''Add background features to an axis'''
    if states_provinces:
        states_provinces = NaturalEarthFeature(
                category='cultural', name='admin_1_states_provinces_lines',
                scale='50m', facecolor='none')
        ax.add_feature(states_provinces, edgecolor='black', alpha=.8, zorder=2)
    if country_borders:
        ctry_borders = NaturalEarthFeature(
            category='cultural', name='admin_0_boundary_lines_land',
            scale='50m', facecolor='none')
        ax.add_feature(ctry_borders, edgecolor='black', zorder=2, alpha=0.8, linewidth=1)
    if land:
        land = NaturalEarthFeature(
            category='physical', name='land', edgecolor='face', facecolor=cfeature.COLORS['land'], scale='50m')
        ax.add_feature(land, zorder=0)
    if ocean:
        ocean = NaturalEarthFeature(
            category='physical', name='ocean', edgecolor='face', facecolor=cfeature.COLORS['water'], scale='50m')
        ax.add_feature(ocean, zorder=1)
    if lake:
        rivers_lakes = NaturalEarthFeature(
            category='physical', name='rivers_lake_centerlines',
            scale='50m', facecolor='none')
        ax.add_feature(rivers_lakes, facecolor='lightblue', zorder=2)


def gen_patches(data_array, geodf, simplify_level=0, robust=False, colormap='viridis'):
    '''Simplify polygons and generate a PatchCollection for faster plotting'''
    vals = []
    patches = []
    geoms = geodf.geometry[data_array['hru'].values]

    for val, shp in zip(data_array.values, geoms):
        if isinstance(shp, shapely.geometry.MultiPolygon):
            for sub in shp:
                if simplify_level:
                    patches.append(Polygon(np.asarray(
                        sub.simplify(simplify_level).exterior)))
                else:
                    patches.append(Polygon(np.asarray(
                        sub.exterior)))
                vals.append(val)
        else:
            if simplify_level:
                patches.append(
                        Polygon(np.asarray(shp.simplify(simplify_level).exterior)))
            else:
                patches.append(Polygon(np.asarray(shp.exterior)))
            vals.append(val)
    vals = np.array(vals)
    patches = PatchCollection(patches, linewidth=0., edgecolor=None, alpha=1.0, cmap=colormap)
    patches.set_array(vals)
    if robust:
        if type(robust) is list:
            patches.set_clim(np.percentile(data_array.values, robust))
        else:
            patches.set_clim(np.percentile(data_array.values, [2,98]))
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
    if robust:
        if type(robust) is list:
            minval, maxval = np.percentile(data_array.values, robust)
        else:
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


