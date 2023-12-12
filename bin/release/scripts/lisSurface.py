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

class SurfaceMaps(StaticModel):
    def __init__(self):
        StaticModel.__init__(self)
    def initial(self):
        mask = lg.mask_
        unitmap = lg.lun #readmap(lg.landuseName)
        
         # needed for erosion actually

        if lg.Debug_ :
            print('create RR, n etc', flush=True)

        rr = cover(max(lookupscalar(lg.LULCtable, 1, unitmap), 0.5),1.0) * mask
        report(rr,lg.rrName)
         # micro relief, random roughness (=std dev in cm)

        mann = lookupscalar(lg.LULCtable, 2, unitmap) * mask
        mann = cover(mann,0.05)*mask

        Cover = lookupscalar(lg.LULCtable, 4, unitmap) * mask
        Cover = max(0,min(1.0,Cover))

        plantHeight = lookupscalar(lg.LULCtable, 3, unitmap) * mask
        plantHeight = max(0,plantHeight)

        if lg.doProcessesNDVI == 1:               
            NDVI = readmap(lg.NDVIName)
            NDVI += 0.2
            a_ = 4.257
            b_ = 100.719
            c_ = -5.439
            Cover = min(0.99,max(0.0,a_*NDVI*NDVI + b_*NDVI + c_)/100.0)
            #Using NDVI for the assessment of canopy cover in agricultural crops within modelling research
            # Tenreiro et al 2021
            mann = 0.01*rr + 0.1*Cover                        

        # cover = 1-exp(-0.4*LAI)
        LAI = mask*(ln(1-min(0.95,Cover))/-0.4)   

        report(Cover,lg.coverName)
        report(Cover,lg.LitterName)                
        report(mann,lg.mannName)
        report(LAI, lg.laiName)
        report(plantHeight, lg.plantHeightName)
                        

        # NOTE: this is valid for the Indian LULC map as provided
        smaxnr = lookupscalar(lg.LULCtable, 6, unitmap)
        #report(smaxnr,'smaxnr.map')

        a = [0, 1.412, 0.2331, 0.3165, 1.46, 0.0918, 0.2856, 0.1713,0.59]
        b = [0, 0.531, 0     , 0     , 0.56, 1.04  , 0     , 0     ,0.88]

        smax1 = ifthenelse(smaxnr == 1, a[1]*LAI**b[1],0)*mask
        smax2 = ifthenelse(smaxnr == 2, a[2]*LAI,0)*mask
        smax3 = ifthenelse(smaxnr == 3, a[3]*LAI,0)*mask
        smax4 = ifthenelse(smaxnr == 4, a[4]*LAI**b[4],0)*mask
        smax5 = ifthenelse(smaxnr == 5, a[5]*LAI**b[5],0)*mask
        smax6 = ifthenelse(smaxnr == 6, a[6]*LAI,0)*mask
        smax7 = ifthenelse(smaxnr == 7, a[7]*LAI,0)*mask
        smax8 = ifthenelse(smaxnr == 8, a[8]*LAI**b[8],0)*mask

        Smax = smax1+smax2+smax3+smax4+smax5+smax6+smax7
        report(Smax, lg.smaxName)

        crust = mask*0
        report(crust,lg.crustName)
        # crust fraction assumed zero
        compact = mask*0
        report(compact,lg.compactName)
        # compact fraction assumed zero

        roadwidth = readmap(lg.roadinName)*mask
        report(roadwidth,lg.roadwidthName)

        building = readmap(lg.housecoverinName)*mask
        
        #hardsurf=cover(max(0,1-Cover-building-roadwidth),0)    
        #hardsurf=ifthenelse(Cover > 0.2,0,hardsurf)
        hardsurf = readmap(lg.hardsurfinName)*mask
        report(hardsurf ,lg.hardsurfName)
         #hard surface, here airports and large impenetrable areas
        
        report(building,lg.housecovName)
        roofstore = 1 * mask
        report(roofstore, lg.roofstoreName)
        drumstore = 0 * mask
        report(drumstore, lg.drumstoreName)
        
        