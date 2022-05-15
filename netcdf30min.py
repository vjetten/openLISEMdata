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

BaseDir = myvars["BaseDirectory"]
#inputdir = myvars["RainBaseDirectory"]
outputdir = myvars["RainDirectory"]
maskmapname  = myvars["RainRefName"]
RainDailyFilename = myvars["RainDailyFilename"]
rainfilename = myvars["RainFilenameHour"]
# ESPG = myvars["ESPGnumber"]    
dailyA= float(myvars["dailyA"])
dailyB= float(myvars["dailyB"])
day0= int(myvars["day0"])
dayn= int(myvars["dayn"])

      
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
#print(nrCols,nrRows,maskbox)
del maskgdal

# Open netCDF4 file
f = netCDF4.Dataset(RainDailyFilename)

# Find the attributes
Data = f.variables['RAINFALL']
#print(Data.get_dims())
 
# Get dimensions
time_dim,  lat_dim, lon_dim = Data.get_dims()
time_var = f.variables[time_dim.name]
times = num2date(time_var[:], time_var.units)
latitudes = f.variables[lat_dim.name][:]
longitudes = f.variables[lon_dim.name][:]

Getdimensions = np.shape(Data)
Time = Getdimensions[0]
Latdim  = Getdimensions[1]
Longdim = Getdimensions[2]

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
        for j in range(0,Longdim):
            if longitudes[j] > llx and longitudes[j] < urx:
                nrstations += 1
cols = int(nrstations/rows)
print('\n  - Gridcells in mask: ',nrstations,flush = True)
#print(startlat,startlon,rows,cols,nrstations)

# calculate row and col number of IMD center grideclls
drows = int((longitudes[1]-longitudes[0])/dx+0.5)
startrow = int(0.5*(longitudes[startlon+1]-llx)/dx+0.5)
dcols = int((latitudes[1]-latitudes[0])/dx+0.5)
startcol = int(0.5*(latitudes[startlat+1]-lly)/dx+0.5)
#print(drows,startrow,dcols,startcol,(longitudes[1]-longitudes[0]),dx)

print(">>> Making openLISEM rainfall input file: ", rainfilename, flush=True)

dt=30
nnn = int(12*60/dt)

with open(rainfilename, 'w') as f:
    
    # write the header with pixel coord of stations
    f.write('# 1/2 hourly data from {0} in {3} with paramaters {1},{2}\n'.format(RainDailyFilename,dailyA,dailyB,maskname))
    f.write("{0}\n".format(nrstations+1))
    f.write('time (ddd:mmmm)\n')
    for i in range(1,nrstations+1):   
        j = int((i-1)/cols)+1
        k = (i-1) % cols + 1
        f.write("{0} {1:6} {2:6}\n".format(i,startrow+j*drows,startcol+k*dcols))

    # first line with 0 rainfall
    f.write("{0}:{1:04d}".format(day0-1,0)) 
    for k in range(0,nrstations) :              
        f.write(" {0:6.2f}".format(0))                 
    f.write("\n")                        

    # for all days   
    sumdays = [0 for x in range(nrstations)]
    sumTdays = [0 for x in range(nrstations)]
    for t in range(day0,dayn+1) :    
        starthour = 240 + random.randint(-1,5)*dt
        #print(starthour)
        P = [0 for x in range(nrstations)]
        step = 0

        #get the daily rainfall for all gridcells               
        for i in range(0,Latdim):
            if latitudes[i] > lly and latitudes[i] < ury:
                for j in range(0,Longdim):
                    if longitudes[j] > llx and longitudes[j] < urx:
                        # missng values are set to ZERO!!!
                        r = 0
                        if Data[t,i,j] > 0:
                            r = Data[t,i,j]
                        P[step] = r
                        step += 1

        # create hourly rainfall        
        rhour = [[0 for x in range(nnn)] for y in range(nrstations)]
        # open the day with 0
        f.write("{0}:{1:04d}".format(t,starthour)) 
        for k in range(0,nrstations) :              
            f.write(" {0:6.2f}".format(0))
        f.write("\n") 
        
        # do the magic for each hour           
       
        # for th in range(0,11) :
        #    f.write("{0}:{1:04d}".format(t,starthour+60+th*60)) 
        #    for k in range(0,nrstations) :  
        #         rhour[k][th] = P[k]/12.0*dailyA*pow(th+0.5,dailyB)
        #         f.write(" {0:6.2f}".format(rhour[k][th])) 
        #    f.write("\n")
        sum = [0 for x in range(nrstations)]
        for th in range(0,nnn) :
           for k in range(0,nrstations) :  
                rhour[k][th] = P[k]*dailyA*pow(th+0.5,dailyB)
                sum[k] = sum[k] + rhour[k][th]
                
        for th in range(0,nnn) :
           for k in range(0,nrstations) :  
               if sum[k] > 0 :
                   rhour[k][th] = rhour[k][th] * P[k]/sum[k] 
                   
        # for k in range(0,nrstations) :                
        #        if sum[k] > 0 :
        #            print(P[k]/sum[k])

        # swap the first two, alternating block method
        # f.write("{0}:{1:04d}".format(t,starthour+60+0*60)) 
        # for k in range(0,nrstations) :  
        #     f.write(" {0:6.2f}".format(rhour[k][1])) 
        # f.write("\n")

        # f.write("{0}:{1:04d}".format(t,starthour+60+1*60)) 
        # for k in range(0,nrstations) :  
        #     f.write(" {0:6.2f}".format(rhour[k][0])) 
        # f.write("\n")

        for th in range(0,nnn) :
            f.write("{0}:{1:04d}".format(t,starthour+dt+th*dt)) 
            for k in range(0,nrstations) :  
                f.write(" {0:6.2f}".format(rhour[k][th]*60/dt)) 
            f.write("\n")
        
        # close the day with 0
        f.write("{0}:{1:04d}".format(t,starthour+(nnn+1)*dt)) 
        for k in range(0,nrstations) :              
            f.write(" {0:6.2f}".format(0))                 
        f.write("\n")  
             
        update_progress(t/dayn)
        
        for k in range(0,nrstations) :  
            sumdays[k] = sumdays[k] + P[k]
            for th in range(0,12) :
                sumTdays[k] = sumdays[k] + rhour[k][th]
            

    # end the file with 0    
    f.write("{0}:{1:04d}".format(dayn+1,1340)) 
    for k in range(0,nrstations) :              
        f.write(" {0:6.2f}".format(0))                 
    f.write("\n")                        

    f.close()    
    
    print('\n\nGridcell totals:\n',sumdays, '\n')   
    print(sumTdays)
               
print('\n>>> done\n',flush = True)
