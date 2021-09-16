# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 11:52:56 2021

@author: vjett
"""
from osgeo import gdal, gdalconst, osr
import os
from pcraster import *
from pcraster.framework import *
import numpy as np



def hdf_subdataset_extraction(hdf_file, dst_dir, subdataset):
    # open the dataset

    hdf_ds = gdal.Open(hdf_file, gdal.GA_ReadOnly)
    band_ds = gdal.Open(hdf_ds.GetSubDatasets()[subdataset][0], gdal.GA_ReadOnly)

    # read into numpy array
    band_array = band_ds.ReadAsArray().astype(np.int16)

    # convert no_data values
    band_array[band_array == -28672] = 0 #-32768
    band_array[band_array > 30000] = 0 #-32768

    # build output path
    #band_path = os.path.join(dst_dir, os.path.basename(os.path.splitext(hdf_file)[0]) + "-sd" + str(subdataset+1) + ".tif")
    band_path = os.path.join(dst_dir, "MOD" + "-sd" + str(subdataset+1) + ".tif")

    # write raster
    out_ds = gdal.GetDriverByName('GTiff').Create(band_path,
                                                  band_ds.RasterXSize,
                                                  band_ds.RasterYSize,
                                                  1,  #Number of bands
                                                  gdal.GDT_Int16,
                                                  ['COMPRESS=LZW', 'TILED=YES'])
    out_ds.SetGeoTransform(band_ds.GetGeoTransform())
    out_ds.SetProjection(band_ds.GetProjection())
    out_ds.GetRasterBand(1).WriteArray(band_array)
    out_ds.GetRasterBand(1).SetNoDataValue(-32768)

    out_ds = None  #close dataset to write to disc



hdf_file = 'C:/CRCLisem/MODIS Data-July/ET-July/2014/MOD16A2.A2014209.h24v06.006.2017075055726.hdf'
dst_dir = 'C:/CRCLisem/MODIS Data-July/ET-July/'


os.chdir(inputdir)
totallinks = os.listdir(os.getcwd())
print("nr files to be processed: ", len(totallinks))
hdflinks = []
for link in totallinks:
    if link[-3:] == 'hdf':
        hdflinks.append(link)


# covert date into ddd:mmmm and add to stringlist
print("find Julian day numbers and minutes")
dddmmmm = []
#for each link (filename) do
for link in hdflinks:
    if link[-3:] == 'tif':
        print(' => '+link)

        # find julian day number
        daystr =  link[23:]
        daystr = daystr[:8]
        day_of_year = time.strptime(daystr, "%Y%m%d").tm_yday
        minstr = link[-19:]
        minstr = minstr[:4]
        print(daystr, day_of_year,minstr)
        dddmmmm.append("{0}:{1}".format(str(day_of_year),minstr))



#for each link (filename) do
for link in hdflinks:
    hdf_subdataset_extraction(link, outputdir, 2)

# make raintext file and convert files division by 10
print("making lisem ET txt file")
os.chdir(outputdir)
ETtxtname = ETfilename
with open(ETtxtname, 'w') as f:
    f.write('# MODIS ET data \n')
    f.write('2\n')
    f.write('time (ddd:mmmm)\n')
    f.write('filename\n')
    f.close()

# read all maps in folder

nr = 0
totallinks = os.listdir(os.getcwd())
hdflinks = []
for link in totallinks:
    if link[-9:] == '30min.map':
        print(' => '+link)
        with open(raintxtname, 'a') as f:
            f.write('{0}  {1}\n'.format(dddmmmm[nr],link))
        nr+=1

        rain = readmap(link)
        if (option > -1) :
            rain = max(0,rain/10.0)
        report(rain,link)
        sum=sum+rain

f.close()