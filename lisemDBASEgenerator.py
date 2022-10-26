# lisemDBASEgenerator
# global vraiables and initialisation
#
# author: V.G.Jetten @ 2022
# University of Twente, Faculty ITC
# this software has copyright model: GPLV3
# this software has a disclaimer


# In conda make sure the following libs are installed:
#     conda create --name lisem python
#     conda activate lisem
#     conda install -c conda-forge pcraster owslib scipy gdal

# gdal
from osgeo import gdal, gdalconst, osr
from owslib.wcs import WebCoverageService

# pcraster
from pcraster import *
from pcraster.framework import *

# operation system
import subprocess  # call exe from wihin script
import os          # operating system, change dir
import time,sys         # read commandline arguments

# lisem DBASE generator classes 
import lisGlobals as lg
import lisDemDerivatives
import lisChannels
import lisSurface
import lisSoils
import lisErosion
import lisDams

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


class InfrastructureMaps(StaticModel):
    def __init__(self):
        StaticModel.__init__(self)
    def initial(self):
        mask = mask_
    # nrRows = maskgdal.RasterYSize
    # nrCols = maskgdal.RasterXSize
    # dx = maskgdal.GetGeoTransform()[1]
    # dy = maskgdal.GetGeoTransform()[5]
    # llx = maskgdal.GetGeoTransform()[0]
    # ury = maskgdal.GetGeoTransform()[3]
    # urx = llx + nrCols*dx
    # lly = ury + dy*nrRows
    # maskbox = [llx,lly,urx,ury]
    # ESPG = int(ESPGnumber)
        shape_v = ogr.Open(lg.shpName)
        shape_l = shape_v.GetLayer()
        output = lg.nametif
        x_res = lg.dx/5.0
        y_res = x_res
        target_ds = gdal.GetDriverByName('GTiff').Create(output, x_res, y_res, 1, gdal.GDT_Byte)
        target_ds.SetGeoTransform(lg.llx, x_res, 0, lg.lly, 0, x_res))
        band = target_ds.GetRasterBand(1)
        NoData_value = -999999
        band.SetNoDataValue(NoData_value)
        band.FlushCache()
        gdal.RasterizeLayer(target_ds, [1], shape_l) #, options=["ATTRIBUTE=hedgerow"])

        target_ds = None
        
        
        
        map_ = scalar(readmap(nametif))
        
        


if __name__ == "__main__":
    print(">>> Reading interface options",flush=True)
    
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
        print('>>> Create channel maps', flush=True)
        obj = lisChannels.ChannelMaps()
        staticModelCH = StaticFramework(obj)
        staticModelCH.run()       

    # surface variables related to LULC
    if lg.doProcessesLULC == 1:   
        print('>>> Create surface and land use related maps', flush=True)
        obj = lisSurface.SurfaceMaps()
        staticModelSURF = StaticFramework(obj)
        staticModelSURF.run()

    # soil processes, SOILGIRDS and pedotransfer functions Saxton and Rawls
    if lg.doProcessesInfil == 1 and lg.doProcessesSG == 1:    
        print(">>> Downloading SOILGRIDS layers from web server ISRIC", flush=True)        
        for x in range(0,6):
            lisSoils.GetSoilGridsLayer(lg.masknamemap_,lg.ESPG,lg.SG_names_[x],lg.optionSG1,1)
        for x in range(0,6):
            lisSoils.GetSoilGridsLayer(lg.masknamemap_,lg.ESPG,lg.SG_names_[x],lg.optionSG2,2)

    if lg.doProcessesInfil == 1 and lg.doProcessesSGInterpolation == 1:
        print(">>> Inverse distance interpolation SOILGRIDS layers for missing values ", flush=True)
        obj = lisSoils.SoilGridsTransform()
        update_progress(0)
        for x in range(0,6):
            lg.layer_ = 1
            lg.mapnr_ = x
            staticModel = StaticFramework(obj)
            staticModel.run()
            update_progress((x+1)/12)
        for x in range(0,6):
            layer_ = 2
            mapnr_ = x
            staticModel = StaticFramework(obj)
            staticModel.run()        
            update_progress((x+7)/12)
        update_progress(1)    

    
    if lg.doProcessesInfil == 1:
        print(">>> Creating soil physical maps for infiltration", flush=True)
        obj = lisSoils.PedoTransfer()
        staticModel = StaticFramework(obj)
        lg.layer_ = 1
        staticModel.run()
        lg.layer_ = 2
        staticModel.run()

    # splash and flow erosion variables
    if lg.doProcessesErosion == 1:
        obj = lisErosion.ErosionMaps()
        staticModel = StaticFramework(obj)
        staticModel.run()
       
    # adjust rivers for large dams
    if lg.doProcessesDams == 1:
        print('>>> Adjust maps for Dams', flush=True)
        obj = lisDams.DamsinRivers()
        staticModelDams = StaticFramework(obj)
        staticModelDams.run()

    print("Done")

