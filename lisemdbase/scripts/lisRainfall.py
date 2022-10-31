##############################################################################
# CWC project script for GPM IMERG to PCRaster rainfall conversion
#
# - read all global IMERG GPM GTiff files in a directory (espg 4326)
# - read a reference PCRaster map for the target area bounding box and dx
# - provide ESPG target projection
# - give input and output folders have to be given
# - choose interpolation option
# - a text file is produced for openLISEM that is the list for all rainfall
#   maps with their time intervals
# - a map with total rainfall is produced for reference
# NOTE: ALL MAPS ARE DIVIDED BY 10 because GPM is stored in 0.1mm/h
#
#                                               auhtor: V.Jetten 20220620
##############################################################################


from osgeo import gdal, gdalconst, osr
import os, glob
from os import listdir
from pcraster import *
from pcraster.framework import *
import time
import lisGlobals as lg

# use unix style path delimiters: / instead of \
# pathnames end with /

def update_progress(progress):
    barLength = 50 
    if progress >= 0.99:
        progress = 1
    block = int((barLength*progress))
    text = "\rProcessing: [{0}] {1:.2f}% ".format( '#'*block + '-'*(barLength-block), (progress)*100)
    sys.stdout.write(text)
    sys.stdout.flush()    

class GPMRainfall(StaticModel):
    def __init__(self):
        StaticModel.__init__(self)
    def initial(self):
        mask = lg.mask_
        ESPG = lg.ESPG
        
        #rainMaskmapname = lg.BaseDir+lg.rainMaskmapname
        
        if not os.path.exists(lg.rainOutputdir):
            print('>>> Creating output dir: '+lg.rainOutputdir, flush=True)
            os.makedirs(lg.rainOutputdir)
            # if you don't do this you get an error later

        # 0 =  nearest neighbour, 1 = bilinear interpolation while resampling, 2 =  cubic interpolation
        # if option = -1 the lisem rainfall textfile is regenerated and the conversion is skipped

        # set clone for pcraster operations
        setclone(lg.rainMaskmapname)

        # destination boundingbox
        # maskgdal = gdal.Open(rainMaskmapname)
        # maskproj = maskgdal.GetProjection()
        # nrRows = maskgdal.RasterYSize
        # nrCols = maskgdal.RasterXSize
        # masktrans = maskgdal.GetGeoTransform()
        # dx = maskgdal.GetGeoTransform()[1]
        # dy = maskgdal.GetGeoTransform()[5]
        # llx = maskgdal.GetGeoTransform()[0]
        # ury = maskgdal.GetGeoTransform()[3]
        # urx = llx + nrCols*dx
        # lly = ury + dy*nrRows
        # maskbox = [llx,lly,urx,ury]
        # print("rows,cols,dx: ",nrRows,nrCols,dx)
        # print("Bounding box: ",maskbox)

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


        print('>>> Deleting previous GPM files in folder: {0} '.format(outputdir), flush=True)
        # for root, dirs, files in os.walk(outputdir):
            # for file in files:
                # os.remove(os.path.join(root, file))
        for file_name in listdir(lg.rainOutputdir):
            if "3B-HHR-L.MS.MRG.3IMERG" in file_name :
                #print(outputdir + '/' + file_name,flush=True)
                os.remove(lg.rainOutputdir + '/' + file_name)

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
                        prj1.ImportFromEPSG(4326)
                        wkt1 = prj1.ExportToWkt()
                        
                    src.SetProjection(wkt1)

                    filename = link[:-4]+".map"
                    gpmoutName = lg.rainOutputdir+filename
                    dst = gdal.GetDriverByName('PCRaster').Create(gpmoutName, lg.nrCols, lg.nrRows, 1,gdalconst.GDT_Float32,["PCRASTER_VALUESCALE=VS_SCALAR"])
                    dst.SetGeoTransform( lg.masktrans )
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

                    #del dst, Flush
                    dst = None

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

        os.chdir(outputdir)
        raintxtname = rainfilename
        with open(raintxtname, 'w') as f:
            f.write('# GPM data \n')
            f.write('2\n')
            f.write('time (ddd:mmmm)\n')
            f.write('filename\n')
            f.close()

        # read all maps in folder
        DEM = readmap(maskmapname)
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
                with open(raintxtname, 'a') as f:
                    f.write('{0}  {1}\n'.format(dddmmmm[j],link))

                # calculate the total rainfall
                raina = readmap(link)
                #if (option > -1) :
                rain = max(0,(60/timeinterval)*raina/conversionmm)   # data is stored in factor 10, 4.0 means 0.4 mm/h)

                report(rain,link)
                sum=sum+rain/(60/timeinterval)    # assumning the value is intensity in mm/h the rianfall is p/2
                update_progress(j/totalnr)
                j+=1

        f.close()
        report(sum,outputdir+'sumrainfall.map')

        if optionGaugeGPM == 1:

            print(">>> Making rainfall point file \n")

            rowpoint = []
            colpoint = []
            valpoint = []
            # read pcraster map with single point = 1
            pointmap = readmap(BaseDir+pointmapname)
            pm = pcr2numpy(pointmap, -9999)

            i = 0
            for row in range(1,nrRows) :
                for col in range(1,nrCols) :
                    value = int(pm[row][col])
                    if (value > 0) :
                        rowpoint.append(row)
                        colpoint.append(col)
                        valpoint.append(value)
            pointlen = len(valpoint)
                    
            if len(rowpoint) == 0 :
                print('no point found in file {0}'.format(pointmapname), flush = True)
                exit()
            else :
                for i in range(pointlen) :
                    print('point(s) found in file {0}: {1} {2} - {3}'.format(pointmapname,rowpoint[i],colpoint[i],valpoint[i]), flush = True)

            nr = 0
            raintxtname = []
            sumvalue = []
            
            update_progress(0)
            
            for i in range(pointlen) :
                number = "p{0}_".format(valpoint[i])
                raintxtname.append(outputdir + number + pointnameIn)
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
                    
            #f.close()  # with "with open" you don't need to close!
                    
        for i in range(pointlen) :            
            sumvalue[i] /= 2.0  # from intensity to amount
            print("\nTotal rainfall for point {0}: {1} mm".format(valpoint[i],sumvalue[i]), flush=True)

        print(">>> Done.", flush=True)