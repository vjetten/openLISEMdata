# lisemDBASEgenerator
# global vraiables and initialisation
#
# author: V.G.Jetten @ 2022, 2023, 2024
# University of Twente, Faculty ITC
# this software has copyright model: GPLV3
# this software has a disclaimer
# last edit: 17 Jan 2024

from owslib.wcs import WebCoverageService
from pcraster import *
from pcraster.framework import *
from osgeo import gdal, gdalconst, osr, ogr
import numpy as np
import lisGlobals as lg
from os.path import exists

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
    #gdal.FillNodata(in_ds.GetRasterBand(1), None, out_ds.GetRasterBand(1), lg.nrCols, 0)
    gdal.FillNodata(out_ds.GetRasterBand(1), None, lg.nrCols, 0)

    # Close datasets
    in_ds = None
    out_ds = None

# okay but does not work with very large datasets
def inverse_distance_weighting(points, values, target_points, power=2, smoothing=0):
    distances = np.linalg.norm(points - target_points[:, np.newaxis], axis=2)
    weights = 1.0 / (distances ** power + smoothing)
    weights /= np.sum(weights, axis=1)[:, np.newaxis]
    interpolated_values = np.sum(weights * values, axis=1)
    return interpolated_values

def interpolate_tiff(input_tiff, output_tiff, power=2, smoothing=0):
    gdal.UseExceptions()

    src_ds = gdal.Open(input_tiff)
    band = src_ds.GetRasterBand(1)  # Assuming a single band for simplicity
    nodata_value = band.GetNoDataValue()
    print(nodata_value,flush = True)
    geotransform = src_ds.GetGeoTransform()
    width = src_ds.RasterXSize
    height = src_ds.RasterYSize

    points = np.array([(i % width, i // width) for i in range(width * height) if band.ReadAsArray(i % width, i // width, 1, 1)[0] != nodata_value])
    values = band.ReadAsArray()[points[:, 1], points[:, 0]]

    all_points = np.array([(i % width, i // width) for i in range(width * height)])
    all_indices = np.arange(all_points.shape[0])

    missing_points = np.array([(i % width, i // width) for i in range(width * height) if band.ReadAsArray(i % width, i // width, 1, 1)[0] < 1e-5]) #== nodata_value])
    missing_indices = np.arange(missing_points.shape[0])
        
    interpolated_values = inverse_distance_weighting(
        points, values, missing_points, power=power, smoothing=smoothing
    )

    output_array = band.ReadAsArray()
    output_array[missing_points[:, 1], missing_points[:, 0]] = interpolated_values

    driver = gdal.GetDriverByName("GTiff")
    dst_ds = driver.Create(output_tiff, width, height, 1, gdal.GDT_Float32)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(src_ds.GetProjection())
    dst_ds.GetRasterBand(1).WriteArray(output_array)
    dst_ds.GetRasterBand(1).SetNoDataValue(nodata_value)

    src_ds = None
    dst_ds = None



class GetSoilGridsLayer:
    "downbloading a SOILGRIDS layer from WCS service"
    def __init__(self, x = 0):
          
        varname = lg.SG_names_[x]
        # depth string
        if lg.SG_horizon_ == 1 :
            ID = lg.SG_layers_[lg.optionSG1-1] 
        if lg.SG_horizon_ == 2 :
            ID = lg.SG_layers_[lg.optionSG2-1]             
            
        self.debug = 0 #Debug_
        vname = varname  # filename for display
               
        # make a readable name for output to screen       
        if x == 3: vname='Soil Org Carbon' 
        if x == 4: vname='Gravel' 
        if x == 5: vname='Bulk Density' 

        print("   => Downloading SOILGRIDS layer "+varname+ID+" as LISEM soil layer "+str(lg.SG_horizon_)+": "+vname+" content", flush=True)

        ESPGs = 'urn:ogc:def:crs:EPSG::{0}'.format(lg.ESPG)

        if self.debug == 1:
            print("Open SOILGRIDS WCS: "+varname+ID, flush=True)

        url = "http://maps.isric.org/mapserv?map=/map/{}.map".format(varname)
        wcs = WebCoverageService(url, version='1.0.0')
        if self.debug == 1:
            cov_list = list(wcs.contents)
            mean_covs = [k for k in wcs.contents.keys() if k.find("mean") != -1]
            print(mean_covs, flush = True)

        variable = varname+ID
        varout = varname+str(lg.SG_horizon_)
        outputnametif = "{0}.tif".format(varout)
        temptif = 'temp.tif'

        dx1 = 250
        dy1 = 250

        # make a tif but the nrrows and nrcols are related to 250m now
        # force maskbox but this is not exact, add one dx1,dy1 because sometimes the box is smaller than the DEM because of rounding off
        Maskbox = [lg.maskbox[0]-dx1,lg.maskbox[1]-dy1,lg.maskbox[2]+2*dx1,lg.maskbox[3]+2*dy1]
        # get data as temp geotif and save to disk
        response = wcs.getCoverage(identifier=variable,crs=ESPGs,bbox=Maskbox,resx=dx1,resy=dy1,format='GEOTIFF_INT16')
        with open('temp.tif', 'wb') as file:
             file.write(response.read())

        src = gdal.Warp(outputnametif, temptif, srcNodata = 0, xRes=dx1, yRes=dy1, outputBounds=Maskbox, resampleAlg = 'near', outputType = gdal.GDT_Float64 )     
        
        os.remove(temptif)
        src = None
        response = None
        


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
            
        src = gdal.Warp(tempwarptif,temptif, srcNodata = 0, xRes=lg.dx, yRes=lg.dy, outputBounds=lg.maskbox, resampleAlg = resa, outputType = gdal.GDT_Float64 )
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
            distriv = spread(cover(nominal(chanm > 0),0),0,1)*mask
            rivfact = -0.5*distriv/mapmaximum(distriv)
            # perpendicular distance to river, closer gives deeper soils

        report(rivfact,"rf.map")
        
        if lg.SG_horizon_ == 1 :
            soildepth1 = lg.soildepth1depth*mask
            report(soildepth1,lg.soildep1Name)
        if lg.SG_horizon_ == 2 :
            # steeper slopes giver undeep soils
            soild = cover((1-min(1,slope(DEM)))+rivfact+5*profcurv(DEM),0)*mask #
            #a bit after Kuriakose et al
            soild = windowaverage(soild,3*celllength())
            # smooth because soil depth does not follow dem exactly        
            smin = mapminimum(soild)
            smax = mapmaximum(soild)
            soild = (soild-smin)/(smax-smin)
            report(soild,"sd.map")
            soildb = soild*(lg.soildepth2depth-lg.soildepth1depth) 
            #min(lg.soildepth2depth,lg.soildepth2depth*(soild)**1.5) # CHARIM, somehow used 1.5...?
            soildepth1 = lg.soildepth1depth*mask
            soildepth2 = soildepth1+soildb # add 100 mm to avoid soildepth2 of 0 in lisem
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
