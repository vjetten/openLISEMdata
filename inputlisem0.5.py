# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 09:50:45 2021
openlisem input script
@author: vjetten
"""

# pcraster stuff
from pcraster import *
from pcraster.framework import *

# gdal stuff
from osgeo import gdal, gdalconst, osr
from owslib.wcs import WebCoverageService

import subprocess  # call exe from wihin script
import os          # change dir and so on


workingDir = 'C:/data/India/Cauvery/Base/'
os.chdir(workingDir)


### ------ ALL STABDARD OPENLISEM MAPNAMES ------ ###

### input maps ###
catchmentsize = 1e6
soildepth1depth = scalar(300) # mm of first layer and minimal soildepth

DEMinName = 'demc.map'                  # digital elevation model, area must be <= mask
buffersinName = 'buffer.map'            # in m, positive valuesName = dike, negative values is basin, added to the DEM

unitinName = 'lu20m.map'                # land use types
lutblName = 'ludataSTL.tbl'             # land use surface properties
                                        # col 1=Micro roughness; 2 = manning's; 3 = plant height; 4 = cover
riversinName = 'chanmask.map'           # river mask
mainoutinName = 'mainout20m.map'        # forced outlet rivers to the sea, because of imperfect dem
outpointuserinName = 'mainout20m.map'   # points for user output hydrographs

housecoverinName = 'building20m.map'    # housing density fraction (0-1)
hardsurfinName = 'zero.map'             # hard surfaces (0-1) such as airport, parking lots etc
roadinName = 'roadtype20m.map'          # type 1Name = highway, 2Name = 2.5 car width is larger, 3 is 1.5 car width


### output maps ###


# basic topography related maps
DEMName = 'dem.map'             # adjusted dem
buffersName = 'buffer.map'      # changes in m to the dem (+ or -)
LddName = 'ldd.map'             # Local Drain Direction surface runoff
gradName = 'grad.map'           # slope, sine!
idName = 'id.map'               # pluviograph influence zones
outletName = 'outlet.map'       # location outlets and checkpoints
landuseName = 'landunit.map'    # land units combined soil and vegetation
outpointName = 'outpoint.map'   # points where hydrograph output is generated
upsName = 'ups.map'             # points where hydrograph output is generated
wsName = 'ws.map'               # points where hydrograph output is generated
shadeName = 'shade.map'

# impermeable roads, tarmac, concrete
roadwidthName = 'roadwidt.map'  # rad width (m)

# vegetation maps
coverName = 'per.map'           # cover fraction (-)
laiName = 'lai.map'             # leaf area index (m2/m2) for interception storage
cropheightName = 'ch.map'       # plant height in m, for erosion, not used
grasswidName = 'grasswid.map'   # width of grass strips for infiltration
LitterName = 'litter.map'       # fraction of litter under tree vegetation.

# Green and Ampt infiltration maps
ksatName = 'ksat'                # sat hydraulic conductivity (mm/h)
poreName = 'thetas'              # porosity (-)
thetaiName = 'thetai'            # initial moisture content (-)
psiName = 'psi1'                 # suction unsat zone (cm)
soildep1Name = 'soildep1.map'    # soil depth (mm), assumed constant
soildep2Name = 'soildep2.map'    # soil depth (mm), assumed constant

cohName = 'coh'
cohaddName = 'cohadd.map'
asName = 'aggrstab.map'
d50Name = 'd50.map'
d90Name = 'd90.map'

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
hardName = 'hardsurf.map'        # impermeable surfaces (0 or 1)

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
chanmasknName = 'chanmask.map'   # copy of channel mask
chancohName = 'chancoh.map'      # channel cohesion (kPa)
chandepthName = 'chandepth.map'  # channel depth (m)
chanmaxqName = 'chanmaxq.map'    # maximum discharge (m3/s) in culvert locations in channel
chanleveesName = 'chanlevee.map' # main levees along channels
chanksatName = 'chanksat.map'    # ksat in case channel infiltrates, for dry channels
baseflowName = 'baseflow.map'    # stationary baseflow at end piints of river

# houses
housecovName = 'housecover.map'  # house cover fraction
roofstoreName = 'roofstore.map'  # roof interception (mm) \
raindrumsizeName = 'raindrum.map'# raindrum size (m3)
drumstoreName = 'drumstore.map'  # locations of rainwater harvesting in drums (0/1)



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

        raster=gdal.Open(self.mask)
        ESPG = 'urn:ogc:def:crs:EPSG::{0}'.format(self.ESPG)
        wide = raster.RasterXSize
        high = raster.RasterYSize
        dx = raster.GetGeoTransform()[1]
        dy = raster.GetGeoTransform()[5]
        llx = raster.GetGeoTransform()[0]
        ury = raster.GetGeoTransform()[3]
        urx = llx+wide*dx
        lly = ury+dy*high
        bbox = [llx,lly,urx,ury]

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
        response = wcs.getCoverage(identifier=variable,crs=ESPG,bbox=bbox,
            resx=dx,resy=dx,format='GEOTIFF_INT16')
        with open(outputnametif, 'wb') as file:
             file.write(response.read())

        # warp to some interpolation
        src = gdal.Open(outputnametif, gdalconst.GA_ReadOnly)
        src_proj = src.GetProjection()
        src_geotrans = src.GetGeoTransform()
        dst = gdal.GetDriverByName('PCRaster').Create(outputnamemap, wide, high, 1,
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
        if self.debug == 1:
            print("Done.\n")


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
        mask=mask_

        S1 = readmap("{0}{1}.map".format(SG_names_[0],str(x)))  # sand g/kg
        Si1 = readmap("{0}{1}.map".format(SG_names_[1],str(x))) # silt g/kg
        C1 = readmap("{0}{1}.map".format(SG_names_[2],str(x)))  # clay g/kg
        OC1 = readmap("{0}{1}.map".format(SG_names_[3],str(x)))  # organic carbon in dg/kg
        Gravel1 = readmap("{0}{1}.map".format(SG_names_[4],str(x))) # coarse fragments cm3/dm3,
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

        mask = ifthen(S+C+Si > 0.01,mask) # assume areas where sum text is not 1 = MV

        OM = OM*mask
        report(OM, om1)
        Dens = 1.0
        if docover:
           Dens = (1-0.1*cover)  #scalar(1.0)
        # density factor is 1.0, but could be made lower for organic soils and higher for compacted urban areas.
        bdsg = bd1*10            #bulkdensity cg/m3 to kg/m3
        bdsg = ifthenelse(bd1 < 1,standardBD,bdsg) # replace areas with MV bdsg to standard BD
        Gravel = Gravel1/1000  # from cm3/dm3 (1000 cc in a liter)
        Densityfactor = bdsg/standardBD*Dens #(1-0.1*cover)
        report(Densityfactor,Densityfactor1)

        #scalar(1.0)  # range 0.9 to 1.15
        # calculated as the bulk density from soilgrids divided by some standard bd
        # multiple regression from excel

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

        Ksat = mask*max(0.0, 1930*(PoreMcomp)**(3-LAMBDA)*GravelRedKsat)  #AN18)
        BD = Gravel*2.65+(1-Gravel)*Dens_comp* mask     #U18
        WP = M1500adj*mask
        FC = M33adj* mask
        PAW = (M33adj - M1500adj)*(1-Gravel)* mask
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

        Coh = max(1.0, 4.316*ln(C+1.0) - 6.955)
        # log fit using values below

        #Coh = lookupscalar("claycoh.tbl",C)*mask
        # content of claycoh.tbl
        # [,20>   2
        # [20,35> 3
        # [35,40> 9
        # [40,55> 10
        # [55,60> 11
        # [60,100> 12

        report(Coh, Coh1)

### ---------- class DEMderivatives() ---------- ###

class DEMderivatives(StaticModel):
    def __init__(self):
        StaticModel.__init__(self)
    def initial(self):
        mask = mask_;

        barriers = scalar(0) #readmap(buffersinName)*mask
        report(barriers,buffersName);

        DEM = readmap(DEMinName)
        DEMm = DEM + barriers;
        report(DEMm, DEMName)

        mainout = readmap(mainoutinName)*mask
        chanm = readmap(riversinName)*mask
        size = catchmentsize

        Ldd = lddcreate (DEMm-chanm*10-mainout*10, size, size, size, size)
        report(Ldd, lddName)
        # runoff flow network based on dem, main outlet, channels and barriers
        #report outlet = mainout; #pit(Ldd);
        grad = sin(atan(slope(dem)))
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

        report(shade,shadeMap)  # not used in lisem


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
        report(soildepth1,soildep2Name)


### ---------- class SurfaceMaps() ---------- ###

class SurfaceMaps(StaticModel):
    def __init__(self):
        StaticModel.__init__(self)
    def initial(self):
        mask = mask_;
        report rr = max(lookupscalar(lutbl, 1, unitmap) * mask, 0.01);
         # micro relief, random roughness (=std dev in cm)

        report mann = lookupscalar(lutbl, 2, unitmap) * mask;
         # in the lisem code Manning's n is increased with house effect

        report crust = mask*0;

         # crust fraction assumed zero

        # report comp = if (road eq 1 or road eq 5, 0.2, 0)*mask;
         #fraction compacted, e.g. dirt roads
        report ksatcomp = 0.1*mask;  # 0.1 mm/h over width of dirt road

        report hard = hard_surf*mask;
         #hard surface, here airports and large impenetrable areas

        report roadwidth = if (road eq 1, 10, if(road eq 2, 6, if(road eq 3, 4, 0)))*mask;

  report D50 = 40 * mask;      # fine material
  report D90 = 100*mask;
  report cohplant = coverc * 5 * mask;  # additional plant root strength
  report aggrstab = 0 * mask;  # aggregate stability
  report cropheight = lookupscalar(lutbl, 3, unitmap) * mask; #plant height in m

### ---------- START ---------- ###


workingDir = 'C:/data/India/Cauvery/Base/'
os.chdir(workingDir)

Debug_ = False #True


# tif file for projection ESPG id
maskname_ = 'dem200m.tif'
masktif = gdal.Open(maskname_, gdalconst.GA_ReadOnly)
proj = osr.SpatialReference(wkt=masktif.GetProjection())
ESPG = proj.GetAttrValue('AUTHORITY',1)

# pcraster file for exact basin mask
masknamemap_ = 'maskbasin.map'
setclone(masknamemap_)

mask_ = readmap(masknamemap_)





staticModelDEM = StaticFramework(DEMderivatives())
staticModelDEM.run()

staticModelSURF = StaticFramework(SurfaceMaps())
staticModelSURF.run()

print("downloading SOILGRIDS layers...")
SG_names_ = ['sand','silt','clay','soc','cfvo','bdod']
# # texture, doil organic carbon, course fragments, bulk dens
# for x in range(0,6):
#     GetSoilGridsLayer(masknamemap_,ESPG,SG_names_[x],2,1)
# for x in range(0,6):
#     GetSoilGridsLayer(masknamemap_,ESPG,SG_names_[x],4,2)

initmoisture_ = 0.7
standardbulkdensity_ = 1450.0
docover = False
cover_ = scalar(0) #readmap("per.map")
# optional, can use for bulkdensity, higher cover is more structure, lower density

staticModel = StaticFramework(PedoTransfer())
layer_ = 1
staticModel.run()
layer_ = 2
staticModel.run()

print("Done")