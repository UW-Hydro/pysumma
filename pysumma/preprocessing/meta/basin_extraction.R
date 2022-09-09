library(rgrass7)
library(sp)
tryCatch({ use_sp() },error=function(cond){message(cond)},warning=function(cond){message(cond)},finally={message("Please update the rgrass7 package on R")})
rast=readRAST(c('tmp','basin_','sub_','hill_','str_','drain'))
mask = !is.na(rast@data[[1]]) # use sub as mask
basin=rast@data[[2]][mask]
sub=rast@data[[3]][mask]
hill=rast@data[[4]][mask]
str=rast@data[[5]][mask]
strCOND = !is.na(str)
drain=rast@data[[6]][mask]

rast2=readRAST(c('rowmap','colmap'))
rows = rast2@data[[1]][mask]
cols = rast2@data[[2]][mask]
	strRows = rows[strCOND]
	strCols = cols[strCOND]
	strDRAIN = abs(drain[strCOND])
maxCol = max(cols,na.rm=T)
maskRC = rows*maxCol+cols 
maskRC_string2Index <- new.env(hash=T)
    list2env(setNames(as.list(sub),maskRC),envir=maskRC_string2Index) #<<---- native R hash 
     
    
# ... which sub contain D8basin
index = tapply(seq_along(sub),sub,function(ii){ ii })
index_partial = tapply(seq_along(sub),sub,function(ii){ ii[ !is.na(basin[ii]) ] })
basin_sub = tapply(seq_along(sub),sub,function(ii){ sum(basin[ii],na.rm=T)/length(ii) })
selected_basin_sub = as.numeric(names(basin_sub)[basin_sub>0])
selected_basin_sub_index = match(selected_basin_sub, as.numeric(names(basin_sub)) )
# sapply(seq_along(index),function(k){length(index[[k]])})
# sapply(seq_along(index_partial),function(k){length(index_partial[[k]])})

# ... stream network structure
# 1.  2. 3.  4. 5.  6. 7.  8. (GRASS from current drainTO code order)
# NE, N, NW, W, SW, S, SE, E
colneighbor = c(1,    0,    -1,    -1,    -1,    0,    1,    1)
rowneighbor = c(-1,    -1,    -1,    0,    1,    1,    1,    0)
downstrRC = 
	sapply(seq_along(strRows), FUN=function(x){strRows[x]+rowneighbor[strDRAIN[x] ] }) * maxCol + 
	sapply(seq_along(strCols), FUN=function(x){strCols[x]+colneighbor[strDRAIN[x] ] })

    
    currentstrSUB =  sapply(maskRC[strCOND], function(x){
    		hh = maskRC_string2Index[[ toString(x) ]]
    		return <- ifelse(is.null(hh),NA,hh);
    })

   	downstrSUB =  sapply(downstrRC, function(x){
    		hh = maskRC_string2Index[[ toString(x) ]]
    		return <- ifelse(is.null(hh),NA,hh);
    })
	downstrSUB[is.na(downstrSUB)] = -1

	cond_ = currentstrSUB != downstrSUB
	selectedSUBs = currentstrSUB[cond_]
	selectedSUBs_down = downstrSUB[cond_]
	selectedSUBs_order = match(selected_basin_sub, selectedSUBs)
	
	
# ... SUB to basin
rast$tmp = rep(NA,length(mask))
for( ii in seq_along(selected_basin_sub) ){
	
	if(selectedSUBs_down[selectedSUBs_order[ii]] %in% selected_basin_sub){
		# upslope sub
        rast$tmp[mask][ index[[ selected_basin_sub_index[ii] ]] ] = 1
	}else{
        # outlet sub
        rast$tmp[mask][ index_partial[[ selected_basin_sub_index[ii] ]] ] = 1
	}

}#ii
basinCond = !is.na(rast$tmp[mask]) 
writeRAST(rast,"basin",zcol='tmp', overwrite=T)

rast$tmp = rep(NA,length(mask))
rast$tmp[mask][basinCond] = sub[basinCond]
writeRAST(rast,"sub",zcol='tmp', overwrite=T)

rast$tmp = rep(NA,length(mask))
rast$tmp[mask][basinCond] = hill[basinCond]
writeRAST(rast,"hill",zcol='tmp', overwrite=T)

rast$tmp = rep(NA,length(mask))
rast$tmp[mask][basinCond] = str[basinCond]
writeRAST(rast,"str",zcol='tmp', overwrite=T)

# rast$tmp = rep(NA,length(mask))
# rast$tmp[mask][basinCond] = maskRC[basinCond]
# writeRAST(rast,"patch",zcol='tmp', overwrite=T)




