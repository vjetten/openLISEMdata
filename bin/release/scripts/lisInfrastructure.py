# lisemDBASEgenerator
# global vraiables and initialisation
#
# author: V.G.Jetten @ 2022
# University of Twente, Faculty ITC
# this software has copyright model: GPLV3
# this software has a disclaimer

from osgeo import gdal, gdalconst, osr, ogr
from pcraster import *
from pcraster.framework import *
import lisGlobals as lg

class InfrastructureMaps(StaticModel):
    def __init__(self):
        StaticModel.__init__(self)
    def initial(self):
        mask = lg.mask_
        sf = lg.shapeNr  # 1 = house, 2 = roads

        if sf == 1 and lg.buildingsSHPName == "" :
            return;
        if sf == 2 and lg.roadsSHPName == "" :
            return;

        ShapeName = ""
        if sf == 1 :
            ShapeName = lg.BaseDir+lg.buildingsSHPName
        if sf == 2 :            
            ShapeName = lg.BaseDir+lg.roadsSHPName
            
        tifname = lg.BaseDir+"tempbuild.tif"
        outnametif = lg.BaseDir+"rescale.tif"

        shape_vector = ogr.Open(ShapeName) 
        shape_layer = shape_vector.GetLayer()
        
        #resolution of temp raster
        x_res = lg.dx/10.0
        if x_res < 1 :
            x_res = 1
        factor = lg.dx/x_res
                
        driver = gdal.GetDriverByName('GTiff')
        dst_ds = driver.Create(tifname,int (lg.nrCols*factor),int(lg.nrRows*factor),1,gdal.GDT_Float32) #GDT_UInt16)
        gt = lg.maskgeotrans
        dst_ds.SetGeoTransform( [ gt[0], x_res, gt[2], gt[3], gt[4], -x_res ] )
        dst_ds.SetProjection(lg.maskproj)
        gdal.RasterizeLayer(dst_ds, [1], shape_layer, None)
        
        dst_ds = None
        shape_vector = None
        shape_layer = None
        
        src = gdal.Open(tifname)
        #cutout and convert
        # dst = gdal.GetDriverByName('PCRaster').Create(outname, lg.nrCols, lg.nrRows, 1,
                                    # gdalconst.GDT_Float32,["PCRASTER_VALUESCALE=VS_SCALAR"])
        #PCRAster directly gives problems sometimes!
        
        dst = gdal.GetDriverByName('GTiff').Create(outnametif, lg.nrCols, lg.nrRows, 1, gdalconst.GDT_Float32)
        dst.SetGeoTransform( lg.maskgeotrans )
        dst.SetProjection( lg.maskproj )
        gdal.ReprojectImage(src, dst, lg.maskproj, lg.maskproj, gdalconst.GRA_Bilinear)
        dst = None
        src = None    
        
        map_ = readmap(outnametif)
        report(map_,"try.map")
        if maptotal(map_) > 0 :
            map_ = map_/mapmaximum(map_)*mask
        else :
            if sf == 1 :
                print("WARNING: resulting building map is empty!, check you shape file");
            if sf == 2 :
                print("WARNING: resulting road map is empty!, check you shape file");
                
        if sf == 1 :
            report(map_,lg.housecovName)
            roofstore = ifthenelse(map_ > 0, scalar(1), 0)*lg.mask_*lg.roofStore
            report(roofstore,lg.roofstoreName)            
        if sf == 2 :    
            map_ = map_ * lg.dx
            report(map_,lg.roadwidthName)

        os.remove(tifname)
        os.remove(outnametif)
        