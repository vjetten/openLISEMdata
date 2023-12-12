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

class DamsinRivers(StaticModel):    
    def __init__(self):
        StaticModel.__init__(self)
    def initial(self):     
        DEM = lg.DEM_ 
        mask = lg.mask_
        DAMS_ = readmap(lg.BaseDir+lg.damsbaseName)
        buf = lg.DAMS_

        #wsarea = areaarea(nominal(watersheds))
        # prune 1 cell
        chanmask = ifthen(lg.rivers_ > 0, scalar(1))*mask
        cm = chanmask
        mainout = ifthenelse(lg.mainout_ > 0,scalar(1),0)
        # create missing value outside channel       
        
        lddch = lddcreate(DEM*chanmask-mainout*100,100,1e20,1e20,1e20);
        #outlet = scalar(pit(lddch));
        ups = accuflux(lddch,1);
        chanmask = ifthen(ups > 1,chanmask)
        lddch = lddcreate(DEM*chanmask-mainout*100,100,1e20,1e20,1e20);

        # spread into the dam
        zone = spread(nominal(buf >= 0),0,1);
        cm = ifthenelse(zone >= 2*celllength(),0,cm);
        chanmask = ifthen(cm == 1,scalar(1));

        #ldd now interrupted in dam
        lddch = lddcreate((DEM+buf*10-mainout*100)*chanmask,100,1e20,1e20,1e20);

        # throw out isolated branches in dam itself
        ups = accuflux(lddch,1);
        a = ifthen(areaarea(clump(ups > 0)) > 4*cellarea(),scalar(1));
        lddch = lddcreate((DEM+buf*10-mainout*100)*a,100,1e20,1e20,1e20);

        #create a 0.5 m wall around the dam with an inflow and outflow opening
        zone = spread(nominal(buf < 0),0,1);
        wall = ifthenelse((zone <= celllength()) & (zone != 0),0.5,buf);
        buf=ifthenelse(cover(chanmask,0) > 0,buf,wall);
        report(buf,buffersName);

        #shorten outflowing branch by 2
        ups = accuflux(lddch,1);
        chanmask = ifthen(ups > 1,chanmask);
        lddch = lddcreate((DEM+buf*10-mainout*100)*chanmask,100,1e20,1e20,1e20);

        demold = DEM;

        DEM = ifthenelse(buf < 0, areaaverage(DEM, clump(buf < 0)),DEM);
        report(DEM,lg.DEMName)
        #dif=demold-dem;
        
        chmask=cover(chanmask,0)*mask
        report(chmask,lg.chanmaskName) 
        
        report(lddch, lg.lddchanName)
        
        chanwidth=readmap(lg.chanwidthName)
        chandepth=readmap(lg.chandepthName)
        changrad =readmap(lg.changradName)
        chanman  =readmap(lg.chanmanName)
        chancoh  =readmap(lg.chancohName)
        chanksat =readmap(lg.chanksatName)
               
        chanwidth=ifthenelse(buf != 0, 0.05*chanwidth, chanwidth)*chmask
        chandepth=ifthenelse(buf != 0, 0.1,chandepth)*chmask
        changrad=ifthenelse(buf != 0, 0.001,changrad)*chmask
        chanman=ifthenelse(buf != 0, 0.02,chanman)*chmask
        chancoh=ifthenelse(buf != 0, 100,chancoh)*chmask
        chanksat=ifthenelse(buf != 0, 100,chanksat)*chmask

        report(chanwidth,lg.chanwidthName)
        report(chandepth,lg.chandepthName)
        report(changrad,lg.changradName)
        report(chanman,lg.chanmanName)
        report(chancoh,lg.chancohName)
        report(chanksat,lg.chanksatName)

        grad=readmap(lg.gradName)
        n=readmap(lg.mannName)
        #ksat1=readmap(lg.ksatName+"1.map")

        grad=ifthenelse(buf != 0,0.001,grad)
        n=ifthenelse(buf != 0,0.005,n)
        #ksat1=ifthenelse(buf != 0,0,ksat1)
        
        report(grad,lg.gradName)
        report(n,mlg.annName)
        #report(ksat1,lg.ksatName+"1.map")

