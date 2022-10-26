# lisemDBASEgenerator
# global vraiables and initialisation
#
# author: V.G.Jetten @ 2022
# University of Twente, Faculty ITC
# this software has copyright model: GPLV3
# this software has a disclaimer

from pcraster import *
from pcraster.framework import *
import lisGlobals as lg
# linear regression for D50 and D90
from scipy import stats

# update_progress() : Displays or updates a console progress bar
def update_progress(progress):
    barLength = 50 # Modify this to change the length of the progress bar
    if progress >= 0.99:
        progress = 1
    block = int(round(barLength*progress))
    text = "\rProcessing: [{0}] {1:.3g}% ".format( "#"*block + "-"*(barLength-block), progress*100)
    sys.stdout.write(text)
    sys.stdout.flush()


class ErosionMaps(StaticModel):
    def __init__(self):
        StaticModel.__init__(self)
    def initial(self):
        mask = lg.mask_

        print(">>> Creating Erosion params ", flush=True)

        ############################################
        ## Generation of soil cohesion map        ##
        ## estimation based on clay content       ##
        ## adapted from Morgan, 2001              ##
        ############################################

        C = readmap(lg.BaseDir+'clay1.map')
        S = readmap(lg.BaseDir+'sand1.map')
        Si = readmap(lg.BaseDir+'silt1.map')
        unitmap = readmap(lg.landuseName)
        Cover = readmap(lg.coverName)

        #Coh = ifthenelse(C < 1e-5, -1,max(1.0, 4.316*ln(C+1.0) - 6.955))
        Coh = ifthenelse(C < 1e-5, -1,max(1.0, 7.018*ln(C) + 13.312))
        # log fit using values below
        #Coh = lookupscalar("claycoh.tbl",C)*mask
        # content of claycoh.tbl
        # [,20>   2
        # [20,35> 3
        # [35,40> 9
        # [40,55> 10
        # [55,60> 11
        # [60,100> 12

        cropheight = lookupscalar(lg.LULCtable, 3, unitmap) * mask #plant height in m
        report(cropheight,lg.cropheightName)

        aggrstab = ((S+0.15*C)/1.3) * mask #from table A9.1 page 27 eurosem manual 2nd column erod (= kfactor multiply directly with splash energy)
        
        # detachability in g/J in lisem this is directly multiplied to the KE
        #aggrstab = 6 * mask;  # aggregate stability
        report(aggrstab,lg.asName)
        
        cohadd = lookupscalar(lg.LULCtable, 7, unitmap) * mask #added cohesion by roots
        
        Coh = ifthenelse(cohadd < 0, -1, Coh)    
        report(Coh, lg.cohName)
        
        cohplant = cohadd #Cover * ifthenelse(cohadd < 0,0,cohadd) * mask  # additional plant root strength
        report(cohplant,lg.cohaddName)
        
        chancoh =  Coh*cover(lg.rivers_, 0)*mask  
        if lg.doChannelsNoEros == 1:
            chancoh = -1*cover(lg.rivers_, 0)*mask               
        report (chancoh, lg.chancohName)            
        
        
        D50 = scalar(0)
        D90 = scalar(0)              

        if lg.optionD50 == 1 :
            print('>>> estimating d50 and d90 from log-linear regression for every cell', flush=True)
            
            #convert texture maps to 2D arrays to access cells, -9999 is MV
            cp = pcr2numpy(C, -9999)
            ctemp = numpy2pcr(Scalar,cp,-9999)
            sip = pcr2numpy(Si, -9999)
            sp = pcr2numpy(S, -9999)
            d50p = pcr2numpy(D50, -9999)
            d90p = pcr2numpy(D90, -9999)

            # linear regression on 3 points: cum fractions C,C+si,C+si+sa, against LN of grainsize
            # then find grainsize for median 0.5 (50%) and 90% quantile
            for row in range(1,lg.nrRows) :
                if row % int(lg.nrRows/50) == 0 :
                    update_progress(row/lg.nrRows)
                for col in range(1,lg.nrCols) :
                    c = cp[row][col]#cellvalue(C, row, col)
                    si = sip[row][col]#cellvalue(Si, row, col)
                    s = sp[row][col]#cellvalue(S, row, col)
                    x = [c,c+si,c+si+s]
                    y = [0.693147181,3.912023005,6.214608098] # LN of average gransize clay (2), silt (50)  sand (500)
                    res = stats.linregress(x, y)
                    #print("a",res.intercept)
                    #print("a",res.slope)
                    # # linear regression between cumulative texture fraction and ln(grainsize)
                    d50p[row][col] = exp(0.5*res.slope+res.intercept)
                    d90p[row][col] = exp(0.9*res.slope+res.intercept)
            update_progress(1)
            
            # convert 2D array to PCRaster and report
            D50 = numpy2pcr(Scalar,d50p,-9999)
            D50 = ifthenelse(D50 > 0,D50,maptotal(D50)/maptotal(mask))
            report(D50*mask,lg.d50Name)
            
            D90 = numpy2pcr(Scalar,d90p,-9999)
            D90 = ifthenelse(D90 > 0,D90,maptotal(D90)/maptotal(mask))
            report(D90*mask,lg.d90Name)
                                    
            print("\n", flush=True)
