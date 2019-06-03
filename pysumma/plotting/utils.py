'''Utilities for preprocessing SUMMA data'''

import numpy as np
import shapely
import geopandas as gpd
from cartopy.feature import NaturalEarthFeature


def justify(a, invalid_val=np.nan, axis=1, side='right'):
    """
    Justifies a 2D array
    Courtesy: https://stackoverflow.com/questions/44558215/python-justifying-numpy-array/44559180#44559180

    Parameters
    ----------
    A : ndarray
        Input array to be justified
    axis : int
        Axis along which justification is to be made
    side : str
        Direction of justification. It could be 'left', 'right', 'up', 'down'
        It should be 'left' or 'right' for axis=1 and 'up' or 'down' for axis=0.

    """
    if invalid_val is np.nan:
        mask = ~np.isnan(a)
    else:
        mask = a!=invalid_val
    justified_mask = np.sort(mask,axis=axis)
    if (side=='up') | (side=='left'):
        justified_mask = np.flip(justified_mask,axis=axis)
    out = np.full(a.shape, invalid_val)
    if axis==1:
        out[justified_mask] = a[mask]
    else:
        out.T[justified_mask.T] = a.T[mask.T]
    return out


def simplify_shapefile(shapefile, outfile=None, simplify_level=250):
    '''Simplify the geometry of a shapefile and write out a new one'''
    if isinstance(shapefile, str):
        geodf = gpd.GeoDataFrame.from_file(shapefile)
    elif isinstance(shapefile, gpd.GeoDataFrame):
        geodf = shapefile
    else:
        raise Exception("Invalid datatype given. Specify",
                        " either a path name or GeoDataFrame.")
    new_geoms = []
    for shp in geodf.geometry:
        if isinstance(shp, shapely.geometry.MultiPolygon):
            pieces = []
            for sub in shp:
                pieces.append(sub.simplify(simplify_level))
            shp = shapely.geometry.MultiPolygon(pieces)
            new_geoms.append(shp)
        else:
            shp = shp.simplify(simplify_level)
            new_geoms.append(shp)
    geodf.geometry = new_geoms
    if outfile:
        geodf.to_file(outfile)
    return geodf



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


