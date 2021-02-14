#!/bin/bash
inputThreshold=$1
inputLower=$2
inputUpper=$3
#
g.region raster=dem
r.mask -r
# set x, y, and physical variables (e.g., slope, aspect ... etc) based on elevation
r.mapcalc --overwrite expression="xmap = x()"
r.mapcalc --overwrite expression="ymap = y()"
r.mapcalc --overwrite expression="rowmap = row()"
r.mapcalc --overwrite expression="colmap = col()"
r.slope.aspect --overwrite elevation=dem slope=slope_ aspect=aspect_
r.horizon --overwrite -d elevation=dem direction=180 output="west" distance=1.0
r.horizon --overwrite -d elevation=dem direction=0 output="east" distance=1.0
#
r.watershed --overwrite elevation=dem accumulation=uaa drainage=drain tci=wetness_index  # -s
r.watershed --overwrite elevation=dem threshold=$inputThreshold basin=sub_ stream=str_ half_basin=hill_  ## -s
#r.watershed --overwrite elevation=dem accumulation=uaaD8 -s
#
# finding the nearest stream/uaa to the provided "outlet" point (vector data)
# this snapping process gets wrong with D-inf routing !
# ... this is for D-8
#r.mapcalc --overwrite expression="tmp = if(abs(uaa)>=$inputLower&&abs(uaa)<=$inputUpper,1,null())"
#r.to.vect input=tmp output=tmp type=line
#declare $(v.distance -p from=outlet from_type=point to=tmp to_type=line upload=to_x,to_y separator=space | awk '{print "xyCoord=" $2 "," $3}')

# ... this is for D-Inf (maybe do it in R?)
# v.to.rast input=outlet type=point output=outlet_tmp use=cat <--- not
eval $(r.what --quiet map=sub_ points=outlet separator=space | awk '{print "outletSUB=" $3}')
r.mapcalc --overwrite expression="tmp = if(sub_==$outletSUB && str_>0, uaa, null())"
r.to.vect --overwrite input=tmp output=tmp type=line
eval $(v.distance -p from=outlet from_type=point to=tmp to_type=line upload=to_x,to_y separator=space | awk '{print "xyCoord=" $2 "," $3}')
# delineate catchment based on the nearest outlet point on the stream/uaa ##--- this step is contrained by D8
r.water.outlet --overwrite input=drain output=basin_ coordinates=$xyCoord
#
r.to.vect --overwrite input=sub_ output=tmp type=area
v.rast.stats -c map=tmp raster=basin_ column_prefix=select method=average
v.to.rast --overwrite input=tmp type=area where=select_average>0 output=tmp use=attr attribute_column=select_average
#g.region raster=tmp


