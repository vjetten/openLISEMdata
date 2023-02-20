# lisemDBASEgenerator
# global vraiables and initialisation
#
# author: V.G.Jetten @ 2022
# University of Twente, Faculty ITC
# this software has copyright model: GPLV3
# this software has a disclaimer



from osgeo import gdal, gdalconst, osr
import os, glob
from os import listdir
from pcraster import *
from pcraster.framework import *
import time
import lisGlobals as lg

# use unix style path delimiters: / instead of \
# pathnames end with /

# update_progress() : Displays or updates a console progress bar
def update_progress(progress):
    barLength = 50 # Modify this to change the length of the progress bar
    if progress >= 0.99:
        progress = 1
    block = int(round(barLength*progress))
    text = "\rProcessing: [{0}] {1:.3g}% ".format( "#"*block + "-"*(barLength-block), progress*100)
    sys.stdout.write(text)
    sys.stdout.flush() 


class GPMRainfall(StaticModel):
    def __init__(self):
        StaticModel.__init__(self)
    def initial(self):
    # faster to copy global vars
        mask = lg.mask_
        rainOutputdir = lg.rainOutputdir
        rainfilename = lg.rainfilename 
        #conversionmmh = lg.conversionmmh
        #timeinterval  = lg.timeinterval
        
        if not os.path.exists(rainOutputdir):
            print('>>> Creating output dir: '+rainOutputdir, flush=True)
            os.makedirs(rainOutputdir)
            # if you don't do this you get an error later

        # 0 =  nearest neighbour, 1 = bilinear interpolation while resampling, 2 =  cubic interpolation
        # if option = -1 the lisem rainfall textfile is regenerated and the conversion is skipped

        # set clone for pcraster operations
        setclone(lg.rainMaskmapname)

        # resample options
        if (lg.IPoption == 0):
            GDO = gdalconst.GRA_NearestNeighbour
            print('>>> Using Nearest Neighbour Interpolation', flush=True)
        if (lg.IPoption == 1):
            GDO = gdalconst.GRA_Bilinear
            print('>>> Using Bilinear Interpolation', flush=True)
        if (lg.IPoption == 2):
            GDO = gdalconst.GRA_Cubic
            print('>>> Using Cubic Interpolation', flush=True)


        print('>>> Deleting previous rainfall maps in folder: {0} '.format(rainOutputdir), flush=True)
        # for root, dirs, files in os.walk(rainOutputdir):
            # for file in files:
                # os.remove(os.path.join(root, file))
        for file_name in listdir(rainOutputdir):
            if lg.rainString in file_name :
                #print(rainOutputdir + '/' + file_name,flush=True)
                os.remove(rainOutputdir + '/' + file_name)

        print('>>> Converting GTiff to PCRaster ', flush=True)

        # get all the TIF files in the directory and put the names in hfdlinks
        os.chdir(lg.rainInputdir)
        totallinks = os.listdir(os.getcwd())
        hdflinks = []
        for link in totallinks:
            if link[-3:] == 'tif':
                hdflinks.append(link)
                
        totalcount = len(hdflinks)
        count = 0
        print(">>> nr GTiff files to be processed: {0}".format(totalcount),flush = True)

        start = 0
        update_progress(0)
        if (lg.IPoption > -1) :
            #for each link (filename) do
            for link in hdflinks:
                if link[-3:] == 'tif':
                    #print(' => '+link, flush=True)
                    src = gdal.Open(link, gdal.GA_ReadOnly)
                    if start == 0 :
                        prj1 = osr.SpatialReference()
                        prj1.ImportFromEPSG(int(lg.rainEPSG))
                        #print(prj1, flush = True)

                        wkt1 = prj1.ExportToWkt()
                        
                    src.SetProjection(wkt1)

                    filename = link[:-4]+".map"
                    gpmoutName = rainOutputdir+filename
                    dst = gdal.GetDriverByName('PCRaster').Create(gpmoutName, lg.nrCols, lg.nrRows, 1,gdalconst.GDT_Float32,["PCRASTER_VALUESCALE=VS_SCALAR"])
                    dst.SetGeoTransform( lg.maskgeotrans )
                    dst.SetProjection( lg.maskproj )

                    if start == 0 :
                        prj2 = osr.SpatialReference()
                        prj2.ImportFromEPSG(int(lg.ESPG))
                        wkt2 = prj2.ExportToWkt()
                        start = 1
                    dst.SetProjection(wkt2)

                    gdal.ReprojectImage(src, dst, wkt1, wkt2, GDO)
                    
                    count += 1            
                    update_progress(count/(totalcount))


                    dst = None
                    src = None
        update_progress(1)   
        
        print("\nreprojection done.",flush = True)        

        # covert date into ddd:mmmm and add to stringlist dddmmmm
        print(">>> Find Julian day numbers and minutes")

        dddmmmm = []  # array of strings with format ddd:mmmm
        i = 0
        for link in hdflinks:
            if link[-3:] == 'tif':
                #print(' => '+link, flush=True)

                # find julian day number
                daystr =  link[23:]
                daystr = daystr[:8]
                day_of_year = time.strptime(daystr, "%Y%m%d").tm_yday
                minstr = link[-19:]
                minstr = minstr[:4]
                
                #print(daystr, day_of_year,minstr, flush=True)
                dddmmmm.append("{0}:{1}".format(str(day_of_year),minstr))
                #print(dddmmmm[i],flush= True)
                i+=1
                

        # make raintext file and convert files division by 10
        print(">>> Making lisem rainfall txt file", flush=True)
        print(">>> and calculating sum of all rainfall in sumrainfall.map\n", flush=True)

        os.chdir(rainOutputdir)
        with open(lg.rainfilename, 'w') as f:
            f.write('# GPM data \n')
            f.write('2\n')
            f.write('time (ddd:mmmm)\n')
            f.write('GPM filename\n')
            f.close()

        # read all maps in folder
        DEM = readmap(lg.BaseDir + lg.rainMaskmapname)
        mask = (DEM*0) + scalar(1)
        sum = 0 * mask
        j = 0
        sumr = 0
        update_progress(0)
        totallinks = os.listdir(os.getcwd())
        totalnr = totalcount
        for link in totallinks:
            if link[-9:] == '30min.map':
                #print(' => '+link)
                #print(j)
                # write the times and filenames in the lisem input file
                with open(rainfilename, 'a') as f:
                    f.write('{0}  {1}\n'.format(dddmmmm[j],link))

                # calculate the total rainfall
                raina = readmap(link)
                #if (option > -1) :
                rain = max(0,(60/lg.timeinterval)*raina*lg.conversionmmh)

                report(rain,link)
                sum=sum+rain/(60/lg.timeinterval)    # assumning the value is intensity in mm/h the rainfall is p/(60/interval)
                update_progress(j/totalnr)
                j+=1

        f.close()
        report(sum,rainOutputdir+'sumrainfall.map')

        if lg.optionGaugeGPM == 1:

            print(">>> Making rainfall point file \n")

            rowpoint = []
            colpoint = []
            valpoint = []
            # read pcraster map with single point = 1
            pointmap = readmap(lg.rainPointmapname) #BaseDir+pointmapname)
          
            pm = pcr2numpy(pointmap, -9999)

            i = 0
            for row in range(1,lg.nrRows) :
                for col in range(1,lg.nrCols) :
                    value = int(pm[row][col])
                    if (value > 0) :
                        rowpoint.append(row)
                        colpoint.append(col)
                        valpoint.append(value)
            pointlen = len(valpoint)
                    
            if len(rowpoint) == 0 :
                print('no point found in file {0}'.format(lg.rainPointmapname), flush = True)
                exit()
            else :
                for i in range(pointlen) :
                    print('point(s) found in file {0}: {1} {2} - {3}'.format(lg.rainPointmapname,rowpoint[i],colpoint[i],valpoint[i]), flush = True)

            nr = 0
            raintxtname = []
            sumvalue = []
            
            update_progress(0)
            
            for i in range(pointlen) :
                number = "p{0}_".format(valpoint[i])
                raintxtname.append(rainOutputdir + number + lg.rainPointnameIn)
                print(raintxtname[i],flush=True)
                with open(raintxtname[i], 'w') as f:
                    f.write("# GPM point data for point{0}\n".format(valpoint[i]))
                    f.write('2\n')
                    f.write('time (ddd:mmmm)\n')
                    f.write('Intensity (mm/h)\n')
                    f.close()
                sumvalue.append(0)
            print
                
            totallinks = os.listdir(os.getcwd())
            hdflinks = []
            totalnr = totalcount
            for link in totallinks:
                if link[-9:] == '30min.map':
                    #print(' => '+link)
                    raina = readmap(link)
                    rm = pcr2numpy(raina, -9999)

                    for i in range(pointlen) :
                        value = rm[rowpoint[i]][colpoint[i]]
                        sumvalue[i] = sumvalue[i] + value
                        with open(raintxtname[i], 'a') as f:        
                             f.write('{0}  {1}\n'.format(dddmmmm[nr],value))

                    update_progress(nr/totalnr)                 
                    nr+=1
            update_progress(1)   
                    
            #f.close()  # with "with open" you don't need to close!
                    
            for i in range(pointlen) :            
                sumvalue[i] /= 2.0  # from intensity to amount
                print("\nTotal rainfall for point {0}: {1} mm".format(valpoint[i],sumvalue[i]), flush=True)

        print(">>> Done.", flush=True)
