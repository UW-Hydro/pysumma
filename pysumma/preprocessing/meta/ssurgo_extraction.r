mapunitTitle=c('musym','muname','mukind','mustatus','muacres','mapunitlfw_l','mapunitlfw_r','mapunitlfw_h','mapunitpfa_l','mapunitpfa_r','mapunitpfa_h','farmlndcl','muhelcl','muwathelcl','muwndhelcl','interpfocus','invesintens','iacornsr','nhiforsoigrp','nhspiagr','vtsepticsyscl','mucertstat','lkey','mukey')
compTitle=c('comppct_l','comppct_r','comppct_h','compname','compkind','majcompflag','otherph','localphase','slope_l','slope_r','slope_h','slopelenusle_l','slopelenusle_r','slopelenusle_h','runoff','tfact','wei','weg','erocl','earthcovkind1','earthcovkind2','hydricon','hydricrating','drainagecl','elev_l','elev_r','elev_h','aspectccwise','aspectrep','aspectcwise','geomdesc','albedodry_l','albedodry_r','albedodry_h','airtempa_l','airtempa_r','airtempa_h','map_l','map_r','map_h','reannualprecip_l','reannualprecip_r','reannualprecip_h','ffd_l','ffd_r','ffd_h','nirrcapcl','nirrcapscl','nirrcapunit','irrcapcl','irrcapscl','irrcapunit','cropprodindex','constreeshrubgrp','wndbrksuitgrp','rsprod_l','rsprod_r','rsprod_h','foragesuitgrpid','wlgrain','wlgrass','wlherbaceous','wlshrub','wlconiferous','wlhardwood','wlwetplant','wlshallowwat','wlrangeland','wlopenland','wlwoodland','wlwetland','soilslippot','frostact','initsub_l','initsub_r','initsub_h','totalsub_l','totalsub_r','totalsub_h','hydgrp','corcon','corsteel','taxclname','taxorder','taxsuborder','taxgrtgroup','taxsubgrp','taxpartsize','taxpartsizemod','taxceactcl','taxreaction','taxtempcl','taxmoistscl','taxtempregime','soiltaxedition','castorieindex','flecolcomnum','flhe','flphe','flsoilleachpot','flsoirunoffpot','fltemik2use','fltriumph2use','indraingrp','innitrateleachi','misoimgmtgrp','vasoimgtgrp','mukey','cokey')
chorizonTitle = c('hzname','desgndisc','desgnmaster','desgnmasterprime','desgnvert','hzdept_l','hzdept_r','hzdept_h','hzdepb_l','hzdepb_r','hzdepb_h','hzthk_l','hzthk_r','hzthk_h','fraggt10_l','fraggt10_r','fraggt10_h','frag3to10_l','frag3to10_r','frag3to10_h','sieveno4_l','sieveno4_r','sieveno4_h','sieveno10_l','sieveno10_r','sieveno10_h','sieveno40_l','sieveno40_r','sieveno40_h','sieveno200_l','sieveno200_r','sieveno200_h','sandtotal_l','sandtotal_r','sandtotal_h','sandvc_l','sandvc_r','sandvc_h','sandco_l','sandco_r','sandco_h','sandmed_l','sandmed_r','sandmed_h','sandfine_l','sandfine_r','sandfine_h','sandvf_l','sandvf_r','sandvf_h','silttotal_l','silttotal_r','silttotal_h','siltco_l','siltco_r','siltco_h','siltfine_l','siltfine_r','siltfine_h','claytotal_l','claytotal_r','claytotal_h','claysizedcarb_l','claysizedcarb_r','claysizedcarb_h','om_l','om_r','om_h','dbtenthbar_l','dbtenthbar_r','dbtenthbar_h','dbthirdbar_l','dbthirdbar_r','dbthirdbar_h','dbfifteenbar_l','dbfifteenbar_r','dbfifteenbar_h','dbovendry_l','dbovendry_r','dbovendry_h','partdensity','ksat_l','ksat_r','ksat_h','awc_l','awc_r','awc_h','wtenthbar_l','wtenthbar_r','wtenthbar_h','wthirdbar_l','wthirdbar_r','wthirdbar_h','wfifteenbar_l','wfifteenbar_r','wfifteenbar_h','wsatiated_l','wsatiated_r','wsatiated_h','lep_l','lep_r','lep_h','ll_l','ll_r','ll_h','pi_l','pi_r','pi_h','aashind_l','aashind_r','aashind_h','kwfact','kffact','caco3_l','caco3_r','caco3_h','gypsum_l','gypsum_r','gypsum_h','sar_l','sar_r','sar_h','ec_l','ec_r','ec_h','cec7_l','cec7_r','cec7_h','ecec_l','ecec_r','ecec_h','sumbases_l','sumbases_r','sumbases_h','ph1to1h2o_l','ph1to1h2o_r','ph1to1h2o_h','ph01mcacl2_l','ph01mcacl2_r','ph01mcacl2_h','freeiron_l','freeiron_r','freeiron_h','feoxalate_l','feoxalate_r','feoxalate_h','extracid_l','extracid_r','extracid_h','extral_l','extral_r','extral_h','aloxalate_l','aloxalate_r','aloxalate_h','pbray1_l','pbray1_r','pbray1_h','poxalate_l','poxalate_r','poxalate_h','ph2osoluble_l','ph2osoluble_r','ph2osoluble_h','ptotal_l','ptotal_r','ptotal_h','excavdifcl','excavdifms','cokey','chkey')
chtexgrpTitle=c('texture','stratextsflag','rvindicator','texdesc','chkey','chtgkey')
chtexturTitle=c('texcl','lieutex','chtgkey','chtkey')
chporesTitle=c('poreqty','poresize','porecont','poreshp','rvindicator','chkey','chporeskey')


arg=commandArgs(T)
target = paste(arg[1],'/tabular',sep='') # e.g., 'VA113/tabular'
#target = '/Volumes/LaCie/current_work/SEES/BAISMAN/raw_data/MD005/tabular/'
#target = '/Volumes/LaCie/workArch/University_of_North_Carolina/WS14/Rhessys520_src_Laurence/setup_rhessys_5_20_debug2_bolstad_zone_bgc_cwt/raw_data/NC113/tabular/'

mapunit = read.table(paste(target,'/mapunit.txt',sep=''),sep='|',stringsAsFactors=F) #mukey
colnames(mapunit) = mapunitTitle
	## 1 mukey to many componments [cokey]
comp = read.table(paste(target,'/comp.txt',sep=''),sep='|',stringsAsFactors=F) #cokey
colnames(comp) = compTitle
	## 1 cokey to many horizons [chkey]
chorizon = read.table(paste(target,'/chorizon.txt',sep=''),sep='|',stringsAsFactors=F) #chkey
colnames(chorizon) = chorizonTitle

chtexgrp = read.table(paste(target,'/chtexgrp.txt',sep=''),sep='|',stringsAsFactors=F) #chkey
colnames(chtexgrp) = chtexgrpTitle

chtextur = read.table(paste(target,'/chtextur.txt',sep=''),sep='|',stringsAsFactors=F) #chkey
colnames(chtextur) = chtexturTitle

# chpores = read.table(paste(target,'/chpores.txt',sep=''),sep='|',stringsAsFactors=F) #chkey
# colnames(chpores) = chporesTitle
#chpores # new table
	# chkey -> chorizon
	# chporeskey ->
	

## mapunit:component:horizon
## extract (weighted average[thickness] of soil horizon in a soil component; then weighted [%composition] by componments):
	# 1 permeability
	# 2 watercapacity
	# 3 bulkdensity
	# 4 saturatedhydraulicconductivity
	# 5 erodibility
	# 6 field capacity
	# 7 porosity
	# 8 soilthickness
	# 9 organ matter 
	
	# relationshup
	# 1 mukey: N cokey (componments) : N chkey (horizons)
 	#        : fraction "comppct_r"  : fraction "hzdepb_r" -> thickness


horizonOrder = c('O','A','E','B','C','R')	
soilscoreNames = c('Sand','Loamy sand','Sandy loam','Silt loam','Silt','Loam','Sandy clay loam','Silty clay loam','Clay loam','Sandy clay','Silty clay','Clay')
soilscore = c(1,2,3,4,5,6,7,8,9,10,11,12); names(soilscore)=soilscoreNames

mukey = mapunit[,'mukey']	
mukeyHold = matrix(NA,length(mukey), 20);

for(i in 1:length(mukey)){
	## for each mukey, we have N cokey
	
	cond1 = comp[,'mukey']== mukey[i]
	# sum(cond1)
	
	componentSummaryTable = as.data.frame(t(sapply( comp[cond1,'cokey'], function(cokey){
		# linking horizons to component
		
			# cokey = comp[cond1,'cokey'][3]
		
		cond2 = chorizon[,'cokey']== cokey
        horizonSummaryTable = data.frame(id = chorizon[cond2,'chkey']) 
        horizonSummaryTable$horizonThinkness = (chorizon[cond2,'hzdepb_r']-chorizon[cond2,'hzdept_r'])*0.01 #cm -> m
        horizonSummaryTable$horizonMeanDepth = 0.5*(chorizon[cond2,'hzdepb_r']+chorizon[cond2,'hzdept_r'])*0.01 # m
        horizonSummaryTable$horizonName = chorizon[cond2,'hzname']
       
        horizonSummaryTable$horizonWeight = horizonSummaryTable$horizonThinkness / sum(horizonSummaryTable$horizonThinkness, na.rm=T)
        horizonSummaryTable$ksat = chorizon[cond2,'ksat_r']*1e-6*3600*24 # m/day
        horizonSummaryTable$ksat[horizonSummaryTable$ksat<=0] = 0.001 # m/day
        horizonSummaryTable$ksat_log = log(horizonSummaryTable$ksat);
        #horizonSummaryTable$ksat_log[!is.finite(horizonSummaryTable$ksat_log)] = NA
        horizonSummaryTable$sand = chorizon[cond2,'sandtotal_r']*0.01 #% -> [0,1]
        horizonSummaryTable$silt = chorizon[cond2,'silttotal_r']*0.01 #% -> [0,1]
        horizonSummaryTable$clay = chorizon[cond2,'claytotal_r']*0.01 #% -> [0,1]
        horizonSummaryTable$POR = chorizon[cond2,'wsatiated_r']*0.01 #% -> [0,1]
        horizonSummaryTable$POR[horizonSummaryTable$POR<=0] = 0.01
        horizonSummaryTable$POR_log = log(horizonSummaryTable$POR)
        #horizonSummaryTable$POR_log[!is.finite(horizonSummaryTable$POR_log)] = NA
        horizonSummaryTable$BD = chorizon[cond2,'dbovendry_r'] #g/cm3
        horizonSummaryTable$fc = chorizon[cond2,'wthirdbar_r']*0.01 #% -> [0,1]
        horizonSummaryTable$awc = chorizon[cond2,'awc_r']*0.01 # cm/cm
        horizonSummaryTable$kffact = chorizon[cond2,'kffact'] # soil erodibility factor
        horizonSummaryTable$om = chorizon[cond2,'om_r']*0.01 #% -> [0,1]
        #horizonSummaryTable$density = chorizon[cond2,'partdensity'] # g/cm3 <<------
        horizonSummaryTable$density = horizonSummaryTable$BD / (1 - horizonSummaryTable$POR)
        	# form text book: % pore space = porosity = (1 - BD / density) * 100 %
        	# from my note: density = BD / (1 - POR)
        	
        ksatLM = NULL
        tryCatch({
        	if(dim(horizonSummaryTable)[1]<2 | sum(!is.na(horizonSummaryTable$ksat_log))<2) stop('no data')
        	ksatLM = lm(ksat_log~horizonMeanDepth, horizonSummaryTable)
        }, error=function(e){ 
        	# print(e);
        	ksatLM <<- list(coefficients=c(
        		-1/4000,
        		sum(horizonSummaryTable$horizonWeight*horizonSummaryTable$ksat_log,na.rm=T)
        	)) 
        })
        
        porLM = NULL
        tryCatch({
        	if(dim(horizonSummaryTable)[1]<2 | sum(!is.na(horizonSummaryTable$POR_log))<2 ) stop('no data')
        	porLM = lm(POR_log~horizonMeanDepth, horizonSummaryTable)
        }, error=function(e){ 
        	porLM <<- list(coefficients=c(
        		-1/4000,
        		sum(horizonSummaryTable$horizonWeight*horizonSummaryTable$POR_log,na.rm=T)
        	)) 
        })
        
        
        # dev.new()
        # plot(horizonSummaryTable $horizonMeanDepth, horizonSummaryTable $ksat_log)
        # abline(ksatLM, col='blue')
        
        deephorizonname = match(substr(gsub('[a-z0-9, ]','',horizonSummaryTable$horizonName[which.max(horizonSummaryTable$horizonMeanDepth)]),1,1), horizonOrder)
        if(length(deephorizonname)<=0) deephorizonname=NA
        
        return <- unlist(list(
        	id = cokey,
        	horizonThinkness = sum(horizonSummaryTable$horizonThinkness,na.rm=T),
        	deepHorizon = deephorizonname,
        	ksat = sum(horizonSummaryTable$horizonWeight * horizonSummaryTable$ksat, na.rm=T),
        	ksat_0 = as.numeric(exp(ksatLM$coefficients[1])),
        	ksat_decay = as.numeric(-ksatLM$coefficients[2]), # 1/m
        	vksat = sum(horizonSummaryTable$horizonThinkness,na.rm=T) / sum(horizonSummaryTable$horizonThinkness/horizonSummaryTable$ksat, na.rm=T),
        	por_0 = as.numeric(exp(porLM$coefficients[1])),
        	por_decay = as.numeric(-porLM$coefficients[2]), # 1/m
        	sand = sum(horizonSummaryTable$horizonWeight * horizonSummaryTable$sand, na.rm=T),
        	silt = sum(horizonSummaryTable$horizonWeight * horizonSummaryTable$silt, na.rm=T),
        	clay = sum(horizonSummaryTable$horizonWeight * horizonSummaryTable$clay, na.rm=T),
        	
        	BD = sum(horizonSummaryTable$horizonWeight * horizonSummaryTable$BD, na.rm=T),
        	partdensity = sum(horizonSummaryTable$horizonWeight * horizonSummaryTable$density, na.rm=T),
        	
        	fc = sum(horizonSummaryTable$horizonWeight * horizonSummaryTable$fc, na.rm=T),
        	awc = sum(horizonSummaryTable$horizonWeight * horizonSummaryTable$awc, na.rm=T),
        	kffact = sum(horizonSummaryTable$horizonWeight * horizonSummaryTable$kffact, na.rm=T),
        	om = sum(horizonSummaryTable$horizonWeight * horizonSummaryTable$om, na.rm=T)
        ))
	})))
	componentSummaryTable$por = 1 - componentSummaryTable$BD/componentSummaryTable$partdensity
	componentSummaryTable$Percent = comp[cond1,'comppct_r']
	componentSummaryTable$Weight = componentSummaryTable$Percent/sum(componentSummaryTable$Percent)
	
	
	
	## mukey soil texture class
	cond25 = chorizon[,'cokey']%in% componentSummaryTable$id
	cond3 = chtexgrp[,'chkey'] %in% chorizon[cond25,'chkey']
	cond4 = chtextur[,'chtgkey'] %in% chtexgrp[cond3,'chtgkey']
	tmp = table(soilscore[match(chtextur[cond4,1], soilscoreNames)])
	soilID_ = ifelse(length(tmp)>0, as.numeric(names(which.max(tmp))), NA)
	soilID_name = ifelse(length(tmp)>0, soilscoreNames[soilID_], NA) 
	
	
	
	## ksat and por distributions
	mydata = data.frame(depthzz = seq(0,10,0.001) )
	ksat = sapply( seq_len(dim(componentSummaryTable)[1]), function(ii){
		componentSummaryTable$ksat_0[ii]*exp(-componentSummaryTable$ksat_decay[ii]*mydata$depthzz) * componentSummaryTable$Weight[ii]
	}); 
	mydata$total_ksat = rowSums(ksat)
	mydata$total_ksat_log = log(mydata$total_ksat)
	
	PORz = sapply( seq_len(dim(componentSummaryTable)[1]), function(ii){
		componentSummaryTable$por_0[ii]*exp(-componentSummaryTable$por_decay[ii]*mydata$depthzz) * componentSummaryTable$Weight[ii]
	}); 
	mydata$total_por = rowSums(PORz)
	mydata$total_por_log = log(mydata$total_por)
	
	mukeyksatLM = lm(total_ksat_log~depthzz, mydata)
    mukeyporLM = lm(total_por_log~depthzz, mydata)
      
        
	# layout(matrix(1:2,nrow=1))
	# plot(ksat[,1], mydata$depthzz, type='l', ylim=c(10,0), xlim=c(0,0.5))
	# lines(ksat[,2], mydata$depthzz)
	# lines(mydata$total_ksat, mydata$depthzz, col='red')
	# lines(exp(mukeyksatLM$coefficients[2]*mydata$depthzz + mukeyksatLM$coefficients[1]), mydata$depthzz, col='blue' )
	
	# plot(PORz[,1], mydata$depthzz, type='l', ylim=c(10,0), xlim=c(0,0.5))
	# lines(PORz[,2], mydata$depthzz)
	# lines(mydata$total_por, mydata$depthzz, col='red')
	# lines(exp(mukeyporLM$coefficients[2]*mydata$depthzz + mukeyporLM$coefficients[1]), mydata$depthzz, col='blue' )
	
	mukey_sand = sum(componentSummaryTable$Weight*componentSummaryTable$sand,na.rm=T)
	mykey_silt = sum(componentSummaryTable$Weight*componentSummaryTable$silt,na.rm=T)
	mykey_clay = sum(componentSummaryTable$Weight*componentSummaryTable$clay,na.rm=T)
	mykey_total = mukey_sand + mykey_silt + mykey_clay
		mukey_sand = mukey_sand/mykey_total
		mykey_silt = mykey_silt/mykey_total
		mykey_clay = mykey_clay/mykey_total
	
	tmp = unlist(list(
		mukey = mukey[i],
		rhessys_soilid = soilID_,
		#soil_name = soilID_name,
		soilDepth = sum(componentSummaryTable$Weight*componentSummaryTable$horizonThinkness,na.rm=T),
		soilhorizon = componentSummaryTable$deepHorizon[which.max(componentSummaryTable$Weight)],
		ksat = sum(componentSummaryTable$Weight*componentSummaryTable$ksat,na.rm=T),
		vksat = sum(componentSummaryTable$Weight*componentSummaryTable$vksat,na.rm=T),
		ksat_0 = as.numeric(exp(mukeyksatLM$coefficients[1])),
		ksat_decay = as.numeric(-mukeyksatLM$coefficients[2]),
		por = sum(componentSummaryTable$Weight*componentSummaryTable$por,na.rm=T),
		por_0 = as.numeric(exp(mukeyporLM$coefficients[1])),
		por_decay = as.numeric(-mukeyporLM$coefficients[2]),
		sand = mukey_sand,
		silt = mykey_silt,
		clay = mykey_clay,
		BD = sum(componentSummaryTable$Weight*componentSummaryTable$BD,na.rm=T),
		partdensity = sum(componentSummaryTable$Weight*componentSummaryTable$partdensity,na.rm=T),
		fc = sum(componentSummaryTable$Weight*componentSummaryTable$fc,na.rm=T),
		awc = sum(componentSummaryTable$Weight*componentSummaryTable$awc,na.rm=T),
		kffact = sum(componentSummaryTable$Weight*componentSummaryTable$kffact,na.rm=T),
		om = sum(componentSummaryTable$Weight*componentSummaryTable$om,na.rm=T)
	))
	mukeyHold[i,] = tmp
	if(i==1) colnames(mukeyHold)=names(tmp)
	
}#i
# write.csv(mukeyHold, paste('~/Downloads/soil_mukey_texture.csv',sep=''),row.names=F)
write.csv(mukeyHold, paste(arg[1],'/soil_mukey_texture.csv',sep=''),row.names=F)