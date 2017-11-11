'''Spatial plotting for SUMMA output'''

import shapely
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
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
        ax.add_feature(ctry_borders, edgecolor='black', zorder=2, linewidth=1)
    if land:
        land = NaturalEarthFeature(
            category='physical', name='land', scale='50m', facecolor='gray')
        ax.add_feature(land, facecolor='lightgray', zorder=0)
    if ocean:
        ocean = NaturalEarthFeature(
            category='physical', name='ocean', scale='50m', facecolor='blue')
        ax.add_feature(ocean, facecolor='lightblue', zorder=1)
    if lake:
        rivers_lakes = NaturalEarthFeature(
            category='physical', name='rivers_lake_centerlines',
            scale='50m', facecolor='none')
        ax.add_feature(rivers_lakes, facecolor='lightblue', zorder=2)


def gen_patches(data_array, geodf, simplify_level=0, robust=False):
    '''Simplify polygons and generate a PatchCollection for faster plotting'''
    vals = []
    patches = []

    for val, shp in zip(data_array.values, geodf.geometry):
        if isinstance(shp, shapely.geometry.MultiPolygon):
            for sub in shp:
                if not simplify_level:
                    patches.append(Polygon(np.asarray(
                        sub.simplify(simplify_level).exterior)))
                else:
                    patches.append(Polygon(np.asarray(
                        sub.exterior)))
                vals.append(val)
        else:
            if not simplify_level:
                patches.append(
                        Polygon(np.asarray(shp.simplify(simplify_level).exterior)))
            else:
                patches.append(Polygon(np.asarray(shp.exterior)))
            vals.append(val)
    vals = np.array(vals)
    patches = PatchCollection(patches, linewidth=0., edgecolor=None, alpha=1.0)
    patches.set_array(vals)
    if robust:
        patches.set_clim(np.percentile(vals, [5,95]))
    return patches


def spatial(data_array, geodf, simplify_level=500, proj=ccrs.Mercator(),
            robust=False):
    '''Make a spatial plot'''
    # Preprocess the data
    geodf_crs = geodf.to_crs(crs=proj.proj4_params)
    patches = gen_patches(data_array, geodf_crs, simplify_level, robust)

    # Map plotting
    fig, ax = plt.subplots(nrows=1, ncols=1, subplot_kw=dict(projection=proj))
    ax.add_collection(patches)
    add_map_features(ax)
    ax.autoscale_view()

    # Colorbar plotting
    if robust:
        minval, maxval = np.percentile(data_array.values, [5, 95])
    else:
        minval, maxval = np.min(data_array.values), np.max(data_array.values)
    sm = plt.cm.ScalarMappable(norm=plt.Normalize(vmin=minval, vmax=maxval))
    sm._A = []
    cax = fig.add_axes([0.92, 0.2, 0.015, 0.6])
    cax.tick_params()
    cb = plt.colorbar(sm, cax=cax)
    cb.set_label(data_array.name)
    return fig, ax


