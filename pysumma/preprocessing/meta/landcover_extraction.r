options(scipen=999)
library(sp)
library(XML)
library(rgrass7)

tryCatch({ use_sp() },error=function(cond){message(cond)},warning=function(cond){message(cond)},finally={message("Please update the rgrass7 package on R")})

rast = readRAST(c('basin','str','LULCcode'))
mask = !is.na(rast@data[[1]])
str = rast@data[[2]][mask]
lulc = rast@data[[3]][mask]

rast$vegid = rep(NA,length(mask))
rast$landuse = rep(NA,length(mask))
rast$lai = rep(NA,length(mask))
rast$impervious = rep(NA,length(mask))
rast$coverFrac = rep(NA,length(mask))

#--- forest
    cond=(lulc==41 | lulc==43 | lulc==90 | lulc==95) & is.na(str); 
    rast$vegid[mask][cond] = as.integer(2) # deciduous @ vegCollection.csv
    rast$landuse[mask][cond] = as.integer(2) # undeveloped @ lulcCollection.csv
    rast$coverFrac[mask][cond] = 1.0
    rast$lai[mask][cond] = 4.5
    rast$impervious[mask][cond] = 0.0

    cond=(lulc==42) & is.na(str); 
    rast$vegid[mask][cond] = as.integer(1) # evergreen @ vegCollection.csv 
    rast$landuse[mask][cond] = as.integer(2) # undeveloped @ lulcCollection.csv
    rast$coverFrac[mask][cond] = 1.0
    rast$lai[mask][cond] = 5.0
    rast$impervious[mask][cond] = 0.0

    cond=(lulc==51 | lulc==52) & is.na(str); 
    rast$vegid[mask][cond] = as.integer(6) # shrub @ vegCollection.csv 
    rast$landuse[mask][cond] = as.integer(2) # undeveloped @ lulcCollection.csv
    rast$coverFrac[mask][cond] = 1.0
    rast$lai[mask][cond] = 2
    rast$impervious[mask][cond] = 0.0

#--- pasture / grass / agriculture 
    cond=(lulc==71 | lulc==72 | lulc==81 | lulc==82) & is.na(str); 
    rast$vegid[mask][cond] = as.integer(3) # grass @ vegCollection.csv 
    rast$landuse[mask][cond] = as.integer(1) # grass @ lulcCollection.csv
    rast$coverFrac[mask][cond] = 1.0
    rast$lai[mask][cond] = 1.5
    rast$impervious[mask][cond] = 0.0

#--- urban / barren
    cond=(lulc==31) & is.na(str); 
    rast$vegid[mask][cond] = as.integer(6) # shrub @ vegCollection.csv (may vary by state/county/city/local)
    rast$landuse[mask][cond] = as.integer(2) # undeveloped @ lulcCollection.csv
    rast$coverFrac[mask][cond] = 0.15 # 15% grass/lawn
    rast$lai[mask][cond] = 3.0
    rast$impervious[mask][cond] = 0.85

    cond=(lulc==21) & is.na(str); 
    rast$vegid[mask][cond] = as.integer(3) # grass @ vegCollection.csv (may vary by state/county/city/local)
    rast$landuse[mask][cond] = as.integer(3) # urban @ lulcCollection.csv
    rast$coverFrac[mask][cond] = 0.8 # 80% grass/lawn
    rast$lai[mask][cond] = 1.5
    rast$impervious[mask][cond] = 0.2

    cond=(lulc==22) & is.na(str); 
    rast$vegid[mask][cond] = as.integer(3) # grass @ vegCollection.csv (may vary by state/county/city/local)
    rast$landuse[mask][cond] = as.integer(3) # urban @ lulcCollection.csv
    rast$coverFrac[mask][cond] = 0.5 # 50% grass/lawn
    rast$lai[mask][cond] = 1.5
    rast$impervious[mask][cond] = 0.5

    cond=(lulc==23) & is.na(str); 
    rast$vegid[mask][cond] = as.integer(3) # grass @ vegCollection.csv (may vary by state/county/city/local)
    rast$landuse[mask][cond] = as.integer(3) # urban @ lulcCollection.csv
    rast$coverFrac[mask][cond] = 0.2 # 20% grass/lawn
    rast$lai[mask][cond] = 1.5
    rast$impervious[mask][cond] = 0.8

    cond=(lulc==24) & is.na(str); 
    rast$vegid[mask][cond] = as.integer(4) # no-veg @ vegCollection.csv (may vary by state/county/city/local)
    rast$landuse[mask][cond] = as.integer(3) # urban @ lulcCollection.csv
    rast$coverFrac[mask][cond] = 1.0
    rast$lai[mask][cond] = 1.0
    rast$impervious[mask][cond] = 1.0

    cond= !is.na(str); 
    rast$vegid[mask][cond] = as.integer(4) # no-veg @ vegCollection.csv (may vary by state/county/city/local)
    rast$landuse[mask][cond] = as.integer(2) # undeveloped @ lulcCollection.csv
    rast$coverFrac[mask][cond] = 1.0
    rast$lai[mask][cond] = 0.0
    rast$impervious[mask][cond] = 0.0

writeRAST(rast,'vegid',zcol='vegid',overwrite=T)
writeRAST(rast,'landuse',zcol='landuse',overwrite=T)
writeRAST(rast,'coverFrac',zcol='coverFrac',overwrite=T)
writeRAST(rast,'lai',zcol='lai',overwrite=T)
writeRAST(rast,'impervious',zcol='impervious',overwrite=T)