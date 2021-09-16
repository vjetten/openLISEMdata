from osgeo import gdal, gdalconst, osr
import os
from pcraster import *
from pcraster.framework import *


inputdir =  'C:\data\India\GPM\July2014'
# folder with GPM global tiff
outputdir =  'C:/data/India/narmada/rainfall/gpm/july2014/'
# output for lisem
maskmapname = 'C:/data/India/narmada/maps/dem.map'
#'C:/CRCLisem/Narmada1/Base/dem0.map'

setclone(maskmapname)

# destination boundingbox and projection
maskgdal=gdal.Open(maskmapname)
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

option = 1


# get all the files in the directory
os.chdir(inputdir)
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

        filename = link[:-4]+".map"
        gpmoutName = outputdir+filename
        dst = gdal.GetDriverByName('PCRaster').Create(gpmoutName, nrCols, nrRows, 1,gdalconst.GDT_Float32,["PCRASTER_VALUESCALE=VS_SCALAR"])
        #dst = gdal.GetDriverByName('GTiff').Create(gpmoutName, nrCols, nrRows, 1,gdalconst.GDT_Float32)
        dst.SetGeoTransform( masktrans )
        dst.SetProjection( maskproj )

        prj2 = osr.SpatialReference()
        prj2.ImportFromEPSG(ESPG)
        wkt2 = prj2.ExportToWkt()
        dst.SetProjection(wkt2)

        GDO = gdalconst.GRA_Bilinear
        if (option == 2):
            GDO = gdalconst.GRA_Cubic

        gdal.ReprojectImage(src, dst, wkt1, wkt2, GDO) #gdalconst.GRA_Bilinear) #gdal.GRA_Cubic)

        # #del dst # Flush
        dst = None


# make raintext file

print("making lisem rainfall txt file")

raintxtname = outputdir+'GPM-2014-07.txt'
with open(raintxtname, 'w') as f:
    f.write('# GPM data GPM-2014-07\n')
    f.write('2\n')
    f.write('time (ddd:mmmm)\n')
    f.write('filename\n')
    f.close()
day = 182
m = 0

os.chdir(outputdir)
totallinks = os.listdir(os.getcwd())
hdflinks = []
for link in totallinks:
    if link[-9:] == '30min.map':
        print(' => '+link)
        with open(raintxtname, 'a') as f:
            f.write('{0}:{1:0>4} {2}\n'.format(day,m,link))

            m = m + 30
            if (m == 1440):
                day = day + 1
                m = 0
f.close()

#calculate total and divide by 10 => gpm 30min has a factor 9.1 for mm/h

for link in totallinks:
    if link[-3:] == 'map':
        print(' => '+link)

        rain = readmap(link)
        rain = rain/10.0
        report(rain,link)
        sum=sum+rain

report(sum,outputdir+'_sum.map')