arg=commandArgs(T)


library(sp)
library(XML)
library(rgrass7)
library(rgdal)
tryCatch({ use_sp() },error=function(cond){message(cond)},warning=function(cond){message(cond)},finally={message("Please update the rgrass7 package on R")})

rast = readRAST('soil_ssurgo')
soil_cat_mukey = arg[1] 
soil_mukey_texture = arg[2]
if(length(arg)>2){ suffix = arg[3]; } else { suffix=''; }

cat_mukey = read.csv(soil_cat_mukey, stringsAsFactors=F,header=F)
if( is.numeric(cat_mukey[1,1]) ){
    colnames(cat_mukey) = c('x','y','cat','MUKEY')
}else{
    cat_mukey = read.csv(soil_cat_mukey, stringsAsFactors=F)
}

mukey_texture = read.csv(soil_mukey_texture, stringsAsFactors=F)
	
	# matching SSURGO dataset product to the mapping mukey
	cond = match(cat_mukey[,'MUKEY'],mukey_texture[,'mukey'])
	cat_texture = mukey_texture[cond,'rhessys_soilid']
	
	# sorting matched mukey to the map organization
	cond2 = match(rast@data[[1]], cat_mukey[,'cat'])
	rast$soil_texture = as.integer(cat_texture[cond2]); writeRAST(rast,paste('soil_texture',suffix,sep=''),zcol='soil_texture',overwrite=T)
	
	## more variable
    cat_texture = mukey_texture[cond,'mukey']
    rast$soil_texture = cat_texture[cond2]; writeRAST(rast,'mukey',zcol='soil_texture',overwrite=T)

    cat_texture = mukey_texture[cond,'rhessys_soilid']
    rast$soil_texture = cat_texture[cond2]; writeRAST(rast,'soil_id',zcol='soil_texture',overwrite=T)	