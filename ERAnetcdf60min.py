from osgeo import gdal
import netCDF4
from netCDF4 import num2date
import numpy as np
import sys
import random



def update_progress(progress):
    barLength = 50 # Modify this to change the length of the progress bar
    if progress >= 0.99:
        progress = 1
    block = int((barLength*progress))
    text = "\rProcessing: [{0}] {1:.2f}% ".format( '#'*block + '-'*(barLength-block), (progress)*100)
    sys.stdout.write(text)
    sys.stdout.flush()    
    
print(">>> Reading interface options",flush=True)

#read init file in test array myvars
myvars = {}
with open(sys.argv[1], 'r') as myfile:
    for line in myfile:
        if '=' not in line:
            continue
        S0 = (line.split('='))[0].strip()
        S1 = (line.split('='))[1].strip()
        myvars[S0] = S1

rainfilename = 'raingauge2014hr.txt'
maskname = 'try.tif' #'mohgaon_latlon.tif'
RainDailyFilename = 'imd_2014.nc'
#masknamem = 'dem500m.tif'
day0 = 152
dayn = 273
dailyA = 0.14
dailyB = -0.374
dt30min = 30

BaseDir = myvars["BaseDirectory"]
#inputdir = myvars["RainBaseDirectory"]
outputdir = myvars["RainDirectory"]
maskmapname  = myvars["RainRefNameDEM"]
ERAFilename = myvars["ERAFilename"]
rainfilename = myvars["RainFilenameHourERA"]
# ESPG = myvars["ESPGnumber"]    
dailyA= float(myvars["dailyA"])
dailyB= float(myvars["dailyB"])
day0= int(myvars["day0"])
dayn= int(myvars["dayn"])
dt30min= int(myvars["30min"])

      
print('>>> Analyzing mask ...',flush = True)

# warp pcraster to tif with lat lon 
maskmapname = BaseDir+maskmapname
maskname = BaseDir+maskname
rainfilename=outputdir+rainfilename

#print(maskmapname,maskname,rainfilename)


#gdalwarp trydem.tif hoi.tif -t_srs EPSG:4326 -tr 0.25 0.25
#goptions = gdal.WarpOptions(dstSRS="+proj=longlat +datum=WGS84 +no_defs",xRes="0.25", yRes="0.25")
goptions = gdal.WarpOptions(srcSRS="EPSG:32644",dstSRS="EPSG:4326")#,xRes="0.25", yRes="0.25")
gdal.Warp(maskname, maskmapname, options=goptions) #srcSRS="EPSG:32644", dstSRS="EPSG:4326")

maskgdal = gdal.Open(maskname)
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
print("rows,cols,box:",nrRows,nrCols,lly,llx,ury,urx)
del maskgdal

# Open netCDF4 file
f = netCDF4.Dataset(ERAFilename)

print (f.variables.keys())
print (f.data_model)

# Find the attributes
Data = f.variables['tp']
print(Data.get_dims())
 
# Get dimensions
time_dim,  lat_dim, lon_dim = Data.get_dims()
#time_var = f.variables[time_dim.name]
#times = num2date(time_var[:], time_var.units)
latitudes = f.variables[lat_dim.name][:]
longitudes = f.variables[lon_dim.name][:]


Getdimensions = np.shape(Data)
Time = Getdimensions[0]
Latdim  = Getdimensions[1]
Longdim = Getdimensions[2]
print(Time,Latdim,Longdim)

print('  - Latitudes in mask:', end = ' ',flush = True)
startlat = -999
doit = False
for i in range(0,Latdim):
    if latitudes[i] >= lly and latitudes[i] <= ury:
        if startlat == -999 :
            startlat = i-1
        print(latitudes[i], end = ' ')
        
print('\n  - longitudes in mask:', end = ' ',flush = True)
startlon = -999
doit = False
for j in range(0,Longdim):
    if longitudes[j] >= llx and longitudes[j] <= urx:
        if startlon == -999 :
            startlon = j-1
        print(longitudes[j], end = ' ')


nrstations = 0
rows = 0
for i in range(0,Latdim):
    if latitudes[i] > lly and latitudes[i] < ury:
        rows += 1
        cols = 0
        for j in range(0,Longdim):
            if longitudes[j] > llx and longitudes[j] < urx:
                cols += 1
                nrstations += 1

print('\n  - Gridcells in mask: ',nrstations,flush = True)
#print(startlat,startlon,rows,cols,nrstations)
print(longitudes[startlon+1],llx,latitudes[startlat+1],lly)

# calculate row and col number of IMD center grideclls
drows = round((longitudes[startlon+1]-longitudes[startlon])/dx)
startrow = round((longitudes[startlon+1]-llx)/dx)

dcols = round((latitudes[startlat+1]-latitudes[startlat])/dx)
startcol = round((latitudes[startlat+1]-lly)/dx)

print(drows,startrow,dcols,startcol,(longitudes[1]-longitudes[0]),dx)

print(">>> Making openLISEM rainfall input file: ", rainfilename, flush=True)


with open(rainfilename, 'w') as f:
    
    # write the header with pixel coord of stations
    f.write('# hourly data from {0} in {3} with paramaters {1},{2}\n'.format(RainDailyFilename,dailyA,dailyB,maskname))
    f.write("{0}\n".format(nrstations+1))
    f.write('time (ddd:mmmm)\n')
    for i in range(1,nrstations+1):   
        j = int((i-1)/cols)
        k = (i-1) % cols 
        f.write("{0} {1:6} {2:6}\n".format(i,startrow+j*drows,startcol+k*dcols))

    # for all days   
    sumdays = [0 for x in range(nrstations)]
    
    endtime = Time #(dayn-day0)*24
    day = day0
    min = 0
    #print(endtime)
    
    P = [0 for x in range(nrstations)]
    for t in range(0,endtime) : 
        

        nrst = 0
        #get the hourly rainfall for all gridcellsand fill the P station array               
        for i in range(0,Latdim):
            if latitudes[i] > lly and latitudes[i] < ury:
                #for j in range(0,Longdim):
                for j in range(Longdim-1,0,-1):
                    if longitudes[j] > llx and longitudes[j] < urx:
                        # missng values are set to ZERO!!!
                        r = 0
                        if Data[t,i,j] > 0:
                            r = Data[t,i,j]
                        P[nrst] = r*1000
       # print(P, flush = True)                        
                        
        #write hourly rainfall
        f.write("{0}:{1:04d}".format(day,min)) 
        for k in range(0,nrstations) :              
            f.write(" {0:6.2f}".format(P[k]))
        f.write("\n") 
        nrst += 1
        min = min + 60
        if (min >= 1440):
            min = 0
            day += 1            
            
             
        update_progress(t/endtime)
        
        for k in range(0,nrstations) :  
            sumdays[k] = sumdays[k] + P[k]
            

    # end the file with 0    
    f.write("{0}:{1:04d}".format(dayn+1,1340)) 
    for k in range(0,nrstations) :              
        f.write(" {0:6.2f}".format(0))                 
    f.write("\n")                        

    f.close()    
    
    print('\n\nGridcell totals:\n',sumdays, '\n')   
               
print('\n>>> done\n',flush = True)
