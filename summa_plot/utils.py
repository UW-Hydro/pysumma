'''Utilities for preprocessing SUMMA data'''

import shapely
import geopandas as gpd


def simplify_shapefile(shapefile, outfile, simplify_level=250):
    '''Simplify the geometry of a shapefile and write out a new one'''
    geodf = gpd.GeoDataFrame.from_file(shapefile)
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
    geodf.to_file(outfile)
