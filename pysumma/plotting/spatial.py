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


def spatial(data_array, geodf, ax=None, simplify_level=500, proj=ccrs.Mercator(),
            robust=False, add_colorbar=True, colormap='viridis'):
    """Make a spatial plot. Example usage:

    ::

        import pysumma.plotting as psp
        import geopandas as gpd

        gdf = gpd.GeoDataFrame.from_file(shapefile)
        psp.spatial(ds[scalarTotalSoilLiq'].mean(dim='time'), gdf)

    Parameters
    ----------
    data_array: xr.DataArray
        The variable to plot
    geodf: gpd.GeoDataFrame
        The GeoDataFrame containing the geometries to plot on
    ax: Axes
        The axis to draw on. If none are provided one will be
        created
    simplify_level: Int, default=500
        The simplification level for the geometries. Higher values
        will simplify further. This can help with speed for large domains
        or overly complicated geometries.
    proj: crs.Projection, default=ccrs.Mercator
        The projection to draw onto
    robust: boolean or List[float], default=False
        If true, will clip to 2nd and 98th percentiles.
        If given as a list of integers will clip to the range given.
        This can help if you have outliers in your dataset
    add_colorbar: boolean, default=True
        Whether to add a colorbar
    colormap: string, default='viridis'
        The colormap to draw with
    """
    # Preprocess the data
    geodf_crs = geodf.to_crs(crs=proj.proj4_params)
    patches = gen_patches(data_array, geodf_crs, robust)
    # Map plotting
    if not ax:
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

    if add_colorbar:
        sm = plt.cm.ScalarMappable(norm=plt.Normalize(vmin=minval, vmax=maxval))
        sm._A = []
        cax = plt.gcf().add_axes([0.92, 0.2, 0.015, 0.6])
        cax.tick_params()
        cb = plt.colorbar(sm, cax=cax)
        cb.set_label(data_array.name)
    return ax
