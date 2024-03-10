# lisemDBASEgenerator
# global vraiables and initialisation
#
# author: V.G.Jetten @ 2022
# University of Twente, Faculty ITC
# this software has copyright model: GPLV3
# this software has a disclaimer


# In conda make sure the following libs are installed:
#     conda create --name lisem
#     conda activate lisem
#     conda install -c conda-forge pcraster owslib scipy gdal

# gdal
from osgeo import gdal, gdalconst, osr, ogr
#from owslib.wcs import WebCoverageService
import numpy as np

# pcraster
from pcraster import *
from pcraster.framework import *

# operation system
import subprocess  # call exe from wihin script
import os          # operating system, change dir
import time,sys    # read commandline arguments

# lisem DBASE generator classes 
import lisGlobals as lg
import lisDemDerivatives
import lisChannels
import lisSurface
import lisSoils
import lisErosion
import lisDams
import lisInfrastructure
import lisRainfall

SGconda = 1
try:
    import soilgrids
except ImportError:    
    SGconda = 0


# PCRaster global options
setglobaloption("lddin")
setglobaloption("lddfill")
setglobaloption("matrixtable")

# update_progress() : Displays or updates a console progress bar
def update_progress(progress):
    barLength = 50 # Modify this to change the length of the progress bar
    if progress >= 0.99:
        progress = 1
    block = int(round(barLength*progress))
    text = "\rProcessing: [{0}] {1:.3g}% ".format( "#"*block + "-"*(barLength-block), progress*100)
    sys.stdout.write(text)
    sys.stdout.flush()


if __name__ == "__main__":
    gdal.UseExceptions()
    
    print(">>> Reading interface options",flush=True)
   # print(sys.path)
    lg.initialize() 
    # define all global variables and initialize
    # also get GDAL bounding box, ESPG, rows cols etc
    # cut LULC map to size
               
    # DEM derivatives, LDD, gradient, soil depth
    if lg.doProcessesDEM == 1 :
        print('>>> Create dem derivatives, slope, LDD', flush=True)
        obj = lisDemDerivatives.DEMderivatives()        
        staticModelDEM = StaticFramework(obj) #DEMderivatives())
        staticModelDEM.run()
    
    # Channel dimensions and characteristics
    if lg.doProcessesChannels == 1:    
        print('>>> Creating channel maps', flush=True)
        obj = lisChannels.ChannelMaps()
        staticModelCH = StaticFramework(obj)
        staticModelCH.run()       

    # surface variables related to LULC
    if lg.doProcessesLULC == 1:   
        print('>>> Creating surface and land use related maps', flush=True)
        obj = lisSurface.SurfaceMaps()
        staticModelSURF = StaticFramework(obj)
        staticModelSURF.run()
    print(SGconda,flush=True)
    if SGconda == 1:
        # soil processes, SOILGIRDS and pedotransfer functions Saxton and Rawls
        if lg.doProcessesInfil == 1 and lg.doProcessesSG == 1:    
            print(">>> Downloading SOILGRIDS layers from conda package", flush=True)        
            for x in range(6):
                lg.SG_horizon_ = 1
                lisSoils.GetSoilGridsLayerConda(x)
            for x in range(6):
                lg.SG_horizon_ = 2
                lisSoils.GetSoilGridsLayerConda(x)
    else : 
        # soil processes, SOILGIRDS and pedotransfer functions Saxton and Rawls
        if lg.doProcessesInfil == 1 and lg.doProcessesSG == 1:    
            print(">>> Downloading SOILGRIDS layers from web server https://maps.isric.org", flush=True)        
            for x in range(6):
                lg.SG_horizon_ = 1
                lisSoils.GetSoilGridsLayer(x)
            for x in range(6):
                lg.SG_horizon_ = 2
                lisSoils.GetSoilGridsLayer(x)


    if lg.doProcessesInfil == 1 and lg.doProcessesSGInterpolation == 1:
        print(">>> Inverse distance interpolation SOILGRIDS layers for missing values ", flush=True)
        obj = lisSoils.SoilGridsTransform()
        staticModel = StaticFramework(obj)
        #update_progress(0)
        for x in range(6):
            lg.SG_horizon_ = 1
            #print(lg.SG_horizon_, flush = True)
            lg.SG_mapnr_ = x
            staticModel.run()
            update_progress((x+1)/12)
        for x in range(6):
            lg.SG_horizon_ = 2
            #print(lg.SG_horizon_, flush = True)
            lg.SG_mapnr_ = x
            staticModel.run()        
            update_progress((x+7)/12)
        #update_progress(1)    
        print("\n");
     
    if lg.doProcessesInfil == 1 and lg.useCorrText == 1:
        print(">>> Correcting texture to area guide values", flush=True)
        obj = lisSoils.CorrectTextures()
        staticModel = StaticFramework(obj)
        staticModel.run()

    if lg.doProcessesInfil == 1:
        print(">>> Creating soil physical maps for infiltration", flush=True)
        obj = lisSoils.PedoTransfer()
        staticModel = StaticFramework(obj)
        lg.SG_horizon_ = 1
        staticModel.run()
        lg.SG_horizon_ = 2
        staticModel.run()

    # splash and flow erosion variables
    if lg.doProcessesErosion == 1:
        obj = lisErosion.ErosionMaps()
        staticModel = StaticFramework(obj)
        staticModel.run()
        
    # rasterize infrastructure and buildings shape files 
    if lg.doProcessesInfrastructure == 1 :
        print('>>> Rasterize shapefiles of buildings and roads', flush=True)
        obj = lisInfrastructure.InfrastructureMaps()        
        staticModelBuild = StaticFramework(obj) 
        lg.shapeNr = 1
        staticModelBuild.run()
        lg.shapeNr = 2
        staticModelBuild.run()
               
    # adjust rivers for large dams
    if lg.doProcessesDams == 1:
        print('>>> Adjust maps for Dams', flush=True)
        obj = lisDams.DamsinRivers()
        staticModelDams = StaticFramework(obj)
        staticModelDams.run()
   

    # adjust rivers for large dams
    if lg.doProcessesRain == 1:   # add option if GPM later
        print('>>> Process GPM rainfall', flush=True)
        obj = lisRainfall.GPMRainfall()
        staticModelDams = StaticFramework(obj)
        staticModelDams.run()   
       
    print("Done")

