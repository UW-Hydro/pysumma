'''Utilities for preprocessing SUMMA data'''

import shapely
import geopandas as gpd
from cartopy.feature import NaturalEarthFeature


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


