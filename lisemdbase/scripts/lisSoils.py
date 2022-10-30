# lisemDBASEgenerator
# global vraiables and initialisation
#
# author: V.G.Jetten @ 2022
# University of Twente, Faculty ITC
# this software has copyright model: GPLV3
# this software has a disclaimer

from pcraster import *
from pcraster.framework import *
from owslib.wcs import WebCoverageService
import lisGlobals as lg


class GetSoilGridsLayer:
    "downbloading a SOILGRIDS layer from WCS service"
    def __init__(
    self, x = 0, i=1, j = 1):
        varname = lg.SG_names_[x]
        self.debug = 0 #Debug_

        if i == 1: ID='_0-5cm_mean'
        if i == 2: ID='_5-15cm_mean'
        if i == 3: ID='_15-30cm_mean'
        if i == 4: ID='_30-60cm_mean'
        if i == 5: ID='_60-100cm_mean'
        if i == 6: ID='_100-200cm_mean'

        #if self.debug == 1:
        print("   => Downloading for soil layer "+str(i)+": "+varname+ID, flush=True)

        ESPGs = 'urn:ogc:def:crs:EPSG::{0}'.format(lg.ESPG)

        if self.debug == 1:
            print("Mask ESPG and bounding box:"+ESPG,lg.maskbox,lg.dx,lg.dy, flush=True) 

        if self.debug == 1:
            print("Open SOILGRIDS WCS: "+varname, flush=True)

        url = "http://maps.isric.org/mapserv?map=/map/{}.map".format(varname)
        wcs = WebCoverageService(url, version='1.0.0')
        if self.debug == 1:
            cov_list = list(wcs.contents)
            mean_covs = [k for k in wcs.contents.keys() if k.find("mean") != -1]
            print(mean_covs, flush = True)

        variable = varname+ID
        varout = varname+str(j)
        outputnametif = "{0}.tif".format(varout)
        outputnamemap = "{0}.map".format(varout)

        if self.debug == 1:
            print("Downloading "+variable, flush=True)
        dx1 = lg.dx
        # get data as temp geotif and save to disk
        response = wcs.getCoverage(identifier=variable,crs=ESPGs,bbox=lg.maskbox,resx=dx1,resy=dx1,format='GEOTIFF_INT16')
        with open(outputnametif, 'wb') as file:
             file.write(response.read())
             
             
             

### ---------- class PedoTranfer() ---------- ###


class SoilGridsTransform(StaticModel):
    def __init__(self, mask=0, mapnr=1, layer=1):
        StaticModel.__init__(self)
    def initial(self):
        DEM = lg.DEM_
        mask = lg.mask_
        xs = str(lg.layer_)
        mapnr = lg.mapnr_
        name = ""
        factor = 1.0

        if mapnr == 0: name = "sand{0}".format(xs); factor = 0.001  # fraction sand, server gives g/kg
        if mapnr == 1: name = "clay{0}".format(xs); factor = 0.001  # fraction silt, server gives g/kg
        if mapnr == 2: name = "silt{0}".format(xs); factor = 0.001  # fraction clay, server gives g/kg
        if mapnr == 3: name = "soc{0}".format(xs);  factor = 0.0001 # fraction SOC, server give dg/kg
        if mapnr == 4: name = "cfvo{0}".format(xs); factor = 0.001  # fraction gravel, server gives cm3/dm3
        if mapnr == 5: name = "bdod{0}".format(xs); factor = 10     # bulk density kg/m3, server gives cg/cm3 

        nametif = name+".tif"
        namemap2 = name+".map"
        nt = name+"_.tif"
        
        # open the tif and create PCRaster copy      
        map_ = scalar(readmap(nametif))
        # give the missing areas the value nominal 1, the rest 0
        mapmask = ifthenelse(map_ > 1e-5,0,nominal(1))
        # isolate the pixels arounf the missing value, 1 cell thick
        edge = ifthen(spread(mapmask,0,1) == 3*celllength(), map_)
        # interpolate into the missing areas with the edge cell values, ID weight 1
        map1 = inversedistance(boolean(mapmask),edge,1,0,0)                
        # combine the original and the ID map into one and save
        map2 = cover(ifthen(map_ > 1e-5,map_),map1)*factor
        
        if lg.doProcessesSGAverage == 1 :
            map2 = windowaverage(map2, 250) #3*celllength())
                
        report(map2,namemap2)
        

### ---------- class PedoTranfer() ---------- ###

class PedoTransfer(StaticModel):
    # creates infiltration input vars: Ksat 1,2; Thetas1,2; Thetai1,2; Psi1,2
    # from SOILGRID.ORG GTiff maps for texture, org matter, gravel and bulkdensity
    # Using Saxton And Rawls 2006 pedotransferfunctions
    # https://hrsl.ba.ars.usda.gov/SPAW/Index.htm
    def __init__(self,mask=0,layer=1,moisture=0):
        StaticModel.__init__(self)
    def initial(self):
        standardBD = scalar(lg.standardbulkdensity_)  # standard bulk dens assumed by saxton and rawls. High! 1350 would be better
        #standardBD2 = scalar(standardbulkdensity2_)  # standard bulk dens assumed by saxton and rawls. High! 1350 would be better
        fractionmoisture = scalar(lg.initmoisture_)   #inital moisture as fraction between porosity and field capacity
        x = lg.layer_
        mask = lg.mask_
        DEM = lg.DEM_
        xs = str(x)
 
        S1 = readmap("sand{0}.map".format(xs))  # sand g/kg
        Si1 = readmap("silt{0}.map".format(xs)) # silt g/kg
        C1 = readmap("clay{0}.map".format(xs))  # clay g/kg
        OC1 = readmap("soc{0}.map".format(xs))  # organic carbon in dg/kg
        Grv = readmap("cfvo{0}.map".format(xs)) # coarse fragments cm3/dm3,
        bdod = readmap("bdod{0}.map".format(xs)) # bulk density in cg/m3 so kg/m3 = *0.1

        #output map name strings
        om1 = "om{0}.map".format(xs)             # organic matter in %
        WP1 = "wilting{0}.map".format(xs)      	# wilting point moisture content
        FC1 = "fieldcap{0}.map".format(xs)     	# field capacity moisture content
        PAW1 = "plantAVW{0}.map".format(xs)    	# plant available water content
        #K1 = "k{0}.map".format(xs)  		        #USLE erodibility
        BD1 = "bulkdens{0}.map".format(xs)       # bulk density in kg/m3
        Pore1 = lg.poreName+"{0}.map".format(xs)   	#porosity (cm3/cm3)
        Ksat1 = lg.ksatName+"{0}.map".format(xs)      	#ksat in mm/h
        initmoist1 = lg.thetaiName+"{0}.map".format(xs)  # inital moisture (cm3/cm3)
        psi1 = lg.psiName+"{0}.map".format(xs)  		    # suction with init moisture in cm, used in LISEM
        DF1 = "densfact{0}.map".format(xs)
        
        BDdf = "bddf1_{0}.map".format(xs) 

        print(">>> Creating infiltration parameters for layer "+xs, flush=True)

        lun = readmap(lg.landuseName)
        OMaddition = scalar(0.0)*mask
        if lg.useLUdensity == 1 and x == 1:
            OMaddition =  lookupscalar(lg.LULCtable, 8, nominal(lun)) * mask
        
        CorrectionOM = 0.0
        if lg.useCorrOM == 1 and x == 1:
            CorrectionOM = lg.CorrOM_            
        
        S = S1 
        C = C1 
        Si = Si1 
        OC = OC1*100  # conversion OC from fraction to percentage
        OM = min(OC*1.73,5) +  OMaddition + CorrectionOM  #conversion org carbon to org matter factor 2
        
        report(OM, om1)

        Gravel = 0 #fGrv
        if lg.useNoGravel == 1 :
            Gravel *= 0.2

        #------ this part does not consider density factor
        # wilting point stuff
        M1500 =-0.024*S+0.487*C+0.006*OM+0.005*S*OM-0.013*C*OM+0.068*S*C+0.031  #W18)
        # =-0.024*F18+0.487*G18+0.006*H18+0.005*F18*H18-0.013*G18*H18+0.068*F18*G18+0.031
        M1500adj =M1500+0.14*M1500-0.02  #X18) =W18+0.14*W18-0.02
        # field capacity stuff
        M33  =-0.251*S+0.195*C+0.011*OM+0.006*S*OM-0.027*C*OM+0.452*S*C+0.299  #Y18)
        #=-0.251*F18+0.195*G18+0.011*H18+0.006*F18*H18-0.027*G18*H18+0.452*F18*G18+0.299
        M33adj = M33+(1.283*M33*M33-0.374*M33-0.015)  #Z18) =Y18+(1.283*Y18*Y18-0.374*Y18-0.015)
        # porosity - FC
        PM33    = 0.278*S+0.034*C+0.022*OM-0.018*S*OM-0.027*C*OM-0.584*S*C+0.078  #AA18)
        #=0.278*F18+0.034*G18+0.022*H18-0.018*F18*H18-0.027*G18*H18-0.584*F18*G18+0.078
        PM33adj = PM33+(0.636*PM33-0.107)  #AB18) =AA18+(0.636*AA18-0.107)
        # porosity
        SatPM33 = M33adj + PM33adj  #AC18) =AB18+Z18
        SatSadj = -0.097*S+0.043  #AD18) =-0.097*F18+0.043
        SadjSat = SatPM33  + SatSadj  #AE18) =AC18+AD18
        Dens_om = (1-SadjSat)*2.65  #AF18) =(1-AE18)*2.65
        poredf1 = (1-Dens_om/2.65)  # pore with dens factor 1.0        
      #  bddf = 1000*(1-poredf1)*2.65  # bulk derived from pore with df 1 so standard
        
        #------ this part does not consider density factor        
        Densityfactor = scalar(1.0)*mask
        Densityfactor2 = scalar(1.0)*mask
                              
        if lg.useLUdensity == 1 and x == 1:
            Densityfactor2 =  lookupscalar(lg.LULCtable, 5, nominal(lg.lun)) * mask

            # Densityfactor = (2*Densityfactor2+Densityfactor)/3.0
            # minv = mapminimum(Densityfactor)
            # maxv = mapmaximum(Densityfactor)
            # Densityfactor = minv + (maxv-minv)*(Densityfactor-0.9)/(1.1-0.9)
        #Densityfactor = min(Densityfactor,Densityfactor2)*standardBD/bddf*mask  
        Densityfactor = min(Densityfactor,Densityfactor2)*standardBD/bdod*mask
        Densityfactor = max(0.9,min(1.2,Densityfactor))            
        # limit between 0.9 and 1.2 else can generate missing values         
        report(Densityfactor,DF1)
        
        Dens_comp = Dens_om * Densityfactor  #AG18) =AF18*(I18)
        PORE_comp =(1-Dens_om/2.65)-(1-Dens_comp/2.65)  #AI18) =(1-AG18/2.65)-(1-AF18/2.65)
        M33comp = M33adj + 0.2*PORE_comp  #AJ18)  =Z18+0.2*AI18
      #  report(Dens_comp,BDdf)
        #output maps
        POROSITY = (1-Dens_comp/2.65)*mask  #AH18)               
        
        PoreMcomp = POROSITY-M33comp  #AK18)
        LAMBDA = (ln(M33comp)-ln(M1500adj))/(ln(1500)-ln(33))  #AL18)
        GravelRedKsat =(1-Gravel)/(1-Gravel*(1-1.5*(Dens_comp/2.65)))  #AM18)
        # NOTE: soilgrids gravel is a volume fraction while the PTF need a weight fraction
        # if gravel = 0 then gravelreduction = 1
        report(GravelRedKsat,'gravred.map')       
        #report(LAMBDA,'lambda.map')
        
        Ksat = mask*max(0.0, 1930*(PoreMcomp)**(3-LAMBDA)*GravelRedKsat)  #AN18)
        BD = Gravel*2.65+(1-Gravel)*Dens_comp* mask     #U18
        WP = M1500adj*mask
        FC = M33adj* mask
        PAW = (M33adj - M1500adj)*(1-Gravel)* mask

        # POROSITY = ifthenelse(unitmap == unitBuild_, Poreurban_, POROSITY)
        # Ksat = ifthenelse(unitmap == unitBuild_, Ksaturban_, Ksat)
        # POROSITY = ifthenelse(unitmap == unitWater_, 0, POROSITY)
        # Ksat = ifthenelse(unitmap == unitWater_, 0, Ksat)

        if (fractionmoisture >= 0) :
            initmoist = fractionmoisture*POROSITY+ (1-fractionmoisture)*FC
        else :
            initmoist = -fractionmoisture*WP + (1+fractionmoisture)*FC
        BD1000 = BD*1000  #kg/m3
        report(POROSITY,Pore1)
        report(Ksat,Ksat1)
        report(BD1000,BD1)
        report(WP,WP1)
        report(FC,FC1)
        report(PAW,PAW1)
        report(initmoist,initmoist1)
        #report(bddf, BDdf1)
        
        report(Gravel*mask,lg.stoneName)

        # A = exp[ln(33) + B ln(T33)]
        # B = [ln(1500) - ln(33)] / [ln(T33) - ln(T1500)]
        #bB = (ln(1500)-ln(33))/(ln(FC)-ln(WP))
        #aA = exp(ln(33)+bB*ln(FC))
        #Psi1= aA * initmoist**-bB *100/9.8
        SS = S**2
        CC = C**2
        PP = POROSITY**2
        Psi1 =10*exp(6.53-7.326*POROSITY+15.8*CC+3.809*PP+3.44*S*C-4.989*S*POROSITY+16*SS*PP+16*CC*PP-13.6*SS*C-34.8*CC*POROSITY-7.99*SS*POROSITY)
        Psi1 = Psi1 * max(0.1,1-fractionmoisture)
        # correct psi slightly for initmoisture, where psi1 is assumed to corrspond to FC
        report(Psi1,psi1)
        report(initmoist/POROSITY,"se1.map")
        
        
        #SOILDEPTH
       # distsea = spread(nominal(1-cover(mask,0)),0,1)*mask
       # +0.5*(distsea/mapmaximum(distsea))**0.1
        rivfact = mask*0
        chanm = mask*0;
        if  lg.doProcessesChannels == 1:
            chanm = cover(lg.rivers_, 0)*mask       
        else:
            chanm = readmap(lg.chanmaskName) 
        
            
        distriv = spread(cover(nominal(chanm > 0),0),0,1)*mask
        rivfact = -0.5*distriv/mapmaximum(distriv)
            # perpendicular distance to river, closer gives deeper soils          
       
        if x == 1 :
            soildepth1 = lg.soildepth1depth*mask
            report(soildepth1,lg.soildep1Name)
        if x == 2 :
            # steeper slopes giver undeep soils
            soild = mask*cover((1-min(1,slope(DEM)))+rivfact,0)
            #soild = mask*cover((1-min(1,slope(DEM)))+rivfact+100*profcurv(DEM),0) #
            soildb = min(lg.soildepth2depth,lg.soildepth2depth*(soild)**1.5)
            # m to mm for lisem, higher power emphasizes depth
            soildb = windowaverage(soildb,3*celllength())
            # smooth because soil depth does not follow dem exactly        
            soildepth1 = lg.soildepth1depth*mask
            mapavg = areaaverage(soildb,nominal(mask))
            soildepth2 = mask*cover(soildepth1+soildb,mapavg)     
            report(soildepth2,lg.soildep2Name)
        
