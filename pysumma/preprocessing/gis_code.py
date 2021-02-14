import os
import shutil
import pkg_resources

delineation_d8 = pkg_resources.resource_filename(
        __name__, 'meta/grass_delineation_d8.sh')
delineation_dinf = pkg_resources.resource_filename(
        __name__, 'meta/grass_delineation_dinf.sh')
basin_extraction = pkg_resources.resource_filename(
        __name__, 'meta/basin_extraction.R')
spatial_hierarchy = pkg_resources.resource_filename(
        __name__, 'meta/grass_spatial_hierarchy.sh')
ssurgo_extraction = pkg_resources.resource_filename(
        __name__, 'meta/ssurgo_extraction.r')
soiltexture2gis = pkg_resources.resource_filename(
        __name__, 'meta/ssurgo_soiltexture2gis.r')
ssurgo_soil_db = pkg_resources.resource_filename(
        __name__, 'meta/ssurgo_soils_db.csv')