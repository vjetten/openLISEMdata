# lisemDBASEgenerator
# global vraiables and initialisation
#
# author: V.G.Jetten @ 2022, 2023, 2024
# University of Twente, Faculty ITC
# this software has copyright model: GPLV3
# Soilgrids layers have copyright model: https://creativecommons.org/licenses/by/4.0/
# this software has a disclaimer
# last edit: 11 May feb 2024

from owslib.wcs import WebCoverageService
from pcraster import *
from pcraster.framework import *
from osgeo import gdal, gdalconst, osr, ogr
import numpy as np
import lisGlobals as lg
from os.path import exists
#import threading
import math 

SGconda = 1
try:
    from soilgrids import SoilGrids   
except ImportError:    
    SGconda = 0


def fill_nodata(input_raster, output_raster):
    # Open the input raster dataset
    in_ds = gdal.Open(input_raster, gdal.GA_ReadOnly)
    if in_ds is None:
        print(f"Error: Could not open input raster '{input_raster}'")
        return

    # Create an output raster dataset
    driver = gdal.GetDriverByName("GTiff")
    out_ds = driver.CreateCopy(output_raster, in_ds)
    if out_ds is None:
        print(f"Error: Could not create output raster '{output_raster}'")
        return
    
    # Use gdal.FillNodata to fill nodata values
    gdal.FillNodata(out_ds.GetRasterBand(1), None, lg.nrCols, 0)

    # Close datasets
    in_ds = None
    out_ds = None
    

class GetSoilGridsLayerConda:
    "downbloading a SOILGRIDS layer"
    def __init__(self, x = 0):
          
        varname = lg.SG_names_[x]
        # depth string
        if lg.SG_horizon_ == 1 :
            ID = lg.SG_layers_[lg.optionSG1-1] 
        if lg.SG_horizon_ == 2 :
            ID = lg.SG_layers_[lg.optionSG2-1]             
            
        vname = varname  # filename for display
               
        # make a readable name for output to screen       
        if x == 3: vname='Soil Org Carbon' 
        if x == 4: vname='Gravel' 
        if x == 5: vname='Bulk Density' 

        print("   => Downloading "+varname+ID+" as LISEM soil layer "+str(lg.SG_horizon_)+": "+vname+" content", flush=True)

        mean_covs = varname+ID
        varout = varname+str(lg.SG_horizon_)
        
        outputnametif = "{0}.tif".format(varout)
        temptif = '_temp.tif'
        if exists(temptif) :
            os.remove(temptif)
        
        # convert the mask box from the project EPSG to EPSG::152160
        
        # make a polygon of the maskbox coordinates
        bbox = lg.maskbox
        ring = ogr.Geometry(ogr.wkbLinearRing)
        ring.AddPoint_2D(bbox[0], bbox[1])  # lower left
        ring.AddPoint_2D(bbox[2], bbox[1])  # lower right
        ring.AddPoint_2D(bbox[2], bbox[3])  # upper right
        ring.AddPoint_2D(bbox[0], bbox[3])  # upper left
        ring.AddPoint_2D(bbox[0], bbox[1])  # close the ring
        bbox_geom = ogr.Geometry(ogr.wkbPolygon)
        bbox_geom.AddGeometry(ring)
        
        # Define the source and target spatial reference systems
        src_sr = osr.SpatialReference()
        src_sr.ImportFromEPSG(lg.EPSG)
        target_sr = osr.SpatialReference()
        target_sr.ImportFromProj4('+proj=igh +datum=WGS84 +no_defs +towgs84=0,0,0')
        # transform the box
        transform = osr.CoordinateTransformation(src_sr, target_sr)
        bbox_geom.Transform(transform)
        transformed_bbox = bbox_geom.GetEnvelope()
        # expand by one cell
        x_min = transformed_bbox[0]-250
        x_max = transformed_bbox[1]+250
        y_min = transformed_bbox[2]-250
        y_max = transformed_bbox[3]+250
        Maskbox = [x_min,y_min,x_max,y_max]

        EPSGs = 'urn:ogc:def:crs:EPSG::152160'
       
        if SGconda == 1:
            #print("conda",flush = True)
            soil_grids = SoilGrids()
            data = soil_grids.get_coverage_data(service_id=varname, coverage_id=mean_covs, west = x_min,south=y_min,east =x_max,north=y_max, crs=EPSGs, output=temptif)
        else :            
            url = "https://maps.isric.org/mapserv?map=/map/{0}.map".format(varname)
            wcs = WebCoverageService(url, version='1.0.0') 
            response = wcs.getCoverage(identifier=mean_covs,crs=EPSGs, bbox=Maskbox,resx=250,resy=250,format='GEOTIFF_INT16')               
            with open(temptif, 'wb') as file:
                file.write(response.read())
         
        input_dataset = gdal.Open(temptif)        
        gdal.Warp(outputnametif, input_dataset, 
            format='GTiff', 
            srcNodata = -32768,
            xRes=250, yRes=250, 
            outputType = gdal.GDT_Float32)        
        
        # Close the datasets
        input_dataset = None
        response = None
        if exists(temptif) :
            os.remove(temptif)


### ---------- class SoilGridsTransform() ---------- ###

class SoilGridsTransform(StaticModel):
    # convert tif to map and do inverse distance interpolation to fill missing values
    def __init__(self, mask=0, mapnr=1):
        StaticModel.__init__(self)
    def initial(self):
        DEM = lg.DEM_
        mask = lg.mask_
        xs = str(lg.SG_horizon_)
        mapnr = lg.SG_mapnr_
        name = ""
        factor = 1.0
        
        if mapnr == 0: name = "sand{0}".format(xs); factor = 0.001  # fraction sand, server gives g/kg
        if mapnr == 1: name = "clay{0}".format(xs); factor = 0.001  # fraction silt, server gives g/kg
        if mapnr == 2: name = "silt{0}".format(xs); factor = 0.001  # fraction clay, server gives g/kg
        if mapnr == 3: name =  "soc{0}".format(xs); factor = 0.0001 # fraction SOC, server give dg/kg
        if mapnr == 4: name = "cfvo{0}".format(xs); factor = 0.001  # fraction gravel, server gives cm3/dm3
        if mapnr == 5: name = "bdod{0}".format(xs); factor = 10.0     # bulk density kg/m3, server gives cg/cm3 

        nametif = name+".tif"
        namemap = name+".map"
        temptif = "temp.tif"
        tempwarptif = "temp1.tif"

        #interpolate_tiff(nametif,temptif, power=2, smoothing=0)
        fill_nodata(nametif, temptif)


        # create a high res resampled version of the downloaded tif, using maskbox, forcing float64
        resa = 'near'
        if lg.optionResample == 1 :
            resa = 'bilinear'
        if lg.optionResample == 2 :
            resa = 'cubic'       
            
        warp_options = {
            "xRes": lg.dx,
            "yRes": lg.dy,
            "outputBounds": lg.maskbox,
            "resampleAlg": resa,
            "outputType": gdal.GDT_Float32,
            "dstSRS": 'EPSG:{0}'.format(lg.EPSG)
        }
  
        src = gdal.Warp(tempwarptif, temptif, **warp_options)    
            
        #src = gdal.Warp(tempwarptif,temptif, srcNodata = 0, xRes=lg.dx, yRes=lg.dy, outputBounds=lg.maskbox, resampleAlg = resa, outputType = gdal.GDT_Float64 )
        src = None
        
        #open the tif and create PCRaster copy
        map_ = scalar(readmap('temp1.tif'))
        map_ *= factor
        report(map_,namemap)
        os.remove('temp.tif')
        os.remove('temp1.tif')
        ET = None
        

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
        mask = lg.mask_
        DEM = lg.DEM_
        xs = str(lg.SG_horizon_)
         
        print(">>> Creating infiltration parameters for layer "+xs, flush=True)

        S1 = readmap("sand{0}.map".format(xs))  # sand fraction
        Si1 = readmap("silt{0}.map".format(xs)) # silt fraction 
        C1 = readmap("clay{0}.map".format(xs))  # clay fraction
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

        OMaddition = scalar(0.0)*mask
        if (lg.doProcessesLULC) :
            lun = readmap(lg.landuseName)
            if lg.useLUdensity == 1 and lg.SG_horizon_ == 1:
                OMaddition =  lookupscalar(lg.LULCtable, 8, nominal(lun)) * mask
        
        CorrectionOM = 0.0
        if lg.useCorrOM == 1 :             # and lgSG_horizon_ == 1:
            CorrectionOM = lg.CorrOM            
        
        S = S1 # 
        C = C1 # 
        Si = Si1 #1-S-C #Si1 
        
        if mapmaximum(S+C+Si) > 99 :
        # if sum > 99 assume in percetages instead of fraction
            S = S/100
            C = C /100
            Si = Si/100
                        
        OC = OC1*100  # conversion OC from fraction to percentage
        OM = (min(OC*1.73,10) +  OMaddition) * CorrectionOM  #conversion org carbon to org matter factor 2
              
        report(OM, om1)

        Gravel = 0 #fGrv
        #if lg.useNoGravel == 1 :
        #    Gravel *= 0.2

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
        bddf = 1000*(1-poredf1)*2.65  # bulk derived from pore with df 1 so standard

        bdodscaled = bdod/areaaverage(bdod,boolean(bdod))-1.0  #scale around 0
        Densityfactor = standardBD/1350+0.5*bdodscaled 
        DensityfactorLU = 1.0
        # average between the interface bulk density and the bdod from soilgrids
        
        if lg.useLUdensity == 1 and lg.SG_horizon_ == 1:
            DensityfactorLU =  lookupscalar(lg.LULCtable, 5, nominal(lg.lun)) * mask
            Densityfactor += (DensityfactorLU - 1.0)
            #ifthenelse(DensityfactorLU == 1.0, Densityfactor, 0.5*(Densityfactor + DensityfactorLU))#- 1.0)
        #Densityfactor = min(Densityfactor,DensityfactorLU)*standardBD/bdod*mask
        
        Densityfactor = max(0.9,min(1.2,Densityfactor))            
        # limit between 0.9 and 1.2 else can generate missing values         
        report(Densityfactor,DF1)
        
        Dens_comp = Dens_om * Densityfactor  #AG18) =AF18*(I18)
        PORE_comp =(1-Dens_om/2.65)-(1-Dens_comp/2.65)  #AI18) =(1-AG18/2.65)-(1-AF18/2.65)
        M33comp = M33adj + 0.2*PORE_comp  #AJ18)  =Z18+0.2*AI18
        report(Dens_comp,BDdf)
        #output maps
        POROSITY = (1-Dens_comp/2.65)*mask  #AH18)               
        
        PoreMcomp = POROSITY-M33comp  #AK18)
        LAMBDA = (ln(M33comp)-ln(M1500adj))/(ln(1500)-ln(33))  #AL18)
        GravelRedKsat =(1-Gravel)/(1-Gravel*(1-1.5*(Dens_comp/2.65)))  #AM18)
        # NOTE: soilgrids gravel is a volume fraction while the PTF need a weight fraction
        # if gravel = 0 then gravelreduction = 1
        report(GravelRedKsat,'gravred.map')       
        report(LAMBDA,'lambda.map')
        report(POROSITY,'PoreMcomp.map')
        
        Ksat = mask*max(0.0, 1930*(PoreMcomp)**(3-LAMBDA))#*GravelRedKsat)  #AN18)
        BD = Gravel*2.65+(1-Gravel)*Dens_comp* mask     #U18
        WP = M1500adj*mask
        FC = M33adj* mask
        PAW = (M33adj - M1500adj)*(1-Gravel)* mask
        
        Ksat = ifthenelse(DensityfactorLU == 0,0,Ksat)
        POROSITY = ifthenelse(DensityfactorLU == 0,0,POROSITY)
        FC = ifthenelse(DensityfactorLU == 0,0,FC)
        WP = ifthenelse(DensityfactorLU == 0,0,WP)

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
        #SS = S**2
        #CC = C**2
        #PP = POROSITY**2
        # 10.2 is from kPa to cm!
        # I cannot find where this comes from!!!
        #Psi1 =10.2*exp(6.53-7.326*POROSITY+15.8*CC+3.809*PP+3.44*S*C-4.989*S*POROSITY+16*SS*PP+16*CC*PP-13.6*SS*C-34.8*CC*POROSITY-7.99*SS*POROSITY)
        #Psi1 = Psi1 * max(0.1,1-fractionmoisture)
        # correct psi slightly for initmoisture, where psi1 is assumed to corrspond to FC
        #bB = (ln(1500)-ln(33))/(ln(FC)-ln(WP))
        #aA = exp(ln(33)+bB*ln(FC))
        #Psi1= aA * initmoist**-bB * 10.2
        # 10.2 is from kPa to cm
        
        # Rawls in https://www.gsshawiki.com/Infiltration:Parameter_Estimates		
        ks = max(0.5,min(ln(Ksat),1000))
        lamb = min(max(0.1,0.0849*ks+0.159),0.7)
        psi1ae = exp( -0.3012*ks + 3.5164)   #in cm 			
        #Psi1 = exp(-0.3382*ks + 3.3425) #wetting front
        Psi1 = psi1ae*pow(initmoist/POROSITY,-1/lamb) #based on theta in cm
        #Psi1 = max(Psi1,psi1ae)
        report(psi1ae,"psiae.map")
       
        report(Psi1,psi1)
        report(initmoist/POROSITY,"se1.map")
        
        
        #SOILDEPTH
        rivfact = mask*0
        chanm = mask*0
        if lg.riverExists:
            chanm = readmap(lg.BaseDir+lg.riversbaseName) 
            if mapmaximum(chanm) > 0 :
                distriv = spread(cover(nominal(chanm > 0),0),0,1)*mask
                rivfact = -0.5*distriv/mapmaximum(distriv)
                # perpendicular distance to river, closer gives deeper soils
        
        if lg.SG_horizon_ == 1 :
            soildepth1 = lg.soildepth1depth*mask
            report(soildepth1,lg.soildep1Name)
        if lg.SG_horizon_ == 2 :
            if lg.soildepthMethod == 1 :
                # steeper slopes giver undeep soils
                soild = cover((1-min(1,slope(DEM)))+rivfact+profcurv(DEM),0)*mask #
                #a bit after Kuriakose et al
                # scale between 0 and 1 and smooth
                soild = windowaverage(soild,lg.dx*5)
                minm = mapminimum(soild)
                maxm = mapmaximum(soild)
                sd = (lg.soildepth2depth-lg.soildepth1depth-100)*(soild-minm)/(maxm-minm)
            else :
                # scale DEM between 0 and 1
                demr = windowaverage(DEM**0.5, lg.dx*5)
                demr = (demr - mapminimum(demr))/(mapmaximum(demr) - mapminimum(demr))
                sd = (lg.soildepth2depth-lg.soildepth1depth-100) * demr
            soildepth2 = (lg.soildepth1depth+100+sd)*mask
            report(soildepth2,lg.soildep2Name)
       
### ---------- class CorrectTextures() ---------- ###

class CorrectTextures(StaticModel):
    # correct soilgrids textures to field values and make sure sum = 1
    def __init__(self,mask=0):
        StaticModel.__init__(self)
    def initial(self):
        mask = lg.mask_
 
        S = readmap("sand1.map") 
        Si = readmap("silt1.map")
        C = readmap("clay1.map") 
        
        
       #Si = (mapmaximum(Si) - Si)/(mapmaximum(Si)-mapminimum(Si))
       #Si = (Si *(0.353-0.963)+1)*0.963
       #S = (mapmaximum(S) - S)/(mapmaximum(S)-mapminimum(S))
       #S = (S *(0.14-0.612)+1)*0.612
       #C = min(1.0,max(0,1-Si-S))
        
        
        S = S * lg.CorrSand/areaaverage(S,boolean(S+1))
        C = C * lg.CorrClay/areaaverage(C,boolean(C+1))
       
        Si = 1 - S - C
        report(S, "sand1.map");
        report(C, "clay1.map");
        report(Si,"silt1.map");

        S = readmap("sand2.map") 
        Si = readmap("silt2.map")
        C = readmap("clay2.map") 
        
        S = S * lg.CorrSand/areaaverage(S,boolean(S+1))
        C = C * lg.CorrClay/areaaverage(C,boolean(C+1))
       
        Si = 1 - S - C
        
        report(S, "sand2.map");
        report(C, "clay2.map");
        report(Si,"silt2.map");
