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

class DEMderivatives(StaticModel):
    def __init__(self):
        StaticModel.__init__(self)
    def initial(self):
        DEM = lg.DEM_
        mask = lg.mask_
        if lg.doCatchment == 0 :
            lg.catchmentsize_ = 1e20

        size = lg.catchmentsize_   #????
        
        ID = mask
        report(ID,lg.IDName)

        IDET = mask
        report(IDET,lg.IDETName)

        buffers = scalar(0) #readmap(buffersinName)*mask
        report(buffers,lg.buffersName);

        # fill in pits
        DEMc = DEM
        if lg.doCorrectDEM > 0 :            
            #print(">>> Filling in DEM depressions (see demcorr.map for filled in pixels)",flush=True)            
            DEMc = lddcreatedem(DEM, 1e20,1e20,9*cellarea(),1e20)
            DEMcorrect = DEMc - DEM
            DEMcorrect = ifthenelse(DEMcorrect < lg.fillDEM,0,DEMcorrect)
            DEMc = DEM+DEMcorrect
            report(DEMcorrect, lg.MapsDir+"demcorr.map")

        # add buffers/dykes to the DEM to include in ldd and gradient
        DEMm = DEMc + buffers;
        report(DEMc, lg.DEMName)
        DEM = DEMc
       
        chanm = cover(lg.rivers_, 0)*mask
        mainout = ifthenelse(lg.mainout_ > 0, scalar(1), 0)  
        #wsarea = areaarea(nominal(watersheds_))          
        #watersheds_ is mask if not multiple watersheds
        #mainout_ can be sero, then endpoint must be used

        thr = 100
        Ldd = lddcreate (DEMc-chanm*thr-mainout*thr, thr, size, size, size)
        report(Ldd, lg.LddName)
        Ldd_ = Ldd

        outlet = lg.mainout_
        report(outlet,lg.outletName)
        outpoint = lg.mainoutpoint_
        report(outpoint,lg.outpointName)

        # runoff flow network based on dem, main outlet, channels and barriers
        grad = sin(atan(slope(DEMm)))
        report(grad, lg.gradName)

        #### not used in lisem, auxilary maps

        ups=accuflux(Ldd,1)
        report(ups,lg.upsName)  # not used
        wsn = catchment(Ldd, pit(Ldd));
        report(wsn, lg.wsName)

        asp = scalar( aspect(DEMm));
        shade = cos(15)*sin(grad)*cos(asp+45) + sin(15)*cos(grad);
        shade = 0.7*(shade-mapminimum(shade))/(mapmaximum(shade)-mapminimum(shade))
        + 0.3*(DEMm-mapminimum(DEMm))/(mapmaximum(DEMm)-mapminimum(DEMm))

        report(shade,lg.shadeName)  # not used in lisem

