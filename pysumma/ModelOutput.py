class ModelOutput:
    def __init__(self, filepath):
        self.filepath = filepath
        self.text = self.read_file()
        self.var_choices = ['numStats', 'maxFreq', 'ixVal', 'iLength', 'iLook_decision', 'simulStart', 'simulFinsh',
                         'soilCatTbl', 'vegeParTbl', 'soilStress', 'stomResist', 'bbTempFunc', 'bbHumdFunc',
                         'bbElecFunc', 'bbCO2point', 'bbNumerics', 'bbAssimFnc', 'bbCanIntg8', 'num_method',
                         'fDerivMeth', 'LAI_method', 'cIntercept', 'f_Richards', 'groundwatr', 'hc_profile',
                         'bcUpprTdyn', 'bcLowrTdyn', 'bcUpprSoiH', 'bcLowrSoiH', 'veg_traits', 'rootProfil',
                            'canopyEmis', 'snowIncept', 'windPrfile', 'astability', 'canopySrad', 'alb_method',
                            'snowLayers', 'compaction', 'thCondSnow', 'thCondSoil', 'spatial_gw', 'subRouting',
                            'snowDenNew', 'iLook_time', 'iyyy', 'im', 'id', 'ih', 'imin', 'iLook_force', 'time', 'pptrate',
                            'airtemp', 'spechum', 'windspd', 'SWRadAtm', 'LWRadAtm', 'airpres', 'iLook_attr', 'latitude',
                            'longitude', 'elevation', 'tan_slope', 'contourLength', 'HRUarea', 'mHeight', 'iLook_type',
                            'hruIndex', 'vegTypeIndex', 'soilTypeIndex', 'slopeTypeIndex', 'downHRUindex', 'iLook_param',
                            'upperBoundHead', 'lowerBoundHead', 'upperBoundTheta', 'lowerBoundTheta', 'upperBoundTemp',
                            'lowerBoundTemp', 'tempCritRain', 'tempRangeTimestep', 'frozenPrecipMultip', 'snowfrz_scale',
                            'fixedThermalCond_snow', 'albedoMax', 'albedoMinWinter', 'albedoMinSpring', 'albedoMaxVisible',
                            'albedoMinVisible', 'albedoMaxNearIR', 'albedoMinNearIR', 'albedoDecayRate', 'albedoSootLoad',
                            'albedoRefresh', 'radExt_snow', 'directScale', 'Frad_direct', 'Frad_vis', 'newSnowDenMin',
                            'newSnowDenMult', 'newSnowDenScal', 'constSnowDen', 'newSnowDenAdd', 'newSnowDenMultTemp',
                            'newSnowDenMultWind', 'newSnowDenMultAnd', 'newSnowDenBase', 'densScalGrowth',
                            'tempScalGrowth', 'grainGrowthRate', 'densScalOvrbdn', 'tempScalOvrbdn', 'baseViscosity',
                            'Fcapil', 'k_snow', 'mw_exp', 'z0Snow', 'z0Soil', 'z0Canopy', 'zpdFraction', 'critRichNumber',
                            'Louis79_bparam', 'Louis79_cStar', 'Mahrt87_eScale', 'leafExchangeCoeff', 'windReductionParam',
                            'Kc25', 'Ko25', 'Kc_qFac', 'Ko_qFac', 'kc_Ha', 'ko_Ha', 'vcmax25_canopyTop', 'vcmax_qFac',
                            'vcmax_Ha', 'vcmax_Hd', 'vcmax_Sv', 'vcmax_Kn', 'jmax25_scale', 'jmax_Ha', 'jmax_Hd',
                            'jmax_Sv', 'fractionJ', 'quantamYield', 'vpScaleFactor', 'cond2photo_slope',
                            'minStomatalConductance', 'winterSAI', 'summerLAI', 'rootScaleFactor1', 'rootScaleFactor2',
                            'rootingDepth', 'rootDistExp', 'plantWiltPsi', 'soilStressParam', 'critSoilWilting',
                            'critSoilTranspire', 'critAquiferTranspire', 'minStomatalResistance', 'leafDimension',
                            'heightCanopyTop', 'heightCanopyBottom', 'specificHeatVeg', 'maxMassVegetation',
                            'throughfallScaleSnow', 'throughfallScaleRain', 'refInterceptCapSnow', 'refInterceptCapRain',
                            'snowUnloadingCoeff', 'canopyDrainageCoeff', 'ratioDrip2Unloading', 'canopyWettingFactor',
                            'canopyWettingExp', 'soil_dens_intr', 'thCond_soil', 'frac_sand', 'frac_silt', 'frac_clay',
                            'fieldCapacity', 'wettingFrontSuction', 'theta_mp', 'theta_sat', 'theta_res', 'vGn_alpha',
                            'vGn_n', 'mpExp', 'k_soil', 'k_macropore', 'kAnisotropic', 'zScale_TOPMODEL', 'compactedDepth',
                            'aquiferScaleFactor', 'aquiferBaseflowExp', 'qSurfScale', 'specificYield', 'specificStorage',
                            'f_impede', 'soilIceScale', 'soilIceCV', 'minwind', 'minstep', 'maxstep', 'wimplicit',
                            'maxiter', 'relConvTol_liquid', 'absConvTol_liquid', 'relConvTol_matric', 'absConvTol_matric',
                            'relConvTol_energy', 'absConvTol_energy', 'relConvTol_aquifr', 'absConvTol_aquifr', 'zmin',
                            'zmax', 'zminLayer1', 'zminLayer2', 'zminLayer3', 'zminLayer4', 'zminLayer5',
                            'zmaxLayer1_lower', 'zmaxLayer2_lower', 'zmaxLayer3_lower', 'zmaxLayer4_lower',
                            'zmaxLayer1_upper', 'zmaxLayer2_upper', 'zmaxLayer3_upper', 'zmaxLayer4_upper', 'iLook_prog',
                            'dt_init', 'scalarCanopyIce', 'scalarCanopyLiq', 'scalarCanopyWat', 'scalarCanairTemp',
                            'scalarCanopyTemp', 'spectralSnowAlbedoDiffuse', 'scalarSnowAlbedo', 'scalarSnowDepth',
                            'scalarSWE', 'scalarSfcMeltPond', 'mLayerTemp', 'mLayerVolFracIce', 'mLayerVolFracLiq',
                            'mLayerVolFracWat', 'mLayerMatricHead', 'scalarAquiferStorage', 'scalarSurfaceTemp',
                            'mLayerDepth', 'mLayerHeight', 'iLayerHeight', 'iLook_diag', 'scalarCanopyDepth',
                            'scalarGreenVegFraction', 'scalarBulkVolHeatCapVeg', 'scalarCanopyEmissivity',
                            'scalarRootZoneTemp', 'scalarLAI', 'scalarSAI', 'scalarExposedLAI', 'scalarExposedSAI',
                            'scalarCanopyIceMax', 'scalarCanopyLiqMax', 'scalarGrowingSeasonIndex', 'scalarVolHtCap_air',
                            'scalarVolHtCap_ice', 'scalarVolHtCap_soil', 'scalarVolHtCap_water', 'mLayerVolHtCapBulk',
                            'scalarLambda_drysoil', 'scalarLambda_wetsoil', 'mLayerThermalC', 'iLayerThermalC',
                            'scalarVPair', 'scalarVP_CanopyAir', 'scalarTwetbulb', 'scalarSnowfallTemp',
                            'scalarNewSnowDensity', 'scalarO2air', 'scalarCO2air', 'scalarCosZenith',
                            'scalarFractionDirect', 'scalarCanopySunlitFraction', 'scalarCanopySunlitLAI',
                            'scalarCanopyShadedLAI', 'spectralAlbGndDirect', 'spectralAlbGndDiffuse', 'scalarGroundAlbedo',
                            'scalarLatHeatSubVapCanopy', 'scalarLatHeatSubVapGround', 'scalarSatVP_CanopyTemp',
                            'scalarSatVP_GroundTemp', 'scalarZ0Canopy', 'scalarWindReductionFactor',
                            'scalarZeroPlaneDisplacement', 'scalarRiBulkCanopy', 'scalarRiBulkGround',
                            'scalarCanopyStabilityCorrection', 'scalarGroundStabilityCorrection',
                            'scalarIntercellularCO2Sunlit', 'scalarIntercellularCO2Shaded', 'scalarTranspireLim',
                            'scalarTranspireLimAqfr', 'scalarFoliageNitrogenFactor', 'scalarSoilRelHumidity',
                            'mLayerTranspireLim', 'mLayerRootDensity', 'scalarAquiferRootFrac', 'scalarFracLiqVeg',
                            'scalarCanopyWetFraction', 'scalarSnowAge', 'scalarGroundSnowFraction',
                            'spectralSnowAlbedoDirect', 'mLayerFracLiqSnow', 'mLayerThetaResid', 'mLayerPoreSpace',
                            'mLayerMeltFreeze', 'scalarInfilArea', 'scalarFrozenArea', 'scalarSoilControl',
                            'mLayerVolFracAir', 'mLayerTcrit', 'mLayerCompress', 'scalarSoilCompress',
                            'mLayerMatricHeadLiq', 'scalarSoilWatBalError', 'scalarAquiferBalError', 'scalarTotalSoilLiq',
                            'scalarTotalSoilIce', 'scalarVGn_m', 'scalarKappa', 'scalarVolLatHt_fus', 'numFluxCalls',
                            'iLook_flux', 'scalarCanairNetNrgFlux', 'scalarCanopyNetNrgFlux', 'scalarGroundNetNrgFlux',
                            'scalarCanopyNetLiqFlux', 'scalarRainfall', 'scalarSnowfall', 'spectralIncomingDirect',
                            'spectralIncomingDiffuse', 'scalarCanopySunlitPAR', 'scalarCanopyShadedPAR',
                            'spectralBelowCanopyDirect', 'spectralBelowCanopyDiffuse', 'scalarBelowCanopySolar',
                            'scalarCanopyAbsorbedSolar', 'scalarGroundAbsorbedSolar', 'scalarLWRadCanopy',
                            'scalarLWRadGround', 'scalarLWRadUbound2Canopy', 'scalarLWRadUbound2Ground',
                            'scalarLWRadUbound2Ubound', 'scalarLWRadCanopy2Ubound', 'scalarLWRadCanopy2Ground',
                            'scalarLWRadCanopy2Canopy', 'scalarLWRadGround2Ubound', 'scalarLWRadGround2Canopy',
                            'scalarLWNetCanopy', 'scalarLWNetGround', 'scalarLWNetUbound', 'scalarEddyDiffusCanopyTop',
                            'scalarFrictionVelocity', 'scalarWindspdCanopyTop', 'scalarWindspdCanopyBottom',
                            'scalarGroundResistance', 'scalarCanopyResistance', 'scalarLeafResistance',
                            'scalarSoilResistance', 'scalarSenHeatTotal', 'scalarSenHeatCanopy', 'scalarSenHeatGround',
                            'scalarLatHeatTotal', 'scalarLatHeatCanopyEvap', 'scalarLatHeatCanopyTrans',
                            'scalarLatHeatGround', 'scalarCanopyAdvectiveHeatFlux', 'scalarGroundAdvectiveHeatFlux',
                            'scalarCanopySublimation', 'scalarSnowSublimation', 'scalarStomResistSunlit',
                            'scalarStomResistShaded', 'scalarPhotosynthesisSunlit', 'scalarPhotosynthesisShaded',
                            'scalarCanopyTranspiration', 'scalarCanopyEvaporation', 'scalarGroundEvaporation',
                            'mLayerTranspire', 'scalarThroughfallSnow', 'scalarThroughfallRain',
                            'scalarCanopySnowUnloading', 'scalarCanopyLiqDrainage', 'scalarCanopyMeltFreeze',
                            'iLayerConductiveFlux', 'iLayerAdvectiveFlux', 'iLayerNrgFlux', 'mLayerNrgFlux',
                            'scalarSnowDrainage', 'iLayerLiqFluxSnow', 'mLayerLiqFluxSnow', 'scalarRainPlusMelt',
                            'scalarMaxInfilRate', 'scalarInfiltration', 'scalarExfiltration', 'scalarSurfaceRunoff',
                            'mLayerSatHydCondMP', 'mLayerSatHydCond', 'iLayerSatHydCond', 'mLayerHydCond',
                            'iLayerLiqFluxSoil', 'mLayerLiqFluxSoil', 'mLayerBaseflow', 'mLayerColumnInflow',
                            'mLayerColumnOutflow', 'scalarSoilBaseflow', 'scalarSoilDrainage', 'scalarAquiferRecharge',
                            'scalarAquiferTranspire', 'scalarAquiferBaseflow', 'iLook_deriv', 'dCanairNetFlux_dCanairTemp',
                            'dCanairNetFlux_dCanopyTemp', 'dCanairNetFlux_dGroundTemp', 'dCanopyNetFlux_dCanairTemp',
                            'dCanopyNetFlux_dCanopyTemp', 'dCanopyNetFlux_dGroundTemp', 'dCanopyNetFlux_dCanLiq',
                            'dGroundNetFlux_dCanairTemp', 'dGroundNetFlux_dCanopyTemp', 'dGroundNetFlux_dGroundTemp',
                            'dGroundNetFlux_dCanLiq', 'dCanopyEvaporation_dTCanair', 'dCanopyEvaporation_dTCanopy',
                            'dCanopyEvaporation_dTGround', 'dCanopyEvaporation_dCanLiq', 'dGroundEvaporation_dTCanair',
                            'dGroundEvaporation_dTCanopy', 'dGroundEvaporation_dTGround', 'dGroundEvaporation_dCanLiq',
                            'dTheta_dTkCanopy', 'dCanLiq_dTcanopy', 'scalarCanopyLiqDeriv', 'scalarThroughfallRainDeriv',
                            'scalarCanopyLiqDrainageDeriv', 'dNrgFlux_dTempAbove', 'dNrgFlux_dTempBelow',
                            'iLayerLiqFluxSnowDeriv', 'dVolTot_dPsi0', 'dq_dHydStateAbove', 'dq_dHydStateBelow',
                            'mLayerdTheta_dPsi', 'mLayerdPsi_dTheta', 'dCompress_dPsi', 'dq_dNrgStateAbove',
                            'dq_dNrgStateBelow', 'mLayerdTheta_dTk', 'dPsiLiq_dTemp', 'dPsiLiq_dPsi0', 'iLook_index',
                            'nSnow', 'nSoil', 'nLayers', 'layerType', 'nCasNrg', 'nVegNrg', 'nVegMass', 'nVegState',
                            'nNrgState', 'nWatState', 'nMatState', 'nMassState', 'nState', 'nSnowSoilNrg', 'nSnowOnlyNrg',
                            'nSoilOnlyNrg', 'nSnowSoilHyd', 'nSnowOnlyHyd', 'nSoilOnlyHyd', 'ixControlVolume',
                            'ixDomainType', 'ixStateType', 'ixHydType', 'ixDomainType_subset', 'ixStateType_subset',
                            'ixMapFull2Subset', 'ixMapSubset2Full', 'ixCasNrg', 'ixVegNrg', 'ixVegHyd', 'ixTopNrg',
                            'ixTopHyd', 'ixNrgOnly', 'ixHydOnly', 'ixMatOnly', 'ixMassOnly', 'ixSnowSoilNrg',
                            'ixSnowOnlyNrg', 'ixSoilOnlyNrg', 'ixSnowSoilHyd', 'ixSnowOnlyHyd', 'ixSoilOnlyHyd',
                            'ixNrgCanair', 'ixNrgCanopy', 'ixHydCanopy', 'ixNrgLayer', 'ixHydLayer', 'ixVolFracWat',
                            'ixMatricHead', 'ixAllState', 'ixSoilState', 'ixLayerState', 'midSnowStartIndex',
                            'midSoilStartIndex', 'midTotoStartIndex', 'ifcSnowStartIndex', 'ifcSoilStartIndex',
                            'ifcTotoStartIndex', 'iLook_bpar', 'basin__aquiferHydCond', 'basin__aquiferScaleFactor',
                            'basin__aquiferBaseflowExp', 'routingGammaShape', 'routingGammaScale', 'iLook_bvar',
                            'basin__totalArea', 'basin__SurfaceRunoff', 'basin__ColumnOutflow', 'basin__AquiferStorage',
                            'basin__AquiferRecharge', 'basin__AquiferBaseflow', 'basin__AquiferTranspire',
                            'routingRunoffFuture', 'routingFractionFuture', 'averageInstantRunoff', 'averageRoutedRunoff',
                            'iLook_varType', 'scalarv', 'wLength', 'midSnow', 'midSoil', 'midToto', 'ifcSnow', 'ifcSoil',
                            'ifcToto', 'parSoil', 'routing', 'outstat', 'unknown', 'iLook_stat', 'totl', 'inst', 'mean',
                            'vari', 'mini', 'maxi', 'mode', 'iLookDECISIONS', 'iLookTIME', 'iLookFORCE', 'iLookATTR',
                            'iLookTYPE', 'iLookPARAM', 'iLookPROG', 'iLookDIAG', 'iLookFLUX', 'iLookDERIV', 'iLookINDEX',
                         'iLookBPAR', 'iLookBVAR', 'iLookVarType', 'iLookStat', 'maxvarDecisions', 'maxvarTime',
                         'maxvarForc', 'maxvarAttr', 'maxvarType', 'maxvarMpar', 'maxvarProg', 'maxvarDiag',
                         'maxvarFlux', 'maxvarDeriv', 'maxvarIndx', 'maxvarBpar', 'maxvarBvar', 'maxvarVarType',
                         'maxvarStat', 'childFLUX_MEAN(:)']

    # Writes <variable> to ModelOutput.txt iff it's a valid choice AND not already in the file
    def write_variable_to_file(self, variable):
        if variable not in self.var_choices:
            print("Not a valid variable.")
        elif self.check_for_variable(variable):
            print("Variable already in output file.")
        else:
            with open(self.filepath, 'a') as file:
                file.write(variable + " | ")

    # Returns the entire text of the file at self.filepath
    def read_file(self):
        with open(self.filepath, 'rt') as f:
            return f.readlines()

    # If <variable> is in the file, return TRUE. Else, return FALSE
    def check_for_variable(self, variable):
        self.text = self.read_file()
        if variable in self.text:
            return True
        else:
            return False

    # Removes the line ascribed to <variable>
    def remove_variable(self, variable):
        self.text = self.read_file()
        output_text = []
        for line in self.text:
            # If <variable> = the first element on the line (before |)
            if variable.equals(line.split('|')[0].strip()):
                output_text += line
        # Write the new text (without the line with <variable>) to <filepath>
        with open(self.filepath, 'w') as file:
            file.writelines(output_text)