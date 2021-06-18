from osgeo import gdal, gdalconst, osr
import os
from pcraster import *
from pcraster.framework import *
#import matplotlib.pyplot as plt

#,osr
#from qgis.core import *
#import qgis.utils

os.chdir('C:/data/India/GPM/July2014')

#print(os.listdir(os.getcwd()))

#setclone('C:/CRCLisem/Narmada1/Base/dem0.map')
#setclone('C:/data/India/narmada/maps/dem.map')

# destination boundingbox and projection
maskgdal=gdal.Open('C:/CRCLisem/Narmada1/Base/dem0.map') # get mask details
#maskgdal=gdal.Open('C:/data/India/narmada/maps/dem.map')
maskproj = maskgdal.GetProjection()
nrRows = maskgdal.RasterYSize
nrCols = maskgdal.RasterXSize
masktrans = maskgdal.GetGeoTransform()
dx = maskgdal.GetGeoTransform()[1]
dy = maskgdal.GetGeoTransform()[5]
llx = maskgdal.GetGeoTransform()[0]
ury = maskgdal.GetGeoTransform()[3]
urx = llx + nrCols*dx
lly = ury + dy*nrRows
maskbox = [llx,lly,urx,ury]
print(nrRows,nrCols,dx,dy,maskbox)


ESPG = 32644


outputdir = 'C:/CRCLisem/Narmada1/Rain/gpm/july2014/'

#get all the files in the directory
totallinks = os.listdir(os.getcwd())
hdflinks = []
for link in totallinks:
    if link[-3:] == 'tif':
        hdflinks.append(link)

#for ech link (filename) do
for link in hdflinks:
    if link[-3:] == 'tif':
        print(' => '+link)

        src = gdal.Open(link, gdal.GA_ReadOnly)
        prj1 = osr.SpatialReference()
        prj1.ImportFromEPSG(4326)
        wkt1 = prj1.ExportToWkt()
        src.SetProjection(wkt1)

      #   band_ds = gdal.Open(hdf_ds.GetSubDatasets()[7][0], gdal.GA_ReadOnly)
        #choose the 7th dataset that corresponds to precipitationCal
        #band_array = hdf_ds.ReadAsArray()
        #band_array[band_array<0] = 0 #filter all NaN values that appear as negative values, specially for the tiff representation


    #cutout and convert

        filename = link[:-4]+".map"
        gpmoutName = outputdir+filename
        dst = gdal.GetDriverByName('PCRaster').Create(gpmoutName, nrCols, nrRows, 1,gdalconst.GDT_Float32,["PCRASTER_VALUESCALE=VS_SCALAR"])
        #dst = gdal.GetDriverByName('GTiff').Create(gpmoutName, nrCols, nrRows, 1,gdalconst.GDT_Float32)
        dst.SetGeoTransform( masktrans )
        dst.SetProjection( maskproj )

        prj2 = osr.SpatialReference()
        prj2.ImportFromEPSG(32644)
        wkt2 = prj2.ExportToWkt()
        dst.SetProjection(wkt2)

        gdal.ReprojectImage(src, dst, wkt1, wkt2, gdalconst.GRA_Bilinear) #gdal.GRA_Cubic)


        #gdal.ReprojectImage(src, dst, maskproj, maskproj, gdalconst.GRA_Bilinear)
        # # add the band information
        #dst.GetRasterBand(1).WriteArray(band_array.T[::-1])
        # raster = None

        # geotransform = ([-180,0.1,0,90,0,-0.1])

        # # make a tif file
        # filename = link[:-5]+".tif"
        # raster = gdal.GetDriverByName('GTiff').Create(filename,nrCols,nrRows,1,gdal.GDT_Float32)
        # raster.SetGeoTransform(geotransform)
        # srs=osr.SpatialReference()
        # srs.ImportFromEPSG(4326)
        # sss = srs.ExportToWkt()
        # raster.SetProjection(srs.ExportToWkt())
        # # add the band information
        # raster.GetRasterBand(1).WriteArray(band_array.T[::-1])
        # raster = None
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
        dst = None



raintxtname = outputdir+'GPM-2014-07.txt'
with open(raintxtname, 'w') as f:
    f.write('# GPM data GPM-2014-07')
    f.write(2)
    f.write('time (ddd:mmmm)')
    f.write('filename')

os.chdir('C:/CRCLisem/Narmada1/Rain/gpm/July2014')
totallinks = os.listdir(os.getcwd())
hdflinks = []
for link in totallinks:
    if link[-3:] == 'map':
        print(' => '+link)
        with open(raintxtname, 'w') as f:
            f.write('{0}:{1:04d} {2}'.format(day).format(m).format(filename)

        m += 30
        if (m == 1440):
            day = day + 1
            m = 0


# sum = 0

#         rain = readmap(link)
#         sum=sum+rain

# report(sum,'C:/CRCLisem/Narmada1/Rain/gpm/_sum.map')
#maskgdal = None