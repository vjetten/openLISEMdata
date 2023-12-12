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

class ChannelMaps(StaticModel):
    #! --lddout
    def __init__(self):
        StaticModel.__init__(self)
    def initial(self):
        
        DEM = lg.DEM_ 
        mask = lg.mask_
        mainout = ifthenelse(lg.mainout_ > 0,scalar(1),0)

        chanmask = ifthen(lg.rivers_ > 0, scalar(1))*mask
        # create missing value outside channel
        lddchan = lddcreate((DEM-mainout*100-chanmask*100)*chanmask,100,1e20,1e20,1e20)
        cm = chanmask
        if lg.doPruneBranch == 1:
            # delete isolated branches of 1 cell
            cm = ifthen(accuflux(lddchan,1) > 1,chanmask)*mask
            lddchan = lddcreate((DEM-mainout*100-cm*100)*cm,100,1e20,1e20,1e20)
            cm = cover(cm, 0)*mask
            chanmask = cm
            
        cm = cover(cm, 0)*mask
        chanmask = cm
        report(lddchan,lg.lddchanName)
        report(cm, lg.chanmaskName)
        
        chWidthmap = mask*lg.chWidth
        chDepthmap = mask*lg.chDepth
        chBaseflowmap = mask*lg.chBaseflow
        #chNmap = mask*chN
 
        dx = celllength()        
        ws = nominal(lg.watersheds_)
        #channelout = zero_

        if lg.doUserOutlets == 1 :
            channelout = lg.mainout_
            Ldd = readmap(lg.LddName)
            chWidthmap = lookupscalar(lg.outletstableName, 1, ws)
            chDepthmap = lookupscalar(lg.outletstableName, 2, ws)
            chBaseflowmap = lookupscalar(lg.outletstableName, 3, ws)
        
        outlet = lg.mainout_
        report(outlet,lg.outletName)
        
        outpoint = lg.mainoutpoint_
        report(outpoint,lg.outpointName)
        
        culverts = mask*0
        if lg.doUseCulverts :
            culverts = readmap(lg.BaseDir+lg.culvertsbaseName)
        report(culverts, lg.chanmaxqName)

        # report(chWidthmap,"chw.map")
        # report(chDepthmap,"chd.map")
        # report(chBaseflowmap,"chbf.map")

        changrad = min(0.5,max(0.001,sin(atan(slope(ifthen(chanmask>0,scalar(1))*DEM)))))
        changrad = windowaverage(changrad, 3*celllength())*ifthen(chanmask>0,scalar(1))
        report(changrad,lg.changradName)

        chanman = cover(chanmask*lg.chN,0)*mask
        report(chanman,lg.chanmanName) # fairly rough and rocky channel beds
        chanside = mask*0 #chanmask*scalar(0)  # ALWAYS rectangular channel
        report(chanside, lg.chansideName)

        # relation by Allen and Pavelski (2015)
        # area = 3.22e4 * width^-1.18 where area is in km2
        # C=3.24×1010m

        #af = accuflux(Ldd, (dx)/1e6)/3.22e4
        #chanwidth = min(0.95*dx, max(2.0, af**(1.18)))*chanmask
        chanlen = accuflux(lddchan, dx)

        #chanwidth = (af**(1.18))*chanmask
        #chanwidth = 20000*(chanlen/3.67e10)**(1.0/2.64)   #Hydro1K allen and pavelsky page 399
        #chanwidth = (chanlen)**(1.0/2.18)   #Hydro1K allen and pavelsky page 399

        chanwidth = (chanlen)**(lg.chB)   #Hydro1K allen and pavelsky page 399
        #chanwidth = 0.1861*(chanlen)**(0.6046) #Sean Taiwan
        maxw = areamaximum(chanlen,ws)*chanmask
        lenrel = (1-(maxw-chanlen)/(maxw-dx)) 
        # make a relative channel width increase from 0 to 1 for every subcatchment
        chanwidth = lenrel*(chWidthmap-lg.chWidthS)+lg.chWidthS
        # scale that map to a minimum of 2 and a maximum of user defined for each catchment
        report(chanwidth,lg.chanwidthName)        
        
        # do the same for depth
        chandepth = max(1.0,chanwidth**lg.chC)**chanmask
        #chandepth = max(1.0,-2.666*ln(chanwidth)+15.76)*chanmask #Sean Taiwan
        chandepth = lenrel*(chDepthmap-lg.chDepthS)+lg.chDepthS
        report(chandepth,lg.chandepthName)

        chanksat = 0*mask
        report(chanksat,lg.chanksatName)

        #bridges=clump(nominal(cover(if(chanwidth gt 9 and roadwidth gt 0 , 1, 0),0)*mask)); #and so ge 4
        #ws=catchment(Ldd_, pit(lddchan))
        #report(ws,wsName)

        ### VJ 210522
        baseflow=lg.mainout_*chBaseflowmap
        report(baseflow,lg.baseflowName)
              
        basereach = spread(nominal(chanmask),0,1)+0.5*celllength()
        report (basereach, lg.basereachName)
        
        lddbase = lddcreate((basereach-lg.mainout_*10),1e20,1e20,1e20,1e20)
        report (lddbase, lg.lddbaseName)
        
        #return mainout_
        