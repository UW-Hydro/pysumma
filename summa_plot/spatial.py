'''Spatial plotting for SUMMA output'''

import cartopy.feature as cfeature
import cartopy.crs as ccrs
from cartopy.mpl.gridliner imoport LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import geopandas as gp
import xarray as xr
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import shapely


def add_map_features(ax, states_provinces=True, country_borders=True,
                     land=True, ocean=True, lake=False):
    '''Add background features to an axis'''
    if states_provinces:
        states_provinces = cfeature.NaturalEarthFeature(category='cultural',
                name='admin_1_states_provinces_lines', scale='50m', facecolor='none')
        ax.add_feature(states_provinces, edgecolor='black', alpha=0.8, zorder=2)
    if country_borders:
        country_borders = cfeature.NaturalEarthFeature(category='cultural',
                name='admin_0_boundary_lines_land', scale='50m', facecolor='none')
        ax.add_feature(country_borders, edgecolor='black', zorder=2, linewidth=1)
    if land:
        land = cfeature.NaturalEarthFeature(category='physical',
            name='land', scale='50m', facecolor='gray')
        ax.add_feature(land, facecolor='lightgray', zorder=0)
    if ocean:
        ocean = cfeature.NaturalEarthFeature(category='physical',
            name='ocean', scale='50m', facecolor='blue')
        ax.add_feature(ocean, facecolor='lightblue', zorder=1)
    if lake:
        rivers_lakes = cfeature.NaturalEarthFeature(category='physical',
            name='rivers_lake_centerlines', scale='50m', facecolor='none')
        ax.add_feature(rivers_lakes, facecolor='lightblue', zorder=2)


def gen_patches(data_array, geodf, simplify_level=500):
    '''Simplify polygons and generate a PatchCollection for faster plotting'''
    vals = []
    patches = []

    for val, shp in zip(data_array.values, geodf.geometry):
        if isinstance(shp, shapely.geometry.MultiPolygon):
            for sub in shp:
                patches.append(Polygon(np.asarray(sub.simplify(simplify_level).exterior)))
                vals.append(val)
        else:
            patches.append(Polygon(np.asarray(shp.simplify(simplify_level).exterior)))
            vals.append(val)
    patches = PatchCollection(patches, linewidth=0.0, edgecolor=None, alpha=1.0)
    patches.set_array(np.array(vals))
    return patches


def spatial(data_array, geodf, simplify_level=500, projection=ccrs.Mercator()):
    '''Make a spatial plot'''
    patches = gen_patches(data_array, geodf, simplify_level)
    fig, ax = plt.subplots(nrows=1, ncols=1, subplot_kw={'Projection': projection})
    ax.add_collection(patches)
    add_map_features(ax)
    ax.autoscale_view()
    return fig, ax
