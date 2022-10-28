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
            
        #shpname = lg.BaseDir+"gebouw_top10nl.shp"
        #outname = lg.BaseDir+"housecover.map"
        
        shpname = lg.ShapeName
        outname = lg.ShapetoMapName
        tifname = lg.BaseDir+"tempbuild.tif"
        sf = lg.sizeFactor
        
        shape_vector = ogr.Open(shpname) #lg.shpName)
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
        dst = gdal.GetDriverByName('PCRaster').Create(outname, lg.nrCols, lg.nrRows, 1,
                                    gdalconst.GDT_Float32,["PCRASTER_VALUESCALE=VS_SCALAR"])
        dst.SetGeoTransform( lg.maskgeotrans )
        dst.SetProjection( lg.maskproj )
        gdal.ReprojectImage(src, dst, lg.maskproj, lg.maskproj, gdalconst.GRA_Bilinear)
        dst = None
        src = None    
        
        map_ = readmap(outname)
        map_ = map_/mapmaximum(map_)*sf*mask
        report(map_,outname)
        
        