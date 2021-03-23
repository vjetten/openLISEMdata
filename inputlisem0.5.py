# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 14:07:11 2021
openlisem input script
@author: v jetten, ITC
"""

# pcraster stuff
from pcraster import *
from pcraster.framework import *

# gdal stuff
from osgeo import gdal, gdalconst, osr
from owslib.wcs import WebCoverageService

# operation system stuff
import subprocess  # call exe from wihin script
import os          # change dir and so on
#import sys
#import numpy as np

# linear regression for D50 and D90
from scipy import stats


setglobaloption("lddin")
setglobaloption("lddfill")
setglobaloption("matrixtable")

import channelMaps

### ------ ALL STABDARD OPENLISEM MAPNAMES ------ ###

### input maps ###
DEMinName = 'dembasin.map'              # digital elevation model, area must be <= mask
buffersinName = 'zero.map'              # in m, positive valuesName = dike, negative values is basin, added to the DEM
maskinName = 'maskbasin.map'            # mask to the catchment , 1 and MV

LULCinName = 'LULC_2005.tif'            # land use types
lutblName = 'ludata.tbl'                # land use surface properties
                                        # col 1=Micro roughness; 2 = manning's; 3 = plant height; 4 = cover, 5 is bulkdensity factor
lulcDIR = 'C:/\data/India/Decadal_LULC_India_1336/data/'
                                        # folder name of India LU map

riversinName = 'rivermask.map'          # river mask
mainoutinName = 'mainout.map'           # forced outlet rivers to the sea, because of imperfect dem
outpointuserinName = 'mainout.map'      # points for user output hydrographs

housecoverinName = 'zero.map'           # housing density fraction (0-1)
hardsurfinName = 'zero.map'             # hard surfaces (0-1) such as airport, parking lots etc
roadinName = 'zero.map'                 # tarmac roads mask or type numbers
NDVIinName = 'zero.map'                 # NDVI for cover and LAI

### output maps ###

# basic topography related maps
DEMName = 'dem.map'             # adjusted dem
IDName = 'id.map'               # raingauge zones, def set to 1
buffersName = 'buffer.map'      # changes in m to the dem (+ or -)
LddName = 'ldd.map'             # Local Drain Direction for surface runoff
gradName = 'grad.map'           # slope, sine! (0-1)
idName = 'id.map'               # pluviograph influence zones
outletName = 'outlet.map'       # location outlets and checkpoints
landuseName = 'landuse.map'    # landuse/landcover for RR and manning
outpointName = 'outpoint.map'   # user defined output locations
upsName = 'ups.map'             # cumulative flow network, not used in lisem
wsName = 'ws.map'               # watershed boundary map, not used in lisem
shadeName = 'shade.map'         # shaded relief map, not use din lisem

# infrastructure
roadwidthName = 'roadwidt.map'   # road width (m)
hardsurfName = 'hardsurf.map'    # impermeable surfaces (0 or 1)
housecovName = 'housecover.map'  # house cover fraction
roofstoreName = 'roofstore.map'  # roof interception (mm) \
raindrumsizeName = 'raindrum.map'# raindrum size (m3)
drumstoreName = 'drumstore.map'  # locations of rainwater harvesting in drums (0/1)

# vegetation maps
coverName = 'per.map'           # cover fraction (-)
laiName = 'lai.map'             # leaf area index (m2/m2) for interception storage
smaxName = 'smax.map'           # user defined canopy storage
cropheightName = 'ch.map'       # plant height in m, for erosion, not used
grasswidName = 'grasswid.map'   # width of grass strips for infiltration
LitterName = 'litter.map'       # fraction of litter under tree vegetation.

# Green and Ampt infiltration maps
ksatName = 'ksat'                # sat hydraulic conductivity (mm/h)
poreName = 'thetas'              # porosity (-)
thetaiName = 'thetai'            # initial moisture content (-)
psiName = 'psi'                 # suction unsat zone (cm)
soildep1Name = 'soildep1.map'    # soil depth (mm), assumed constant
soildep2Name = 'soildep2.map'    # soil depth (mm), assumed constant

cohName = 'coh'
cohaddName = 'cohadd.map'
asName = 'aggrstab.map'
d50Name = 'd50.map'
d90Name = 'd90.map'

compactName = 'compfrc.map'      # fraction of compacted siurface (0-1)
crustName = 'crustfrc.map'       # fraction of crusted siurface (0-1)
ksatcompName = 'ksatcomp.map'    # ksat of compacted areas (mm/h)
ksatcrustName = 'ksatcrust.map'  # ksat of crusted areas (mm/h)
porecompName = 'porecomp.map'    # Porosity of compacted areas (-)
porecrustName = 'porecomp.map'   # Porosity of crusted areas (-)

# surface maps
rrName = 'rr.map'                # surface roughness (cm)
mannName = 'n.map'               # mannings n ()
stoneName = 'stonefrc.map'       # stone fraction on surface (-)
crustName = 'crustfrc.map'       # crusted soil (-), not present
compName = 'compfrc.map'         # compacted soil (-), murrum roads

# erosion maps , not used
cohsoilName = 'coh.map'          # cohesion (kPa)
cohplantName = 'cohadd.map'      # added root cohesion (kPa)
D50Name = 'd50.map'              # median of texture for suspended (mu)
D90Name = 'd90.map'			     # 90 quantile of texture for bedload (mu)
aggrstabName = 'aggrstab.map'    # aggregate stability number (-)

# channel maps
lddchanName = 'lddchan.map'      # channel 1D network
chanwidthName = 'chanwidt.map'   # channel width (m)
changradName = 'changrad.map'    # channel gradient, sine
chanmanName = 'chanman.map'      # channel manning (-)
chansideName = 'chanside.map'    # angle channel side walls, 0Name = 'rectangular
chanmaskName = 'chanmask.map'   # copy of channel mask
chancohName = 'chancoh.map'      # channel cohesion (kPa)
chandepthName = 'chandepth.map'  # channel depth (m)
chanmaxqName = 'chanmaxq.map'    # maximum discharge (m3/s) in culvert locations in channel
chanleveesName = 'chanlevee.map' # main levees along channels
chanksatName = 'chanksat.map'    # ksat in case channel infiltrates, for dry channels
baseflowName = 'baseflow.map'    # stationary baseflow at end piints of river


### ---------- class GetSoilGridsLayer ---------- ###

class GetSoilGridsLayer:
    "downbloading a SOILGRIDS layer from WCS service"
    def __init__(self, mask, ESPG="",s="", i=1, j = 1):
        self.mask = mask
        self.varname = s
        self.layer = i
        self.outlayer = j
        self.debug = Debug_
        self.ESPG = ESPG

        if self.layer == 1: ID='_0-5cm_mean'
        if self.layer == 2: ID='_5-15cm_mean'
        if self.layer == 3: ID='_15-30cm_mean'
        if self.layer == 4: ID='_30-60cm_mean'
        if self.layer == 5: ID='_60-100cm_mean'
        if self.layer == 6: ID='_100-200cm_mean'

        #if self.debug == 1:
        print("Processing layer "+str(self.outlayer)+": "+self.varname+ID)

       # raster=gdal.Open(self.mask)
        ESPG = 'urn:ogc:def:crs:EPSG::{0}'.format(self.ESPG)

        if self.debug == 1:
            print("Mask ESPG and bounding box:"+ESPG,llx,lly,urx,ury,dx,dy)

        if self.debug == 1:
            print("Open SOILGRIDS WCS")

        url = "http://maps.isric.org/mapserv?map=/map/{}.map".format(self.varname)
        wcs = WebCoverageService(url, version='1.0.0')
        # show some info:
        # cov_list = list(wcs.contents)
        # mean_covs = [k for k in wcs.contents.keys() if k.find("mean") != -1]
        # print(mean_covs)

        variable = self.varname+ID
        varout = self.varname+str(self.outlayer)
        outputnametif = "{0}.tif".format(varout)
        outputnamemap = "{0}.map".format(varout)
        #outputnametmp = '_temp_.tif'

        if self.debug == 1:
            print("Downloading "+variable)

        # get data as temp geotif and save to disk
        response = wcs.getCoverage(identifier=variable,crs=ESPG,bbox=maskbox,
            resx=dx,resy=dx,format='GEOTIFF_INT16')
        with open(outputnametif, 'wb') as file:
             file.write(response.read())

        # warp to some interpolation
        src = gdal.Open(outputnametif, gdalconst.GA_ReadOnly)
        src_proj = src.GetProjection()
        src_geotrans = src.GetGeoTransform()
        dst = gdal.GetDriverByName('PCRaster').Create(outputnamemap, nrCols, nrRows, 1,
                                   gdalconst.GDT_Float32,["PCRASTER_VALUESCALE=VS_SCALAR"])
        dst.SetGeoTransform( src_geotrans )
        dst.SetProjection( src_proj )
        gdal.ReprojectImage(src, dst, src_proj, src_proj, gdalconst.GRA_Bilinear)
        #gdalconst.GRA_Cubic)

        # brute force convert tif to map by calling pcrcalc !!!!
        # CMD = "pcrcalc.exe"
        # arg = outputnamemap+"="+outputnametif
        # arg = '{0}{1}.map={0}{1}.tif'.format(self.varname,str(self.outlayer))
        # subprocess.run([CMD,arg])

        dst = None
        src = None


### ---------- class PedoTranfer() ---------- ###

class PedoTransfer(StaticModel):
    # creates infiltration input vars: Ksat 1,2; Thetas1,2; Thetai1,2; Psi1,2
    # from SOILGRID.ORG GTiff maps for texture, org matter, gravel and bulkdensity
    # Using Saxton And Rawls 2006 pedotransferfunctions
    # https://hrsl.ba.ars.usda.gov/SPAW/Index.htm
    def __init__(self,mask=0,layer=1,moisture=0.7,sBD=1350.0):
        StaticModel.__init__(self)
    def initial(self):
        standardBD = scalar(standardbulkdensity_)  # standard bulk dens assumed by saxton and rawls. High! 1350 would be better
        fractionmoisture = scalar(initmoisture_)   #inital moisture as fraction between porosity and field capacity
        x = layer_
        mask = mask_

        S1 = readmap("{0}{1}.map".format(SG_names_[0],str(x)))  # sand g/kg
        Si1 = readmap("{0}{1}.map".format(SG_names_[1],str(x))) # silt g/kg
        C1 = readmap("{0}{1}.map".format(SG_names_[2],str(x)))  # clay g/kg
        OC1 = readmap("{0}{1}.map".format(SG_names_[3],str(x)))  # organic carbon in dg/kg
        Grv = readmap("{0}{1}.map".format(SG_names_[4],str(x))) # coarse fragments cm3/dm3,
        bd1 = readmap("{0}{1}.map".format(SG_names_[5],str(x)))   # bulk density in cg/m3

        #output map name strings
        om1 = "om{0}.map".format(str(x))             # organic matter in %
        WP1 = "wilting{0}.map".format(str(x))      	# wilting point moisture content
        FC1 = "fieldcap{0}.map".format(str(x))     	# field capacity moisture content
        PAW1 = "plantAVW{0}.map".format(str(x))    	# plant available water content
        Coh1 = cohName+"{0}.map".format(str(x))           # soil cohesion (kPa)
        #K1 = "k{0}.map".format(str(x))  		        #USLE erodibility
        BD1 = "bulkdens{0}.map".format(str(x))       # bulk density in kg/m3
        Pore1 = poreName+"{0}.map".format(str(x))   	#porosity (cm3/cm3)
        Ksat1 = ksatName+"{0}.map".format(str(x))      	#ksat in mm/h
        initmoist1 = thetaiName+"{0}.map".format(str(x))  # inital moisture (cm3/cm3)
        psi1 = psiName+"{0}.map".format(str(x))  		    # suction with init moisture in cm, used in LISEM
        Densityfactor1 = "densfact{0}.map".format(str(x))

        print("Creating infil params layer "+str(x))

        S = S1/1000  # from g/kg to fraction
        C = C1/1000
        Si = Si1/1000
        OC = (OC1/10000)*100  # conversion OC from dg/kg to percentage
        OM = OC*1.73  #/2.0   #conversion org carbon to org matter factor 2

        unitmap = readmap(landuseName)

        # quick and dirty filling up from the sides
        S = scalar(spreadzone(nominal(S),0,1))
        Si = scalar(spreadzone(nominal(Si),0,1))
        C = scalar(spreadzone(nominal(C),0,1))
        OM = scalar(spreadzone(nominal(OM),0,1))
        bd1 = scalar(spreadzone(nominal(bd1),0,1))
        Grv = scalar(spreadzone(nominal(Grv),0,1))

        report(OM, om1)

        densityveg = lookupscalar(lulcTable, 5, lun)

        bdsg = bd1*10            #bulkdensity cg/m3 to kg/m3
        bdsg = ifthenelse(bd1 < 1,standardBD,bdsg) # replace areas with MV bdsg to standard BD
        Gravel = Grv/1000  # from cm3/dm3 (1000 cc in a liter)
        Densityfactor = densityveg * scalar(0.95) #bdsg/standardBD*Dens #(1-0.1*cover)
        # density factor is 1.0, but could be made lower for organic soils and higher for compacted urban areas.
        report(Densityfactor,Densityfactor1)

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
        Dens_comp = Dens_om * Densityfactor  #AG18) =AF18*(I18)
        PORE_comp =(1-Dens_om/2.65)-(1-Dens_comp/2.65)  #AI18) =(1-AG18/2.65)-(1-AF18/2.65)
        M33comp = M33adj + 0.2*PORE_comp  #AJ18)  =Z18+0.2*AI18

        #output maps
        POROSITY = (1-Dens_comp/2.65)*mask  #AH18)
        PoreMcomp = POROSITY-M33comp  #AK18)
        LAMBDA = (ln(M33comp)-ln(M1500adj))/(ln(1500)-ln(33))  #AL18)
        GravelRedKsat =(1-Gravel)/(1-Gravel*(1-1.5*(Dens_comp/2.65)))  #AM18)
        report(LAMBDA,'lambda.map')
        report(PoreMcomp,'PoreMcomp.map')
        report(M33comp,'M33comp.map')
        Ksat = mask*max(0.0, 1930*(PoreMcomp)**(3-LAMBDA)*GravelRedKsat)  #AN18)
        BD = Gravel*2.65+(1-Gravel)*Dens_comp* mask     #U18
        WP = M1500adj*mask
        FC = M33adj* mask
        PAW = (M33adj - M1500adj)*(1-Gravel)* mask

        # POROSITY = ifthenelse(unitmap == unitBuild_, Poreurban_, POROSITY)
        # Ksat = ifthenelse(unitmap == unitBuild_, Ksaturban_, Ksat)
        # POROSITY = ifthenelse(unitmap == unitWater_, 0, POROSITY)
        # Ksat = ifthenelse(unitmap == unitWater_, 0, Ksat)

        initmoist = fractionmoisture*POROSITY+ (1-fractionmoisture)*FC

        report(POROSITY,Pore1)
        report(Ksat,Ksat1)
        report(BD,BD1)
        report(WP,WP1)
        report(FC,FC1)
        report(PAW,PAW1)
        report(initmoist,initmoist1)

        # A = exp[ln(33) + B ln(T33)]
        # B = [ln(1500) - ln(33)] / [ln(T33) - ln(T1500)]
        bB = (ln(1500)-ln(33))/(ln(FC)-ln(WP))
        aA = exp(ln(33)+bB*ln(FC))
        Psi1= aA * initmoist**-bB *100/9.8
        report(Psi1,psi1)
        report(initmoist/POROSITY,"se1.map")

        ############################################
        ## Generation of soil cohesion map        ##
        ## estimation based on clay content       ##
        ## adapted from Morgan, 2001              ##
        ############################################
        if optionErosionMaps and x == 1:
            Coh = max(1.0, 4.316*ln(C+1.0) - 6.955)
            # log fit using values below
            Coh = ifthenelse((unitmap == unitBuild_) | (unitmap == unitWater_) , -1, Coh)
            #Coh = lookupscalar("claycoh.tbl",C)*mask
            # content of claycoh.tbl
            # [,20>   2
            # [20,35> 3
            # [35,40> 9
            # [40,55> 10
            # [55,60> 11
            # [60,100> 12

            report(Coh, Coh1)
            report(Coh,aggrstabName)
            D50 = scalar(0)
            D90 = scalar(0)

            if optionD50 == 1 :
                print('estimating d50 and d90 from texture, may take some time')
                cp = pcr2numpy(C, -9999)
                sip = pcr2numpy(Si, -9999)
                sp = pcr2numpy(S, -9999)
                d50p = pcr2numpy(D50, -9999)
                d90p = pcr2numpy(D90, -9999)

                step = 1
                star = ["|","/","-","\\"]
                sr = 0
                for row in range(1,nrRows) :
                    sss = "["+"#"*step+star[sr]+"."*(100-step-1)+"]"
                    sr+= 1
                    if sr == 4: sr = 0
                    if row % int(nrRows/100) == 0 :
                        step += 1

                    #print("\r" + str("{:.0%}".format(row/nrRows)), end="")
                    print("\r" + sss, end="")
                    for col in range(1,nrCols) :
                        c = cp[row][col]#cellvalue(C, row, col)
                        si = sip[row][col]#cellvalue(Si, row, col)
                        s = sp[row][col]#cellvalue(S, row, col)
                        y = [c,c+si,1.0]
                        x = [0.693147181,3.912023005,6.214608098]
                        res = stats.linregress(x, y)
                        # print("a",res.intercept)
                        # print("a",res.slope)
                        # # linear regression between cumulative texture fraction and ln(grainsize)
                        if res.slope > 1e-3 :
                            d50p[row][col] = exp((0.5-res.intercept)/res.slope)
                            d90p[row][col] = exp((0.9-res.intercept)/res.slope)
                        else :
                            d50p[row][col] = 0
                            d90p[row][col] = 0
                            #print(row,col,d50p[row][col])

                # print(d50p[100][100])
                D50 = numpy2pcr(Scalar,d50p,-9999)
                report(D50*mask,d50Name)
                D90 = numpy2pcr(Scalar,d90p,-9999)
                report(D90*mask,d90Name)
                print("\n")


### ---------- class DEMderivatives() ---------- ###

class DEMderivatives(StaticModel):
    def __init__(self):
        StaticModel.__init__(self)
    def initial(self):
        mask = mask_
        size = catchmentsize_
        global mainout_
        mainout = mainout_

        ID = mask
        report(ID,IDName)

        barriers = scalar(0) #readmap(buffersinName)*mask
        report(barriers,buffersName);

        DEM = readmap(DEMinName)*mask
        if fillDEM > 0 :
            DEMc = lddcreatedem(DEM, fillDEM,fillDEM,fillDEM,fillDEM)
        DEMm = DEM + barriers;
        report(DEMm, DEMName)
        DEM_ =- DEMm

        chanm = scalar(0)
        if optionChannelMaps :
            chanm = readmap(riversinName)*mask
            chanm = cover(ifthen(chanm > 1, scalar(1)),0)*mask

        Ldd = lddcreate (DEMm-chanm*10-mainout*10, size, size, size, size)
        report(Ldd, LddName)
        Ldd_ = Ldd
        mainout_ = cover(scalar(pit(Ldd)),0)*mask


        # runoff flow network based on dem, main outlet, channels and barriers
        #report outlet = mainout; #pit(Ldd);
        grad = sin(atan(slope(DEMm)))
        report(grad, gradName)

        #### not used in lisem, auxilary maps

        ups=accuflux(Ldd,1)
        report(ups,upsName)  # not used
        ws=catchment(Ldd, pit(Ldd));
        report(ws,wsName)

        asp = scalar( aspect(DEMm));
        shade = cos(15)*sin(grad)*cos(asp+45) + sin(15)*cos(grad);
        shade = 0.7*(shade-mapminimum(shade))/(mapmaximum(shade)-mapminimum(shade))
        + 0.3*(DEM-mapminimum(DEM))/(mapmaximum(DEM)-mapminimum(DEM))

        report(shade,shadeName)  # not used in lisem


        distriv = spread(nominal(chanm > 0),0,1)*mask
        distsea = spread(nominal(1-cover(mask,0)),0,1)*mask
        soild = mask*cover((1-min(1,grad))       # steeper slopes giver undeep soils
               -0.5*distriv/mapmaximum(distriv)  # perpendicular distance to river, closer gives deeper soils
               +0.5*(distsea/mapmaximum(distsea))**0.1
               ,0)
        soildb = 1500*(soild)**1.5
        # m to mm for lisem, higher power emphasizes deep, updeep
        soildepth1 = soildepth1depth
        soildepth2 = mask*(soildepth1+cover(windowaverage(soildb,3*celllength()),mask))

        report(soildepth1,soildep1Name)
        report(soildepth2,soildep2Name)



### ---------- class SurfaceMaps() ---------- ###

class SurfaceMaps(StaticModel):
    def __init__(self):
        StaticModel.__init__(self)
    def initial(self):
        mask = mask_
        unitmap = lun #readmap(landuseName)

        if Debug_ :
            print('create RR, n etc')


        rr = cover(max(lookupscalar(lulcTable, 1, unitmap), 0.5),1.0) * mask
        report(rr,rrName)
         # micro relief, random roughness (=std dev in cm)

        mann = lookupscalar(lulcTable, 2, unitmap) * mask
        mann = cover(mann,0.05)*mask
        # mann = 0.01*rr + 0.1*Cover
        report(mann,mannName)
         # in the lisem code Manning's n is increased with house effect

        Cover = lookupscalar(lulcTable, 4, unitmap) * mask
        Cover = min(0.95,Cover)
        report(Cover,coverName)

        # cover = exp(-0.4*LAI)
        LAI = ifthenelse(Cover > 0,ln(Cover)/-0.4,0)
        LAI = max(min(6.5, LAI), 0.0)*mask
        report(LAI, laiName)


        smaxnr = lookupscalar(lulcTable, 6, unitmap)
        #report(smaxnr,'smaxnr.map')

        a = [0, 1.412, 0.2331, 0.3165, 1.46, 0.0918, 0.2856, 0.1713,0.59]
        b = [0, 0.531, 0     , 0     , 0.56, 1.04  , 0     , 0     ,0.88]

        smax1 = ifthenelse(smaxnr == 1, a[1]*LAI**b[1],0)*mask
        smax2 = ifthenelse(smaxnr == 2, a[2]*LAI,0)*mask
        smax3 = ifthenelse(smaxnr == 2, a[3]*LAI,0)*mask
        smax4 = ifthenelse(smaxnr == 3, a[4]*LAI**b[4],0)*mask
        smax5 = ifthenelse(smaxnr == 4, a[5]*LAI**b[5],0)*mask
        smax6 = ifthenelse(smaxnr == 5, a[6]*LAI,0)*mask
        smax7 = ifthenelse(smaxnr == 6, a[7]*LAI,0)*mask
        smax8 = ifthenelse(smaxnr == 7, a[8]*LAI**b[8],0)*mask

        Smax = smax1+smax2+smax3+smax4+smax5+smax6+smax7
        report(Smax, smaxName)

        crust = mask*0
        report(crust,crustName)
        # crust fraction assumed zero
        compact = mask*0
        report(compact,compactName)
        # compact fraction assumed zero

        hardsurf = readmap(hardsurfinName)*mask
        report(hardsurf ,hardsurfName)
         #hard surface, here airports and large impenetrable areas

        roadwidth = readmap(roadinName)*mask
        report(roadwidth,roadwidthName)

        building = readmap(housecoverinName)*mask
        report(building,housecovName)


        if optionErosionMaps :
            cropheight = lookupscalar(lulcTable, 3, unitmap) * mask #plant height in m
            report(cropheight,cropheightName)

            aggrstab = 6 * mask;  # aggregate stability
            report(aggrstab,asName)

            cohplant = Cover * 5.0 * mask  # additional plant root strength
            report(cohplant,cohaddName)

### ---------- class ChannelMaps() ---------- ###
class ChannelMaps(StaticModel):
    #! --lddout
    def __init__(self):
        StaticModel.__init__(self)
    def initial(self):
        mask = mask_
        global mainout_
        mainout = mainout_
        DEM = DEM_

        rivers=readmap(riversinName)
        chanmask = ifthen(rivers > 0, scalar(1))*mask
        # create missing value outside channel

        lddchan = lddcreate((DEM-mainout*10)*chanmask,1e20,1e20,1e20,1e20)
        cm=ifthen(accuflux(lddchan,1) > 1,chanmask)*mask
        lddchan = lddcreate((DEM-mainout*10)*cm,1e20,1e20,1e20,1e20)
        report(lddchan,lddchanName)
        report(cm, chanmaskName)

        outpoint = cover(scalar(pit(lddchan)),0)*mask
        outlet = cover(scalar(pit(lddchan)),0)*mask
        mainout_ = outlet
        report(outlet,outletName)
        report(outpoint,outpointName)

        changrad = min(0.5,max(0.01,sin(atan(slope(chanmask*DEM)))))
        changrad = windowaverage(changrad, 5*celllength())*chanmask
        report(changrad,changradName)

        chanman = chanmask*0.05
        report(chanman,chanmanName) # fairly rough and rocky channel beds
        chanside = chanmask*scalar(0)  # ALWAYS rectangular channel
        report(chanside, chansideName)

        # relation by Allen and Pavelski (2015)
        dx = celllength()
        af = accuflux(Ldd_, dx/3.22e4)
        chanwidth = min(0.95*dx, max(2.0, af**(1.18)))*chanmask
        report(chanwidth,chanwidthName)
        ##  culvert_fraction_width = 0.8;
        ##  report chanwidth = min(celllength()*0.95, if(culverts gt 0, chanwidth*culvert_fraction_width, chanwidth));
        ##  # channel width is 15m at outlet and beccoming less away form the coast to 3 m
           #-0.5 +
        chandepth = max(1.0,chanwidth**0.2)
        chandepth = min(chandepth, 1.0/(sqrt(changrad)/chanman))
        report(chandepth,chandepthName)

        chanmaxq = 0*mask#if(culverts gt 0, 2, 0)*mask;
        report(chanmaxq,chanmaxqName)
        chanksat = 0*mask
        report(chanksat,chanksatName)

        #bridges=clump(nominal(cover(if(chanwidth gt 9 and roadwidth gt 0 , 1, 0),0)*mask)); #and so ge 4
        ws=catchment(Ldd_, pit(lddchan));
        report(ws,wsName)

        baseflow=cover(scalar(pit(lddchan) != 0)*chanwidth*chandepth*0.5,0)*mask
        report(baseflow,baseflowName)
        # assuming 0.5 m/s baseflow


### ---------- START ---------- ###

# NIOTE: preperatory actions
# 1. QGIS: download SRTM
# 2. PCRaster create an ldd using 1e8 as weight and --lddin
# 3. create watersheds: pcrcalc ws.map=catchment()ldd.map, pit(ldd.map))
# 4. select appropriate water (cauvery has nr 78)
# craete a mask from this watershed abnd use resample to eliminate ros and cols with missing cvalue



workingDir = 'C:/data/India/narmada/maps'
os.chdir(workingDir)

print('read base maps')

masknamemap_ = maskinName  # pcraster file for exact basin mask

# set the overall mask
setclone(masknamemap_)
mask_ = readmap(masknamemap_)

# set the gdal details of the mask, bounding box, rows and cols
maskgdal=gdal.Open(masknamemap_) # get mask details
maskproj = maskgdal.GetProjection()
nrRows = maskgdal.RasterYSize
nrCols = maskgdal.RasterXSize
dx = maskgdal.GetGeoTransform()[1]
dy = maskgdal.GetGeoTransform()[5]
llx = maskgdal.GetGeoTransform()[0]
ury = maskgdal.GetGeoTransform()[3]
urx = llx + nrCols*dx
lly = ury + dy*nrRows
maskbox = [llx,lly,urx,ury]

# soilgrid layer rootnames
SG_names_ = ['sand','silt','clay','soc','cfvo','bdod']

#maps that are needed in multiple classes
soildepth1depth = scalar(300)           # mm of first layer and minimal soildepth
mainout_ = readmap(mainoutinName)       # can be zero
Ldd_ = ldd(0*mask_)
DEM_ = scalar(0)
Ksaturban_ = scalar(5)
Poreurban_ = scalar(0.45)
unitBuild_ = nominal(3)  # to adapt ksat pore urban areas
unitWater_ = nominal(9)  # to adapt ksat pore water
report(DEM_,'zero.map')
initmoisture_ = 0.7
standardbulkdensity_ = scalar(1450.0)
fillDEM = 1e4  # use fill dem with lddcreatedem, if this value = 0 then this is not used
catchmentsize_ = 1e9

optionErosionMaps = True
optionD50 = False
useBulkdensity = False

Debug_ = False
doProcesses = [0,0,1,0,0]
#dem, channel, lulc, soilgrids, infil



print('Get land use map for the area')
lulcTable = lulcDIR+lutblName
lulcTIF = lulcDIR+LULCinName
src = gdal.Open(lulcTIF)
# get ESPG number
ESPG = osr.SpatialReference(wkt=src.GetProjection()).GetAttrValue('AUTHORITY',1)
print('ESPG:'+ESPG)
#cutout and convert
dst = gdal.GetDriverByName('PCRaster').Create(landuseName, nrCols, nrRows, 1,
                            gdalconst.GDT_Int32,["PCRASTER_VALUESCALE=VS_NOMINAL"])
dst.SetGeoTransform( maskgdal.GetGeoTransform() )
dst.SetProjection( maskproj )
gdal.ReprojectImage(src, dst, maskproj, maskproj, gdalconst.GRA_NearestNeighbour)
dst = None
src = None

lun = readmap(landuseName)
# lun = nominal(lu)
lun = spreadzone(lun,0,1)
#report(lun,landuseName)

mask_ = ifthen( boolean(mask_ == 1) & boolean(lun != 0),scalar(1))
report(ifthen(mask_ == 1, lun),landuseName)


if doProcesses[0] == 1 :
    print('dem derivatives, slope, LDD etc')
    staticModelDEM = StaticFramework(DEMderivatives())
    staticModelDEM.run()

if doProcesses[1] == 1:
    print('channel maps')
    staticModelCH = StaticFramework(ChannelMaps())
    staticModelCH.run()

if doProcesses[2] == 1:
    print('surface and land use related maps')
    staticModelSURF = StaticFramework(SurfaceMaps())
    staticModelSURF.run()


# soil and infiltration maps
if doProcesses[3] == 1:
    print("downloading SOILGRIDS layers...")
    #soigrid map names for texture, doil organic carbon, course fragments, bulk dens
    for x in range(0,6):
        GetSoilGridsLayer(masknamemap_,ESPG,SG_names_[x],2,1)
    for x in range(0,6):
        GetSoilGridsLayer(masknamemap_,ESPG,SG_names_[x],4,2)


if doProcesses[4] == 1:
    staticModel = StaticFramework(PedoTransfer())
    layer_ = 1
    staticModel.run()
    layer_ = 2
    staticModel.run()

print("Done")

# 		rr	n	height
# 	0	1	2	3
# 1- Deciduous Broadleaf Forest	1	2	0.05	10
# 2- Cropland	2	1	0.04	1.5
# 3- Built-up Land	3	0.5	0.1	8
# 4- Mixed Forest	4	2	0.1	10
# 5- Shrubland	5	2	0.08	5
# 6- Barren Land	6	1	0.035	0.2
# 7- Fallow Land	7	1	0.05	0.1
# 8- Wasteland	8	1	0.05	0.1
# 9- Water Bodies	9	0.5	0.01	0
# 10- Plantations	10	1.5	0.05	8
# 11- Aquaculture	11	1	0.06	0.5
# 12- Mangrove Forest	12	2	0.09	8
# 13- Salt Pan	13	0.5	0.03	0
# 14- Grassland	14	1	0.1	0.5
# 15- Evergreen Broadleaf Forest	15	2	0.1	12
# 16- Deciduous Needleleaf Forest	16	2	0.09	12
# 17- Permanent Wetlands	17	1	0.1	1
# 18- Snow & Ice	18	1	0.03	0
# 19- Evergreen Needleleaf Forest	19	2	0.09	10