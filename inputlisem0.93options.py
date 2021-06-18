"""
Created on Fri Mar 19 14:07:11 2021
openlisem input script, v0.7
to be used with Qt UI interface
@author: v jetten, ITC
"""

# In conda make sure the following libs are instaklled:
#     conda create --name lisem python
#     conda activate lisem
#     conda install -c conda-forge pcraster owslib scipy gdal
#     pip install osgeo

# gdal
#from osgeo import gdal
from osgeo import gdal, gdalconst, osr
from owslib.wcs import WebCoverageService

# pcraster
from pcraster import *
from pcraster.framework import *

# operation system
import subprocess  # call exe from wihin script
import os          # operating system, change dir
import sys         # read commandline arguments

# linear regression for D50 and D90
from scipy import stats


setglobaloption("lddin")
setglobaloption("lddfill")
setglobaloption("matrixtable")



### ---------- class DEMderivatives() ---------- ###

class DEMderivatives(StaticModel):
    def __init__(self):
        StaticModel.__init__(self)
    def initial(self):
        mask = mask_
        size = catchmentsize_
        global mainout_
        global DEM_
        DEM = DEM_
        global Ldd_
        global doCorrectDEM
        global fillDEM

        ID = mask
        report(ID,IDName)
        IDET = mask
        report(IDET,IDETName)

        barriers = scalar(0) #readmap(buffersinName)*mask
        report(barriers,buffersName);

        #DEM = readmap(BaseDir+DEMbaseName)*mask
        DEMc = DEM
        if doCorrectDEM > 0 :
            w = fillDEM  ### VJ 210522 was 10**filldem
            print("Filling in DEM depressions, see demcorr.map",flush=True)
            DEMc = lddcreatedem(DEM, w,w,w,w)
            DEMcorrect = DEMc - DEM
            report(DEMcorrect, MapsDir+"demcorr.map")

        DEMm = DEMc + barriers;
        report(DEMm, DEMName)
        DEM_ = DEMm

        chanm = scalar(0)
        if  doProcessesChannels == 1:
            chanm = readmap(BaseDir+riversbaseName)*mask
            #chanm = cover(ifthen(chanm > 1, scalar(1)),0)*mask
            chanm = cover(chanm, 0)*mask

        Ldd = lddcreate (DEMm-chanm*10-mainout_*10, size, size, size, size)
        report(Ldd, LddName)
        Ldd_ = Ldd

        if  doProcessesChannels == 0:
            if  doUserOutlets == 0 :
                mainout_ = cover(scalar(pit(Ldd)),0)*mask            
            outpoint = mainout_
            report(outlet,outletName)
            report(outpoint,outpointName)      

        # runoff flow network based on dem, main outlet, channels and barriers        
        grad = sin(atan(slope(DEMm)))
        report(grad, gradName)

        #### not used in lisem, auxilary maps

        ups=accuflux(Ldd,1)
        report(ups,upsName)  # not used
        ws=catchment(Ldd, pit(Ldd));
        report(ws,wsName)

        asp = scalar( aspect(DEMm));
        shade = cos(15)*sin(grad)*cos(asp+45) + sin(15)*cos(grad);
        shade = 0.7*(shade-mapminimum(shade))/(mapmaximum(shade)-mapminimum(shade))
        + 0.3*(DEM-mapminimum(DEM))/(mapmaximum(DEM)-mapminimum(DEM))

        report(shade,shadeName)  # not used in lisem


        distriv = spread(cover(nominal(chanm > 0),0),0,1)*mask
       # distsea = spread(nominal(1-cover(mask,0)),0,1)*mask
        soild = mask*cover((1-min(1,slope(DEMm)))       # steeper slopes giver undeep soils
               -0.5*distriv/mapmaximum(distriv)  # perpendicular distance to river, closer gives deeper soils
              # +0.5*(distsea/mapmaximum(distsea))**0.1
               ,0)
        soildb = 1500*(soild)**1.5

        # m to mm for lisem, higher power emphasizes deep, updeep
        soildepth1 = soildepth1depth*mask
        soildepth2 = mask*(soildepth1+windowaverage(soildb,3*celllength()))

        report(soildepth1,soildep1Name)
        report(soildepth2,soildep2Name)

### ---------- class GetSoilGridsLayer ---------- ###

class GetSoilGridsLayer:
    "downbloading a SOILGRIDS layer from WCS service"
    def __init__(self, mask, ESPG="",s="", i=1, j = 1):
        self.mask = mask
        self.varname = s
        self.layer = i
        self.outlayer = j
        self.debug = Debug_
        self.ESPG = ESPG

        if self.layer == 1: ID='_0-5cm_mean'
        if self.layer == 2: ID='_5-15cm_mean'
        if self.layer == 3: ID='_15-30cm_mean'
        if self.layer == 4: ID='_30-60cm_mean'
        if self.layer == 5: ID='_60-100cm_mean'
        if self.layer == 6: ID='_100-200cm_mean'

        #if self.debug == 1:
        print("===> Processing layer "+str(self.outlayer)+": "+self.varname+ID, flush=True)

       # raster=gdal.Open(self.mask)
        ESPG = 'urn:ogc:def:crs:EPSG::{0}'.format(self.ESPG)

        if self.debug == 1:
            print("Mask ESPG and bounding box:"+ESPG,llx,lly,urx,ury,dx,dy, flush=True)

        if self.debug == 1:
            print("Open SOILGRIDS WCS", flush=True)

        url = "http://maps.isric.org/mapserv?map=/map/{}.map".format(self.varname)
        wcs = WebCoverageService(url, version='1.0.0')
        # show some info:
        # cov_list = list(wcs.contents)
        # mean_covs = [k for k in wcs.contents.keys() if k.find("mean") != -1]
        # print(mean_covs)

        variable = self.varname+ID
        varout = self.varname+str(self.outlayer)
        outputnametif = "{0}.tif".format(varout)
        outputnamemap = "{0}.map".format(varout)
        #outputnametmp = '_temp_.tif'

        if self.debug == 1:
            print("Downloading "+variable, flush=True)

        # get data as temp geotif and save to disk
        response = wcs.getCoverage(identifier=variable,crs=ESPG,bbox=maskbox,
            resx=dx,resy=dx,format='GEOTIFF_INT16')
        with open(outputnametif, 'wb') as file:
             file.write(response.read())

        # warp to some interpolation
        src = gdal.Open(outputnametif, gdalconst.GA_ReadOnly)
        src_proj = src.GetProjection()
        src_geotrans = src.GetGeoTransform()
        dst = gdal.GetDriverByName('PCRaster').Create(outputnamemap, nrCols, nrRows, 1,
                                   gdalconst.GDT_Float32,["PCRASTER_VALUESCALE=VS_SCALAR"])
        dst.SetGeoTransform( src_geotrans )
        dst.SetProjection( src_proj )
        gdal.ReprojectImage(src, dst, src_proj, src_proj, gdalconst.GRA_Bilinear)
        #gdalconst.GRA_Cubic)

        # brute force convert tif to map by calling pcrcalc !!!!
        # CMD = "pcrcalc.exe"
        # arg = outputnamemap+"="+outputnametif
        # arg = '{0}{1}.map={0}{1}.tif'.format(self.varname,str(self.outlayer))
        # subprocess.run([CMD,arg])

        dst = None
        src = None


### ---------- class PedoTranfer() ---------- ###

class PedoTransfer(StaticModel):
    # creates infiltration input vars: Ksat 1,2; Thetas1,2; Thetai1,2; Psi1,2
    # from SOILGRID.ORG GTiff maps for texture, org matter, gravel and bulkdensity
    # Using Saxton And Rawls 2006 pedotransferfunctions
    # https://hrsl.ba.ars.usda.gov/SPAW/Index.htm
    def __init__(self,mask=0,layer=1,moisture=0.7,sBD=1350.0):
        StaticModel.__init__(self)
    def initial(self):
        standardBD = scalar(standardbulkdensity_)  # standard bulk dens assumed by saxton and rawls. High! 1350 would be better
        fractionmoisture = scalar(initmoisture_)   #inital moisture as fraction between porosity and field capacity
        x = layer_
        mask = mask_

       # S1 = readmap("{0}{1}.map".format(SG_names_[0],str(x)))  # sand g/kg
       # Si1 = readmap("{0}{1}.map".format(SG_names_[1],str(x))) # silt g/kg
       # C1 = readmap("clay1.map")#{0}{1}.map".format(SG_names_[2],str(x)))  # clay g/kg
       # OC1 = readmap("{0}{1}.map".format(SG_names_[3],str(x)))  # organic carbon in dg/kg
       # Grv = readmap("{0}{1}.map".format(SG_names_[4],str(x))) # coarse fragments cm3/dm3,
       # bd1 = readmap("{0}{1}.map".format(SG_names_[5],str(x)))   # bulk density in cg/m3
        S1 = readmap("sand{0}.map".format(str(x)))  # sand g/kg
        Si1 = readmap("silt{0}.map".format(str(x))) # silt g/kg
        C1 = readmap("clay{0}.map".format(str(x)))  # clay g/kg
        OC1 = readmap("soc{0}.map".format(str(x)))  # organic carbon in dg/kg
        Grv = readmap("cfvo{0}.map".format(str(x))) # coarse fragments cm3/dm3,
        bd1 = readmap("bdod{0}.map".format(str(x)))   # bulk density in cg/m3

        #output map name strings
        om1 = "om{0}.map".format(str(x))             # organic matter in %
        WP1 = "wilting{0}.map".format(str(x))      	# wilting point moisture content
        FC1 = "fieldcap{0}.map".format(str(x))     	# field capacity moisture content
        PAW1 = "plantAVW{0}.map".format(str(x))    	# plant available water content
        Coh1 = cohName+".map"           # soil cohesion (kPa)   ### VJ 210522
        #K1 = "k{0}.map".format(str(x))  		        #USLE erodibility
        BD1 = "bulkdens{0}.map".format(str(x))       # bulk density in kg/m3
        Pore1 = poreName+"{0}.map".format(str(x))   	#porosity (cm3/cm3)
        Ksat1 = ksatName+"{0}.map".format(str(x))      	#ksat in mm/h
        initmoist1 = thetaiName+"{0}.map".format(str(x))  # inital moisture (cm3/cm3)
        psi1 = psiName+"{0}.map".format(str(x))  		    # suction with init moisture in cm, used in LISEM
        Densityfactor1 = "densfact{0}.map".format(str(x))

        print("Creating infil params layer "+str(x), flush=True)

        S = S1/1000  # from g/kg to fraction
        C = C1/1000
        Si = Si1/1000
        OC = (OC1/10000)*100  # conversion OC from dg/kg to percentage
        OM = OC*1.73  #/2.0   #conversion org carbon to org matter factor 2

        unitmap = readmap(landuseName)
        ## VJ 210530 concevt to nominal maps
        Sn = nominal(S*1000)
        Sin = nominal(Si*1000)
        Cn = nominal(C*1000)
        OMn = nominal(OM*1000)
        bd1n = nominal(bd1*1000)
        Grvn = nominal(Grv*1000)        

        # quick and dirty filling up from the sides
        S = scalar(spreadzone(Sn,0,1))/1000.0
        Si = scalar(spreadzone(Sin,0,1))/1000.0
        C = scalar(spreadzone(Cn,0,1))/1000.0
        OM = scalar(spreadzone(OMn,0,1))/1000.0
        bd1 = scalar(spreadzone(bd1n,0,1))/1000.0
        Grv= scalar(spreadzone(Grvn,0,1))/1000.0

        report(OM, om1)

        densityveg = lookupscalar(LULCtable, 5, lun)

        bdsg = bd1*10            #bulkdensity cg/m3 to kg/m3
        bdsg = ifthenelse(bd1 < 1,standardBD,bdsg) # replace areas with MV bdsg to standard BD
        Gravel = Grv/1000  # from cm3/dm3 (1000 cc in a liter)
        Densityfactor = scalar(1.0)
        #Densityfactor = densityveg * scalar(0.95) #bdsg/standardBD*Dens #(1-0.1*cover)
        if useBulkdensity == 1:
            Densityfactor = min(max(0.9, standardBD/bdsg), 1.2)
        # density factor is 1.0, but could be made lower for organic soils and higher for compacted urban areas.
        report(Densityfactor,Densityfactor1)

        # wilting point stuff
        M1500 =-0.024*S+0.487*C+0.006*OM+0.005*S*OM-0.013*C*OM+0.068*S*C+0.031  #W18)
        # =-0.024*F18+0.487*G18+0.006*H18+0.005*F18*H18-0.013*G18*H18+0.068*F18*G18+0.031
        M1500adj =M1500+0.14*M1500-0.02  #X18) =W18+0.14*W18-0.02
        # field capacity stuff
        M33  =-0.251*S+0.195*C+0.011*OM+0.006*S*OM-0.027*C*OM+0.452*S*C+0.299  #Y18)
        #=-0.251*F18+0.195*G18+0.011*H18+0.006*F18*H18-0.027*G18*H18+0.452*F18*G18+0.299
        M33adj = M33+(1.283*M33*M33-0.374*M33-0.015)  #Z18) =Y18+(1.283*Y18*Y18-0.374*Y18-0.015)
        # porosity - FC
        PM33    = 0.278*S+0.034*C+0.022*OM-0.018*S*OM-0.027*C*OM-0.584*S*C+0.078  #AA18)
        #=0.278*F18+0.034*G18+0.022*H18-0.018*F18*H18-0.027*G18*H18-0.584*F18*G18+0.078
        PM33adj = PM33+(0.636*PM33-0.107)  #AB18) =AA18+(0.636*AA18-0.107)
        # porosity
        SatPM33 = M33adj + PM33adj  #AC18) =AB18+Z18
        SatSadj = -0.097*S+0.043  #AD18) =-0.097*F18+0.043
        SadjSat = SatPM33  + SatSadj  #AE18) =AC18+AD18
        Dens_om = (1-SadjSat)*2.65  #AF18) =(1-AE18)*2.65
        Dens_comp = Dens_om * Densityfactor  #AG18) =AF18*(I18)
        PORE_comp =(1-Dens_om/2.65)-(1-Dens_comp/2.65)  #AI18) =(1-AG18/2.65)-(1-AF18/2.65)
        M33comp = M33adj + 0.2*PORE_comp  #AJ18)  =Z18+0.2*AI18

        #output maps
        POROSITY = (1-Dens_comp/2.65)*mask  #AH18)
        PoreMcomp = POROSITY-M33comp  #AK18)
        LAMBDA = (ln(M33comp)-ln(M1500adj))/(ln(1500)-ln(33))  #AL18)
        GravelRedKsat =(1-Gravel)/(1-Gravel*(1-1.5*(Dens_comp/2.65)))  #AM18)
        #report(LAMBDA,'lambda.map')
        #report(PoreMcomp,'PoreMcomp.map')
        #report(M33comp,'M33comp.map')
        Ksat = mask*max(0.0, 1930*(PoreMcomp)**(3-LAMBDA)*GravelRedKsat)  #AN18)
        BD = Gravel*2.65+(1-Gravel)*Dens_comp* mask     #U18
        WP = M1500adj*mask
        FC = M33adj* mask
        PAW = (M33adj - M1500adj)*(1-Gravel)* mask

        # POROSITY = ifthenelse(unitmap == unitBuild_, Poreurban_, POROSITY)
        # Ksat = ifthenelse(unitmap == unitBuild_, Ksaturban_, Ksat)
        # POROSITY = ifthenelse(unitmap == unitWater_, 0, POROSITY)
        # Ksat = ifthenelse(unitmap == unitWater_, 0, Ksat)

        initmoist = fractionmoisture*POROSITY+ (1-fractionmoisture)*FC

        report(POROSITY,Pore1)
        report(Ksat,Ksat1)
        report(BD,BD1)
        report(WP,WP1)
        report(FC,FC1)
        report(PAW,PAW1)
        report(initmoist,initmoist1)

        # A = exp[ln(33) + B ln(T33)]
        # B = [ln(1500) - ln(33)] / [ln(T33) - ln(T1500)]
        bB = (ln(1500)-ln(33))/(ln(FC)-ln(WP))
        aA = exp(ln(33)+bB*ln(FC))
        Psi1= aA * initmoist**-bB *100/9.8
        report(Psi1,psi1)
        report(initmoist/POROSITY,"se1.map")

        ############################################
        ## Generation of soil cohesion map        ##
        ## estimation based on clay content       ##
        ## adapted from Morgan, 2001              ##
        ############################################
        if optionerosion == 1 and x == 1:
            Coh = max(1.0, 4.316*ln(C+1.0) - 6.955)
            # log fit using values below
            Coh = ifthenelse((unitmap == unitBuild_) | (unitmap == unitWater_) , -1, Coh)
            #Coh = lookupscalar("claycoh.tbl",C)*mask
            # content of claycoh.tbl
            # [,20>   2
            # [20,35> 3
            # [35,40> 9
            # [40,55> 10
            # [55,60> 11
            # [60,100> 12

            report(Coh, Coh1)
            report(Coh,aggrstabName)
            D50 = scalar(0)
            D90 = scalar(0)

            if optionD50 == 1 :
                print('estimating d50 and d90 from regression texture of every cell (may take some time)', flush=True)
                cp = pcr2numpy(C, -9999)
                ctemp = numpy2pcr(Scalar,cp,-9999)
                report(ctemp,"ctemp.map")
                report(C,"ctemp2.map")
                sip = pcr2numpy(Si, -9999)
                sp = pcr2numpy(S, -9999)
                d50p = pcr2numpy(D50, -9999)
                d90p = pcr2numpy(D90, -9999)

                step = 1
                #star = ["|","/","-","\\"]
                #sr = 0
                for row in range(1,nrRows) :
                    sss = "D50-D90 ["+"#"*step+"-"*(50-step-1)+"]"
                    #sr+= 1
                   # if sr == 4: sr = 0
                    if row % int(nrRows/50+0.5) == 0 :
                        step += 1
                        print("\r" + sss, end="", flush=True)
                    for col in range(1,nrCols) :
                        c = cp[row][col]#cellvalue(C, row, col)
                        si = sip[row][col]#cellvalue(Si, row, col)
                        s = sp[row][col]#cellvalue(S, row, col)
                        x = [c,c+si,1.0]
                        y = [0.693147181,3.912023005,6.214608098] # ln of average gransize clay (2), silt (50)  sand (500)
                        res = stats.linregress(x, y)  
                        # linear regression 3 points: cum fractions C,C+si,C+si+sa, then find grainsize for median 0.5 (50%)
                        #print("a",res.intercept)
                        #print("a",res.slope)
                        # # linear regression between cumulative texture fraction and ln(grainsize)
                        if res.slope > 1e-3 :
                            d50p[row][col] = exp(0.5*res.slope+res.intercept) #exp((0.5-res.intercept)/res.slope)
                            d90p[row][col] = exp(0.9*res.slope+res.intercept)#exp((0.9-res.intercept)/res.slope)
                        else :
                            d50p[row][col] = 0
                            d90p[row][col] = 0
                        #print(row,col,c,si,s,d50p[row][col],res.intercept,res.slope)

                #print(d50p[100][100])
                D50 = numpy2pcr(Scalar,d50p,-9999)
                D50 = ifthenelse(D50 > 0,D50,maptotal(D50)/maptotal(mask))
                report(D50*mask,d50Name)
                D90 = numpy2pcr(Scalar,d90p,-9999)
                D90 = ifthenelse(D90 > 0,D90,maptotal(D90)/maptotal(mask))
                report(D90*mask,d90Name)
                print("\n", flush=True)


### ---------- class SurfaceMaps() ---------- ###

class SurfaceMaps(StaticModel):
    def __init__(self):
        StaticModel.__init__(self)
    def initial(self):
        mask = mask_
        unitmap = lun #readmap(landuseName)

        if Debug_ :
            print('create RR, n etc', flush=True)

        rr = cover(max(lookupscalar(LULCtable, 1, unitmap), 0.5),1.0) * mask
        report(rr,rrName)
         # micro relief, random roughness (=std dev in cm)

        mann = lookupscalar(LULCtable, 2, unitmap) * mask
        mann = cover(mann,0.05)*mask
        # mann = 0.01*rr + 0.1*Cover
        report(mann,mannName)
         # in the lisem code Manning's n is increased with house effect

        Cover = lookupscalar(LULCtable, 4, unitmap) * mask
        Cover = min(0.95,Cover)
        report(Cover,coverName)

        # cover = exp(-0.4*LAI)
        LAI = ifthenelse(Cover > 0,ln(Cover)/-0.4,0)
        LAI = max(min(6.5, LAI), 0.0)*mask
        report(LAI, laiName)

        # NOTE: this is valid for the Indian LULC map as provided
        smaxnr = lookupscalar(LULCtable, 6, unitmap)
        #report(smaxnr,'smaxnr.map')

        a = [0, 1.412, 0.2331, 0.3165, 1.46, 0.0918, 0.2856, 0.1713,0.59]
        b = [0, 0.531, 0     , 0     , 0.56, 1.04  , 0     , 0     ,0.88]

        smax1 = ifthenelse(smaxnr == 1, a[1]*LAI**b[1],0)*mask
        smax2 = ifthenelse(smaxnr == 2, a[2]*LAI,0)*mask
        smax3 = ifthenelse(smaxnr == 2, a[3]*LAI,0)*mask
        smax4 = ifthenelse(smaxnr == 3, a[4]*LAI**b[4],0)*mask
        smax5 = ifthenelse(smaxnr == 4, a[5]*LAI**b[5],0)*mask
        smax6 = ifthenelse(smaxnr == 5, a[6]*LAI,0)*mask
        smax7 = ifthenelse(smaxnr == 6, a[7]*LAI,0)*mask
        smax8 = ifthenelse(smaxnr == 7, a[8]*LAI**b[8],0)*mask

        Smax = smax1+smax2+smax3+smax4+smax5+smax6+smax7
        report(Smax, smaxName)

        crust = mask*0
        report(crust,crustName)
        # crust fraction assumed zero
        compact = mask*0
        report(compact,compactName)
        # compact fraction assumed zero

        stone = mask*0
        report(stone,stoneName)
        # compact fraction assumed zero

        hardsurf = readmap(hardsurfinName)*mask
        report(hardsurf ,hardsurfName)
         #hard surface, here airports and large impenetrable areas

        roadwidth = readmap(roadinName)*mask
        report(roadwidth,roadwidthName)

        building = readmap(housecoverinName)*mask
        report(building,housecovName)


        if optionerosion == 1:
            cropheight = lookupscalar(LULCtable, 3, unitmap) * mask #plant height in m
            report(cropheight,cropheightName)

            aggrstab = 6 * mask;  # aggregate stability
            report(aggrstab,asName)

            cohplant = Cover * 5.0 * mask  # additional plant root strength
            report(cohplant,cohaddName)


### ---------- class ChannelMaps() ---------- ###
class ChannelMaps(StaticModel):
    #! --lddout
    def __init__(self):
        StaticModel.__init__(self)
    def initial(self):
        mask = mask_
        global mainout_  # is zero or if dem is done is endpoints ldd, or userdefined endpoints
        DEM = readmap(DEMName)
        global Ldd_
        global doUserOutlets

        rivers = readmap(BaseDir+riversbaseName)
        chanmask = ifthen(rivers > 0, scalar(1))*mask
        # create missing value outside channel

        lddchan = lddcreate((DEM-mainout_*10)*chanmask,1e20,1e20,1e20,1e20)
        cm = chanmask
        if doPruneBranch == 1:
            # delete isolated branches of 1 cell
            cm = ifthen(accuflux(lddchan,1) > 1,chanmask)*mask
            lddchan = lddcreate((DEM-mainout_*10)*cm,1e20,1e20,1e20,1e20)
            cm = cover(cm, 0)*mask
        
        report(lddchan,lddchanName)
        report(cm, chanmaskName)                    
        
        if doUserOutlets == 0 :
            mainout_ = cover(scalar(pit(lddchan)),0)*mask             
        
        outpoint = mainout_
        outlet = mainout_
        report(outlet,outletName)
        report(outpoint,outpointName)

        changrad = min(0.5,max(0.01,sin(atan(slope(chanmask*DEM)))))
        changrad = windowaverage(changrad, 3*celllength())*chanmask
        report(changrad,changradName)

        chanman = cover(chanmask*0.05,0)*mask
        report(chanman,chanmanName) # fairly rough and rocky channel beds
        chanside = mask*0 #chanmask*scalar(0)  # ALWAYS rectangular channel
        report(chanside, chansideName)

        # relation by Allen and Pavelski (2015)
        Ldd = readmap(LddName)
        dx = celllength()
        af = accuflux(Ldd, dx/3.22e4)
        chanwidth = min(0.95*dx, max(2.0, af**(1.18)))*chanmask
        report(chanwidth,chanwidthName)
        ##  culvert_fraction_width = 0.8;
        ##  report chanwidth = min(celllength()*0.95, if(culverts gt 0, chanwidth*culvert_fraction_width, chanwidth));
        ##  # channel width is 15m at outlet and beccoming less away form the coast to 3 m
        chandepth = cover(max(1.0,chanwidth**0.2),0)*mask
        #chandepth = min(chandepth, 1.0/(sqrt(changrad)/chanman))
        report(chandepth,chandepthName)

        chanmaxq = 0*mask#if(culverts gt 0, 2, 0)*mask;
        report(chanmaxq,chanmaxqName)
        chanksat = 0*mask
        report(chanksat,chanksatName)

        #bridges=clump(nominal(cover(if(chanwidth gt 9 and roadwidth gt 0 , 1, 0),0)*mask)); #and so ge 4
        ws=catchment(Ldd_, pit(lddchan));
        report(ws,wsName)

        ### VJ 210522
        bfh = min(1.0, 0.5*chandepth) # baseflow water height is 1.0m or 0.5 of channelhwight
        baseflow=cover(scalar(pit(lddchan) != 0)*bfh*chanwidth*0.5,0)*mask
        report(baseflow,baseflowName)
        # assuming 0.5 m/s baseflow
        
        ### VJ 210522
        chancoh = 10*mask;
        report (chancoh, chancohName);


### ---------- START ---------- ###

# NIOTE: preperatory actions
# 1. QGIS: download SRTM
# 2. PCRaster create an ldd using 1e8 as weight and --lddin
# 3. create watersheds: pcrcalc ws.map=catchment()ldd.map, pit(ldd.map))
# 4. select appropriate water (cauvery has nr 78)
# craete a mask from this watershed abnd use resample to eliminate ros and cols with missing cvalue


if __name__ == "__main__":
    print(">>> defining and reading standard options",flush=True)


    #default values for interface options
    doProcessesDEM = 1
    doProcessesChannels = 1
    doProcessesInFil = 1
    doProcessesSG = 1
    doProcessesLULC = 1
    optionerosion = 1
    optionD50 = 0
    optionSG1 = 2
    optionSG2 = 4
    doCorrectDEM = 0
    doUserOutlets = 0  ## VJ 210523  added options user defined outlets that are forced in the DEM
    doPruneBranch = 0
    useBulkdensity = 0
    standardbulkdensity_ = 1350.0
    initmoisture_ = 0.5
    ### input maps ###
    MapsDir = "/Maps"
    BaseDir = "/Base"
    lulcDir = "/lulc"
    DEMbaseName = "dem0.map"
    riversbaseName = "chanmask0.map"
    outletsbaseName = "outlet0.map"
    masknamemap_ = "mask0.map" 
    lulcTIF = "lulc.tif"
    lulcTable = "lulc.tbl"
    fillDEM = 1e5  # use fill dem with lddcreatedem, if doCorrectDEM = 0 then this is not used
    catchmentsize_ = 1e9
    ESPGnumber = "32644"

    ### ------ GET INTERFACE OPTIONS ------ ###
    # Read options input file generated by the UI interface
    # file has the name=value format, all strings

    # debug
    # print (sys.argv[0:])
    # print(len(sys.argv))
    # if len(sys.argv) < 2:
    #     print("no config file loaded")
    #     sys.exit()


    myvars = {}
    with open(sys.argv[1], 'r') as myfile:
        for line in myfile:
            if '=' not in line:
                continue
            S0 = (line.split('='))[0].strip()
            S1 = (line.split('='))[1].strip()
            myvars[S0] = S1

    BaseDir = myvars["BaseDirectory"]
    DEMbaseName = myvars["BaseDEM"]
    riversbaseName = myvars["BaseChannel"]
    MapsDir = myvars["MapsDirectory"]
    lulcDir = myvars["LULCDirectory"]
    lulcTIF = myvars["LULCmap"]
    lulcTable = myvars["LULCtable"]
    ESPGnumber = myvars["ESPGnumber"]
    doProcessesDEM = int(myvars["optionDEM"])
    doProcessesChannels = int(myvars["optionChannels"])
    doProcessesInfil = int(myvars["optionInfil"])
    doProcessesSG = int(myvars["optionSG"])
    doProcessesLULC = int(myvars["optionLULC"])
    optionD50 = int(myvars["optionErosion"])
    optionSG1 = int(myvars["optionSG1"])+1
    optionSG2 = int(myvars["optionSG2"])+1
    doCorrectDEM = int(myvars["optionFillDEM"])
    doUserOutlets = int(myvars["optionUserOutlets"])
    if doUserOutlets == 1:
        outletsbaseName = myvars["BaseOutlets"]  ## VJ 210523 added user defined outlets, optional
    doPruneBranch = int(myvars["optionPruneBranch"])
    useBulkdensity = int(myvars["optionUseBD"])
    standardbulkdensity_ = float(myvars["refBulkDens"])
    initmoisture_ = float(myvars["initmoist"])  ## VJ 210523 was wrong initmoist_
    fillDEM = float(myvars["DEMfill"]) ### VJ 210522 was int
    

    ### ------ ALL STABDARD OPENLISEM MAPNAMES ------ ###

    buffersinName = 'zero.map'             # in m, positive valuesName = dike, negative values is basin, added to the DEM
    maskinName = 'mask0.map'               # mask to the catchment , 1 and MV
                                           # col 1=Micro roughness; 2 = manning's; 3 = plant height; 4 = cover, 5 is bulkdensity factor

    mainoutinName = 'mainout0.map'         # forced outlet rivers to the sea, because of imperfect dem

    # not used in CRC project, info dirctly from LULC map
    housecoverinName = 'zero.map'          # housing density fraction (0-1)
    hardsurfinName = 'zero.map'            # hard surfaces (0-1) such as airport, parking lots etc
    roadinName = 'zero.map'                # tarmac roads mask or type numbers

    # will be replaced by a timeseries
    #NDVIinName = 'NDVI'                    # NDVI for cover and LAI

    ### output maps ###

    # basic topography related maps
    DEMName= MapsDir+'dem.map'             # adjusted dem
    IDName= MapsDir+'id.map'               # raingauge zones, def set to 1
    IDETName= MapsDir+'idet.map'           # meteo station zones, def set to 1
    buffersName= MapsDir+'buffer.map'      # changes in m to the dem (+ or -)
    LddName= MapsDir+'ldd.map'             # Local Drain Direction for surface runoff
    gradName= MapsDir+'grad.map'           # slope, sine! (0-1)
    outletName= MapsDir+'outlet.map'       # location outlets and checkpoints
    landuseName= MapsDir+'landuse.map'     # landuse/landcover for RR and manning
    outpointName= MapsDir+'outpoint.map'   # user defined output locations
    upsName= MapsDir+'ups.map'             # cumulative flow network, not used in lisem
    wsName= MapsDir+'ws.map'               # watershed boundary map, not used in lisem
    shadeName= MapsDir+'shade.map'         # shaded relief map, not use din lisem

    # infrastructure
    roadwidthName= MapsDir+'roadwidt.map'   # road width (m)
    hardsurfName= MapsDir+'hardsurf.map'    # impermeable surfaces (0 or 1)
    housecovName= MapsDir+'housecover.map'  # house cover fraction
    roofstoreName= MapsDir+'roofstore.map'  # roof interception (mm) \
    raindrumsizeName= MapsDir+'raindrum.map'# raindrum size (m3)
    drumstoreName= MapsDir+'drumstore.map'  # locations of rainwater harvesting in drums (0/1)

    # vegetation maps
    coverName= MapsDir+'per.map'           # cover fraction (-)
    laiName= MapsDir+'lai.map'             # leaf area index (m2/m2) for interception storage
    smaxName= MapsDir+'smax.map'           # user defined canopy storage
    cropheightName= MapsDir+'ch.map'       # plant height in m, for erosion, not used
    grasswidName= MapsDir+'grasswid.map'   # width of grass strips for infiltration
    LitterName= MapsDir+'litter.map'       # fraction of litter under tree vegetation.

    # Green and Ampt infiltration maps, numbers 1 and 2 are added to the names in the script
    ksatName= MapsDir+'ksat'                # sat hydraulic conductivity (mm/h)
    poreName= MapsDir+'thetas'              # porosity (-)
    thetaiName= MapsDir+'thetai'            # initial moisture content (-)
    psiName= MapsDir+'psi'                  # suction unsat zone (cm)
    soildep1Name= MapsDir+'soildep1.map'    # soil depth (mm), assumed constant
    soildep2Name= MapsDir+'soildep2.map'    # soil depth (mm), assumed constant

    cohName= MapsDir+'coh'
    cohaddName= MapsDir+'cohadd.map'
    asName= MapsDir+'aggrstab.map'
    d50Name= MapsDir+'d50.map'
    d90Name= MapsDir+'d90.map'

    compactName= MapsDir+'compfrc.map'      # fraction of compacted siurface (0-1)
    crustName= MapsDir+'crustfrc.map'       # fraction of crusted siurface (0-1)
    ksatcompName= MapsDir+'ksatcomp.map'    # ksat of compacted areas (mm/h)
    ksatcrustName= MapsDir+'ksatcrust.map'  # ksat of crusted areas (mm/h)
    porecompName= MapsDir+'porecomp.map'    # Porosity of compacted areas (-)
    porecrustName= MapsDir+'porecomp.map'   # Porosity of crusted areas (-)

    # surface maps
    rrName= MapsDir+'rr.map'                # surface roughness (cm)
    mannName= MapsDir+'n.map'               # mannings n ()
    stoneName= MapsDir+'stonefrc.map'       # stone fraction on surface (-)
    crustName= MapsDir+'crustfrc.map'       # crusted soil (-), not present
    compName= MapsDir+'compfrc.map'         # compacted soil (-), murrum roads

    # erosion maps , not used
    cohsoilName= MapsDir+'coh.map'          # cohesion (kPa)
    cohplantName= MapsDir+'cohadd.map'      # added root cohesion (kPa)
    D50Name= MapsDir+'d50.map'              # median of texture for suspended (mu)
    D90Name= MapsDir+'d90.map'			     # 90 quantile of texture for bedload (mu)
    aggrstabName= MapsDir+'aggrstab.map'    # aggregate stability number (-)

    # channel maps
    lddchanName= MapsDir+'lddchan.map'      # channel 1D network
    chanwidthName= MapsDir+'chanwidt.map'   # channel width (m)
    changradName= MapsDir+'changrad.map'    # channel gradient, sine
    chanmanName= MapsDir+'chanman.map'      # channel manning (-)
    chansideName= MapsDir+'chanside.map'    # angle channel side walls, 0Name= MapsDir+'rectangular
    chanmaskName= MapsDir+'chanmask.map'   # copy of channel mask
    chancohName= MapsDir+'chancoh.map'      # channel cohesion (kPa)
    chandepthName= MapsDir+'chandepth.map'  # channel depth (m)
    chanmaxqName= MapsDir+'chanmaxq.map'    # maximum discharge (m3/s) in culvert locations in channel
    chanleveesName= MapsDir+'chanlevee.map' # main levees along channels
    chanksatName= MapsDir+'chanksat.map'    # ksat in case channel infiltrates, for dry channels
    baseflowName= MapsDir+'baseflow.map'    # stationary baseflow at end piints of river


    os.chdir(BaseDir)  # change to base directory, not needed?

    print(">>> read base maps from {0}".format(BaseDir),flush=True)

    setclone(BaseDir+DEMbaseName) # set the overall mask for PCRaster operations
    # now we can do map = scalar(v) and other pcrcalc stuff

    # read DEM and create mask
    DEM_ = readmap(BaseDir+DEMbaseName)
    mask_ = (DEM_*0) + scalar(1)
    report(mask_, BaseDir+masknamemap_)
    report(mask_, MapsDir+masknamemap_)
    # create maps with 0 and add to both directories
    zero_ = mask_*0
    report(zero_,MapsDir+"zero.map")
    report(zero_,BaseDir+"zero.map")
    # find user defined outlets if any, else zero and lddchan is used
    mainout_=zero_
    if doUserOutlets == 1:
        mainout_ = readmap(BaseDir+OutletsbaseName)

    #maps that are needed in multiple classes
    soildepth1depth = scalar(300)           # mm of first layer and minimal soildepth
    Ldd_ = ldd(0*mask_)
    Ksaturban_ = scalar(5)
    Poreurban_ = scalar(0.45)
    unitBuild_ = nominal(3)  # to adapt ksat pore urban areas
    unitWater_ = nominal(9)  # to adapt ksat pore water
    standardBD = scalar(standardbulkdensity_)

    Debug_ = False

    SG_names_ = ['sand','silt','clay','soc','cfvo','bdod']
    print(BaseDir+DEMbaseName)
    # get the gdal details of the mask, bounding box, rows and cols
    #print(BaseDir+DEMbaseName,flush=True)
    maskgdal=gdal.Open(BaseDir+DEMbaseName) # get mask details
    maskproj = maskgdal.GetProjection()
    maskgeotrans = maskgdal.GetGeoTransform()
    nrRows = maskgdal.RasterYSize
    nrCols = maskgdal.RasterXSize
    dx = maskgdal.GetGeoTransform()[1]
    dy = maskgdal.GetGeoTransform()[5]
    llx = maskgdal.GetGeoTransform()[0]
    ury = maskgdal.GetGeoTransform()[3]
    urx = llx + nrCols*dx
    lly = ury + dy*nrRows
    maskbox = [llx,lly,urx,ury]

    print('>>> Get land use map for the area', flush=True)
    LULCtable = lulcDir+lulcTable
    LULCmap = lulcDir+lulcTIF
    src = gdal.Open(LULCmap)
    # get ESPG number
    #ESPG = osr.SpatialReference(wkt=src.GetProjection()).GetAttrValue('AUTHORITY',1)
    ESPG = int(ESPGnumber)
    
    print(ESPG, flush=True)
    #cutout and convert
    dst = gdal.GetDriverByName('PCRaster').Create(landuseName, nrCols, nrRows, 1,
                                gdalconst.GDT_Int32,["PCRASTER_VALUESCALE=VS_NOMINAL"])
    dst.SetGeoTransform( maskgeotrans )
    dst.SetProjection( maskproj )
    gdal.ReprojectImage(src, dst, maskproj, maskproj, gdalconst.GRA_NearestNeighbour)
    dst = None
    src = None

    lun = readmap(landuseName)
    # lun = nominal(lu)
    lun = spreadzone(lun,0,1) # fill in gaps in lu map with surroundng units
    #report(lun,landuseName)

    mask_ = ifthen( boolean(mask_ == 1) & boolean(lun != 0),scalar(1))
    report(ifthen(mask_ == 1, lun),landuseName)

    if doProcessesDEM == 1 :
        print('>>> Create dem derivatives, slope, LDD', flush=True)
        staticModelDEM = StaticFramework(DEMderivatives())
        staticModelDEM.run()

    if doProcessesChannels == 1:
        print('>>> Create channel maps', flush=True)
        staticModelCH = StaticFramework(ChannelMaps())
        staticModelCH.run()

    if doProcessesLULC == 1:
        print('>>> Create surface and land use related maps', flush=True)
        staticModelSURF = StaticFramework(SurfaceMaps())
        staticModelSURF.run()


    # soil and infiltration maps
    if doProcessesSG == 1:
         # soilgrid layer rootnames: S, Si, C, soil org carbon, coarse fragments, bulk dens

        print(">>> Downloading SOILGRIDS layers and creating infiltration maps", flush=True)
        #soigrid map names for texture, doil organic carbon, course fragments, bulk dens
        #print(optionSG1,optionSG2, flush=True)
        for x in range(0,6):
            GetSoilGridsLayer(masknamemap_,ESPG,SG_names_[x],optionSG1,1)
        for x in range(0,6):
            GetSoilGridsLayer(masknamemap_,ESPG,SG_names_[x],optionSG2,2)


    if doProcessesInFil == 1:
        staticModel = StaticFramework(PedoTransfer())
        layer_ = 1
        staticModel.run()
        layer_ = 2
        staticModel.run()

    print("Done")

# 		rr	n	height
# 	0	1	2	3
# 1- Deciduous Broadleaf Forest	1	2	0.05	10
# 2- Cropland	2	1	0.04	1.5
# 3- Built-up Land	3	0.5	0.1	8
# 4- Mixed Forest	4	2	0.1	10
# 5- Shrubland	5	2	0.08	5
# 6- Barren Land	6	1	0.035	0.2
# 7- Fallow Land	7	1	0.05	0.1
# 8- Wasteland	8	1	0.05	0.1
# 9- Water Bodies	9	0.5	0.01	0
# 10- Plantations	10	1.5	0.05	8
# 11- Aquaculture	11	1	0.06	0.5
# 12- Mangrove Forest	12	2	0.09	8
# 13- Salt Pan	13	0.5	0.03	0
# 14- Grassland	14	1	0.1	0.5
# 15- Evergreen Broadleaf Forest	15	2	0.1	12
# 16- Deciduous Needleleaf Forest	16	2	0.09	12
# 17- Permanent Wetlands	17	1	0.1	1
# 18- Snow & Ice	18	1	0.03	0
# 19- Evergreen Needleleaf Forest	19	2	0.09	10