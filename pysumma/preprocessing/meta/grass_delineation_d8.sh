#!/bin/bash
inputThreshold=$1
inputLower=$2
inputUpper=$3
#
g.region raster=dem
r.mask -r
# set maxcol
declare $(r.info map=dem | awk 'NR==13{print "maxcol="$3}')
# set x, y, and physical variables (e.g., slope, aspect ... etc) based on elevation
r.mapcalc --overwrite expression="xmap = x()"
r.mapcalc --overwrite expression="ymap = y()"
r.watershed -s --overwrite elevation=dem accumulation=uaa drainage=drain tci=wetness_index
r.slope.aspect --overwrite elevation=dem slope=slope_ aspect=aspect_
r.horizon --overwrite -d elevation=dem direction=180 output="west" distance=1.0
r.horizon --overwrite -d elevation=dem direction=0 output="east" distance=1.0
# finding the nearest stream/uaa to the provided "outlet" point (vector data)
r.mapcalc --overwrite expression="tmp = if(abs(uaa)>=$inputLower&&abs(uaa)<=$inputUpper,1,null())"
r.to.vect input=tmp output=tmp type=line
declare $(v.distance -p from=outlet from_type=point to=tmp to_type=line upload=to_x,to_y separator=space | awk '{print "xyCoord=" $2 "," $3}')
g.remove -f type=vector name=tmp
g.remove -f type=raster name=tmp
# delineate catchment based on the nearest outlet point on the stream/uaa
r.water.outlet --overwrite input=drain output=basin coordinates=$xyCoord
g.region zoom=basin
r.watershed -s --overwrite elevation=dem threshold=$inputThreshold basin=sub stream=str half_basin=hill
r.mask raster=basin
r.mapcalc --overwrite expression="basin = if(isnull(hill),null(),1)"
g.region raster=dem
g.region zoom=basin
r.mask -r
r.mask raster=basin
# set patch and other variables
r.mapcalc --overwrite expression="patch = row()*$maxcol+col()"
r.mapcalc --overwrite expression="zone = patch"
r.mapcalc --overwrite expression="rowmap = row()"
r.mapcalc --overwrite expression="colmap = col()"
r.mapcalc --overwrite expression="ZERO = 0"
r.mapcalc --overwrite expression="ONE = 1"
r.mapcalc --overwrite expression="slope = if(isnull(slope_),0.143,slope_)"
r.mapcalc --overwrite expression="aspect = if(isnull(aspect_),abs(drain)*45,aspect_)"
