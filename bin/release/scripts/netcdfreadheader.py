from osgeo import gdal
import netCDF4 as nc
from netCDF4 import num2date
import numpy as np
import sys
import random

def update_progress(progress):
    barLength = 50 # Modify this to change the length of the progress bar
    if progress >= 0.99:
        progress = 1
    block = int((barLength*progress))
    text = "\r  Processing: [{0}] {1:.2f}% ".format( '#'*block + '-'*(barLength-block), (progress)*100)
    sys.stdout.write(text)
    sys.stdout.flush()    
    
print('>>> Analyzing mask ...',flush = True)

rainfilename = 'raingauge2014hr.txt'
maskname = 'c:/data/Limburg/Strabeek/base/gebouw5m.tif'
inputfile = 'c:/data/Limburg/Strabeek/rain/KNMI_IRC_FINAL.nc'

day0 = 190
dayn = 200
dailyA = 2.0
dailyB = -0.56
starthour = 600


maskgdal = gdal.Open(maskname)
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

print(nrCols,nrRows,maskbox)


# Open netCDF4 file
f = nc.Dataset(inputfile)
#print(f)
print(f.__dict__)

# Find the attributes
Data = f.variables['rainfall_rate']
#print('v ',Data.get_dims())

for dim in f.dimensions.values():
    print(dim)

 
# Get dimensions
##time_dim,  lat_dim, lon_dim = Data.get_dims()
##time_var = f.variables[time_dim.name]
##times = num2date(time_var[:], time_var.units)
##latitudes = f.variables[lat_dim.name][:]
##longitudes = f.variables[lon_dim.name][:]
##
##Getdimensions = np.shape(Data)
##Time = Getdimensions[0]
##Latdim  = Getdimensions[1]
##Longdim = Getdimensions[2]
