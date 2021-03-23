from osgeo import gdal, gdalconst, osr
import os

#,osr
#from qgis.core import *
#import qgis.utils

os.chdir('C:/data/india/imerg/')

#print(os.listdir(os.getcwd()))


# Source

maskgdal=gdal.Open('C:/data/India/Cauvery/Base/maskbasin.map') # get mask details
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

totallinks = os.listdir(os.getcwd())
hdflinks = []
for link in totallinks:
    if link[-4:] == 'HDF5':
        hdflinks.append(link)

for link in hdflinks:
    if link[-4:] == 'HDF5':
        print(' => '+link)

        hdf_ds = gdal.Open(link, gdal.GA_ReadOnly)
        band_ds = gdal.Open(hdf_ds.GetSubDatasets()[7][0], gdal.GA_ReadOnly)
        #choose the 7th dataset that corresponds to precipitationCal
        band_array = band_ds.ReadAsArray()
        band_array[band_array<0] = 0 #filter all NaN values that appear as negative values, specially for the tiff representation

        geotransform = ([-180,0.1,0,90,0,-0.1])

        # make a tif file
        filename = link[:-5]+".tif"
        raster = gdal.GetDriverByName('GTiff').Create(filename,nrCols,nrRows,1,gdal.GDT_Float32)
        raster.SetGeoTransform(geotransform)
        srs=osr.SpatialReference()
        srs.ImportFromEPSG(4326)
        sss = srs.ExportToWkt()
        raster.SetProjection(srs.ExportToWkt())
        # add the band information
        raster.GetRasterBand(1).WriteArray(band_array.T[::-1])
        raster = None
        #close it

        # # Source
        # src_filename = filename
        # #  src = gdal.Open(src_filename, gdalconst.GA_ReadOnly)
        # src_proj = band_ds.GetProjection()
        # #srs.ExportToWkt()  #raster.GetProjection()
        # #src_geotrans = geotransform #raster.GetGeoTransform()

        # # Output / destination
        # dst_filename = filename
        # dst = gdal.GetDriverByName('GTiff').Create(dst_filename, nrCols, nrRows, 1, gdalconst.GDT_Float32)
        # dst.SetGeoTransform( match_geotrans )
        # dst.SetProjection( maskproj)

        # # Do the work
        # gdal.ReprojectImage(raster, dst, sss, maskproj, gdalconst.GRA_NearestNeighbour) #gdalconst.GRA_Bilinear)

        # #del dst # Flush
        hdf_ds = None
        band_ds = None

maskgdal = None