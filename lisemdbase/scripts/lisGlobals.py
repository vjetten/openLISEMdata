# lisemDBASEgenerator
# global vraiables and initialisation
#
# author: V.G.Jetten @ 2022
# University of Twente, Faculty ITC
# this software has copyright model: GPLV3
# this software has a disclaimer


from osgeo import gdal, gdalconst, osr
from pcraster import *
from pcraster.framework import *
import time,sys         # read commandline arguments
import os   

def initialize():
    global Debug_ 
    
    #default values for interface options
    global doProcessesDEM
    global doProcessesChannels
    global doProcessesInfil
    global doProcessesSG
    global doProcessesLULC
    global doProcessesNDVI
    global doProcessesErosion
    global doProcessesDams
    global doUseCulverts
    global doChannelsNoEros
    global doCatchment
    global doProcessesSGInterpolation
    global doProcessesSGAverage
    global doProcessesInfrastructure
    global doProcessesStormdrain
    global doProcessesRain    
    global optionD50
    global optionSG1
    global optionSG2
    global chWidth
    global chWidthS
    global chB
    global chC
    global chN
    global chDepth
    global chDepthS
    global chBaseflow
    global doCorrectDEM
    global doUserOutlets
    global doPruneBranch
    global optionResample
    global useBulkdensity
    global useLUdensity
    global useNoGravel
    global standardbulkdensity_ 
    global initmoisture_
    global rootzone
    global maxSoildepth
    global useCorrOM
    global CorrOM
    global roofStore
    global useCorrText
    global CorrClay
    global CorrSilt
    global CorrSand
    global tileDiameter
    global tileHeight
    global tileWidth
    global drainInletDistance
    global drainInletSize
    
    ### input maps ###
    global condaDir
    global MapsDir
    global BaseDir
    global DEMbaseName
    global riversbaseName
    global outletsbaseName
    global outpointsbaseName
    global culvertsbaseName
    global damsbaseName
    global masknamemap_ 
    global lulcTIF
    global NDVIinName
    global LULCtable
    global buffersinName 
    global maskinName 
    global mainoutinName 
    global housecoverinName #!!!!!!!!!
    global hardsurfinName 
    global roadinName
    global roadsSHPName
    global buildingsSHPName
    
    global fillDEM
    global catchmentsize
    global EPSGnumber
    global layer_
    global mapnr_
    global shapeNr
    global optionSplash


    ### ------ ALL STANDARD OPENLISEM MAPNAMES ------ ###

    
    # will be replaced by a timeseries
    #NDVIinName 

    ### output maps ###

    # basic topography related maps
    global DEMName
    global IDName
    global IDETName
    global buffersName
    global LddName
    global gradName
    global outletName
    global landuseName
    global outpointName
    global upsName
    global wsName
    global shadeName
    global lddbaseName
    global basereachName

    # infrastructure
    global roadwidthName
    global hardsurfName
    global housecovName
    global roofstoreName
    global raindrumsizeName
    global drumstoreName

    # vegetation maps
    global coverName
    global laiName
    global smaxName
    global cropheightName
    global grasswidName
    global LitterName 
    global NDVIName 

    # Green and Ampt infiltration maps, numbers 1 and 2 are added to the names in the script
    global ksatName
    global poreName
    global thetaiName
    global psiName
    global soildep1Name
    global soildep2Name

    global cohName
    global cohaddName
    global asName
    global d50Name
    global d90Name

    global compactName
    global crustName
    global ksatcompName
    global ksatcrustName
    global porecompName
    global porecrustName

    # surface maps
    global rrName
    global mannName
    global plantHeightName
    global stoneName
    global crustName
    global compName

    # erosion maps , not used
    global cohsoilName
    global cohplantName
    global D50Name
    global D90Name
    global aggrstabName
    global landunitName

    # channel maps
    global lddchanName
    global chanwidthName
    global changradName
    global chanmanName
    global chansideName
    global chanmaskName
    global chancohName
    global chandepthName
    global chanmaxqName
    global chanleveesName
    global chanksatName
    global baseflowName
    
    global lddtileName
    global tilemaskName
    global tilemanName
    global tilediameterName
    global tilegradName
    global tileinletName
    global tileheightName
    global tilewidthName

    
    global DEM_
    global mask_
    global rivers_
    global mainout_
    global mainoutpoint_ 
    global DAMS_
    global zero_
    global soildepth1depth
    global soildepth2depth
    global watersheds_
    
    global maskgdal
    global maskproj 
    global maskgeotrans 
    global nrRows 
    global nrCols 
    global dx 
    global dy 
    global llx 
    global ury 
    global urx 
    global lly 
    global maskbox 
    global EPSG
    global lun
    
    global SG_names_
    global SG_layers_
    global SG_mapnr_
    global SG_horizon_
    
    global conversionmmh
    global timeinterval
    global IPoption
    global optionGaugeGPM
    global rainInputdir 
    global rainOutputdir 
    global rainMaskmapname
    global rainfilename
    global rainPointmapname
    global rainPointnameIn 
    global rainEPSG
    global rainString
    global riverExists
    
   
    #default values for interface options
    condaDir = "c:/"
    doProcessesDEM = 1
    doProcessesChannels = 1
    doProcessesInfil = 1
    doProcessesSG = 1
    doProcessesLULC = 1
    doProcessesNDVI = 0
    doProcessesErosion = 1
    doProcessesDams = 1
    doChannelsNoEros = 1
    doCatchment = 0
    doProcessesSGInterpolation = 1
    doProcessesSGAverage = 0
    doProcessesInfrastructure = 0
    doProcessesStormdrain = 0
    doProcessesRain = 0
    optionD50 = 0
    optionSG1 = 2
    optionSG2 = 4    
    optionResample = 1
    chWidth = 500.0
    chWidthS = 2.0
    chB = 0.459  #=1/2.18
    chC = 0.300
    chN = 0.05
    chDepth = 5.0
    chDepthS = 1.0
    chBaseflow = 0.0
    doCorrectDEM = 0
    doUserOutlets = 0  ## VJ 210523  added options user defined outlets that are forced in the DEM
    doPruneBranch = 0
    useBulkdensity = 1
    #useBulkdensity2 = 0
    useLUdensity = 0
    useNoGravel = 0    
    standardbulkdensity_ = 1350.0
    #standardbulkdensity2_ = 1350.0
    initmoisture_ = 0.0
    rootzone = 0.6
    maxSoildepth = 5.0
    useCorrOM = 0
    CorrOM = 0.0
    useCorrText = 0
    CorrClay = 0.0
    CorrSilt = 0.0
    CorrSand = 0.0
    shapeNr = 1
    roofStore = 1.0
    tileDiameter = 0.65
    tileHeight = 0.5
    tileWidth = 0.5
    drainInletDistance = 30
    drainInletSize = 0.5
    
    
    optionSplash = 1
    conversionmmh = 0.1
    timeinterval = 30
    IPoption = 1
    optionGaugeGPM  = 0
    
    MapsDir = "/Maps"
    BaseDir = "/Base"
    #lulcDir = "/lulc"
    DEMbaseName = "dem0.map"
    riversbaseName = "chanmask0.map"
    outletsbaseName = "outlet0.map"    
    outpointsbaseName = "outpoints0.map"    
    culvertsbaseName = "chanmaxq0.map"    
    damsbaseName = "dams0.map"
    masknamemap_ = "mask0.map"
    #rainMaskmapname = "dem0.map"
    rainPointmapname = ""
    rainPointnameIn = ""
    rainEPSG = ""
    rainString = ""
    riverExists = False

    lulcTIF = "lulc.tif"
    NDVIinName = "ndvi.tif"
    
    LULCtable = "lulc.tbl"
    fillDEM = 10  # use fill dem with lddcreatedem, if doCorrectDEM = 0 then this is not used
    catchmentsize_ = 1e6
    EPSGnumber = ""

    ### ------ GET INTERFACE OPTIONS ------ ###
    # Read options input file generated by the UI interface
    # file has the name=value format, all strings

    # debug
   # print(sys.argv[0:])
   # print(len(sys.argv))
   # if len(sys.argv) < 2:
   #    print("no config file loaded")
   #    sys.exit()

    # read init file in test array myvars
    myvars = {}
  #  with open(sys.argv[1], 'r') as myfile:
  #      for line in myfile:
  #          if '=' not in line:
  #              continue
  #          S0 = (line.split('='))[0].strip()
  #          S1 = (line.split('='))[1].strip()
  #          myvars[S0] = S1
  #          if S0.comtains("RainString"):
  #              S1 = "_" + S1
            
    with open(sys.argv[1], 'r') as myfile:
        for line in myfile:
            if '=' not in line:
                continue
            parts = line.split('=')
            S0 = parts[0].strip()
            S2 = '='.join(parts[1:]).strip()  # Rejoin the parts in case '=' appears multiple times
            S1 = S2
            if S2.startswith('$'):
                S1 = S2[1:]
            myvars[S0] = S1            
            
    condaDir =myvars["CondaDirectory"]
    BaseDir = myvars["BaseDirectory"]
    MapsDir = myvars["MapsDirectory"]
    EPSGnumber = myvars["ESPGnumber"]

    DEMbaseName = myvars["BaseDEM"]
    riversbaseName = myvars["BaseChannel"]
    outletsbaseName = myvars["BaseOutlets"]
    outpointsbaseName = myvars["BaseOutpoints"]
    culvertsbaseName = myvars["BaseCulverts"]
    doUseCulverts = int(myvars["optionUseCulverts"])

    doProcessesDEM = int(myvars["optionDEM"])
    #doCatchment = int(myvars["optionCatchments"])
    #catchmentsize_ = float(myvars["CatchmentSize"]) 
    doCorrectDEM = int(myvars["optionFillDEM"])
    fillDEM = float(myvars["DEMfill"])
    
    doProcessesChannels = int(myvars["optionChannels"])
    #doPruneBranch = int(myvars["optionPruneBranch"])

    doProcessesDams = int(myvars["optionIncludeDams"])
    damsbaseName = myvars["BaseDams"]
    doUserOutlets = int(myvars["optionUserOutlets"])
    chWidth = float(myvars["chWidth"])
    chWidthS = float(myvars["chWidthS"])
    chDepth = float(myvars["chDepth"])
    chDepthS = float(myvars["chDepthS"])
    chB = float(myvars["chB"]) 
    chC = float(myvars["chC"]) 
    chN = float(myvars["chN"]) 
    chBaseflow = float(myvars["chBaseflow"]) 
    outletstableName = myvars["Outletstable"]
    watershedsName = myvars["Watersheds"]

    doProcessesLULC = int(myvars["optionLULC"])
    lulcTIF = myvars["LULCmap"]
    LULCtable = myvars["LULCNNtable"]
    doProcessesNDVI = int(myvars["optionUseNDVI"])
    NDVIinName = myvars["NDVImap"]

    doProcessesInfil = int(myvars["optionInfil"])
    doProcessesSG = int(myvars["optionSG"])
    optionSG1 = int(myvars["optionSG1"])+1
    optionSG2 = int(myvars["optionSG2"])+1
    doProcessesSGInterpolation = int(myvars["optionSGInterpolation"])
    #doProcessesSGAverage = int(myvars["optionSGAverage"])
    optionResample = int(myvars["optionResample"])
    #useBulkdensity = int(myvars["optionUseBD"])
    #useBulkdensity2 = int(myvars["optionUseBD2"])
    useLUdensity = int(myvars["optionUseDensity"])
    useNoGravel = int(myvars["optionNoGravel"])
    standardbulkdensity_ = float(myvars["refBulkDens"])
    #standardbulkdensity2_ = float(myvars["refBulkDens2"])
    rootzone = float(myvars["refRootzone"]) 
    maxSoildepth = float(myvars["refMaxSoildepth"]) 
    initmoisture_ = float(myvars["initmoist"])  
    useCorrOM = int(myvars["optionUseCorrOM"])
    CorrOM = float(myvars["corrOM"])  
    useCorrText = int(myvars["optionUseCorrTexture"])
    CorrClay = float(myvars["corrClay"])  
    CorrSilt = float(myvars["corrSilt"])  
    CorrSand = float(myvars["corrSand"])  
    
    doProcessesErosion = int(myvars["optionErosion"])
    doChannelsNoEros = int(myvars["optionChannelsNoEros"])
    optionD50 = int(myvars["optionD50"])
    optionSplash = int(myvars["optionSplash"])

    doProcessesInfrastructure = int(myvars["optionUseInfrastructure"])
    buildingsSHPName = myvars["buildingsSHPName"]
    roofStore = float(myvars["roofStore"])
    roadsSHPName = myvars["roadsSHPName"]
    doProcessesStormdrain = int(myvars["optionUseStormDrain"])    
    tileDiameter= float(myvars["DrainDiameter"])
    tileHeight= float(myvars["DrainHeight"])
    tileWidth= float(myvars["DrainWidth"])
    drainInletDistance= float(myvars["DrainInletDistance"])
    drainInletSize= float(myvars["DrainInletSize"])
            
    doProcessesRain = int(myvars["optionRain"])
    rainInputdir = myvars["RainBaseDirectory"]
    rainOutputdir = myvars["RainDirectory"]
    #rainMaskmapname  = myvars["RainRefNameDEM"]
    rainEPSG = myvars["RainEPSG"]
    rainString = myvars["RainString"]
    rainfilename = myvars["RainFilename"]
    conversionmmh = float(myvars["conversionmm"])
    timeinterval = float(myvars["timeinterval"])
    IPoption = float(myvars["interpolation"])
    optionGaugeGPM = float(myvars["SelectPointfromGPM"])
    
    if optionGaugeGPM == 1:
        rainPointmapname = myvars["RainGaugeFilename"]
        rainPointnameIn = myvars["RainGaugeFilenameIn"]
    
    # main options determine the suboptions:
    if doProcessesInfil == 0 :
        useBulkdensity = 0
    if doProcessesErosion == 0 :
        optionD50 = 0
    if doProcessesDEM == 0:
        doCorrectDEM = 0
    if doProcessesChannels == 0:
        doPruneBranch = 0
        doProcessesDams = 0
        

    ### ------ ALL STANDARD OPENLISEM MAPNAMES ------ ###

    buffersinName = 'buffers0.map'         # in m, positive is barries, negative values is basin, added to the DEM
    maskinName = 'mask0.map'               # mask to the catchment , 1 and MV
    mainoutinName = 'mainout0.map'         # outlet of rivers, because of imperfect dem

    # placeholders for when shapefiles are not used
    housecoverinName = 'zero.map'          # housing density fraction (0-1)
    hardsurfinName = 'zero.map'            # hard surfaces (0-1) such as airport, parking lots etc
    roadinName = 'zero.map'                # tarmac roads mask or type numbers

    # will be replaced by a timeseries
    #NDVIinName = 'NDVI'                    # NDVI for cover and LAI

    ### output maps ###

    # basic topography related maps
    DEMName= MapsDir+'dem.map'             # adjusted dem
    IDName= MapsDir+'ID.map'               # raingauge zones, def set to 1
    IDETName= MapsDir+'ETID.map'           # meteo station zones, def set to 1
    buffersName= MapsDir+'buffers.map'      # changes in m to the dem (+ or -)
    LddName= MapsDir+'ldd.map'             # Local Drain Direction for surface runoff
    gradName= MapsDir+'grad.map'           # slope, sine! (0-1)
    outletName= MapsDir+'outlet.map'       # location outlets and checkpoints
    landuseName= MapsDir+'landuse.map'     # landuse/landcover for RR and manning
    outpointName= MapsDir+'outpoint.map'   # user defined output locations
    upsName= MapsDir+'ups.map'             # cumulative flow network, not used in lisem
    wsName= MapsDir+'ws.map'               # watershed boundary map, not used in lisem
    shadeName= MapsDir+'shade.map'         # shaded relief map, not use din lisem
    lddbaseName= MapsDir+'lddbaseflow.map'
    basereachName= MapsDir+'basedistance.map'

    # infrastructure
    roadwidthName= MapsDir+'roadwidt.map'   # road width (m)
    hardsurfName= MapsDir+'hardsurf.map'    # impermeable surfaces (0 or 1)
    housecovName= MapsDir+'housecover.map'  # house cover fraction
    roofstoreName= MapsDir+'roofstore.map'  # roof interception (mm) \
    raindrumsizeName= MapsDir+'raindrum.map'# raindrum size (m3)
    drumstoreName= MapsDir+'drumstore.map'  # locations of rainwater harvesting in drums (0/1)
    lddtileName     = MapsDir+'lddtile.map'     
    tilemaskName    = MapsDir+'tilemask.map'
    tilemanName     = MapsDir+'tileman.map'
    tilediameterName= MapsDir+'tilediameter.map'
    tilegradName    = MapsDir+'tilegrad.map'
    tileinletName   = MapsDir+'tileinlet.map' 
    tileheightName   = MapsDir+'tileheight.map' 
    tilewidthName   = MapsDir+'tilewidth.map' 

    # vegetation maps
    coverName= MapsDir+'per.map'           # cover fraction (-)
    laiName= MapsDir+'lai.map'             # leaf area index (m2/m2) for interception storage
    smaxName= MapsDir+'smax.map'           # user defined canopy storage
    cropheightName= MapsDir+'ch.map'       # plant height in m, for erosion, not used
    grasswidName= MapsDir+'grasswid.map'   # width of grass strips for infiltration
    LitterName = MapsDir+'litter.map'       # fraction of litter under tree vegetation.
    NDVIName = MapsDir+'NDVI.map'

    # Green and Ampt infiltration maps, numbers 1 and 2 are added to the names in the script
    ksatName= MapsDir+'ksat'                # sat hydraulic conductivity (mm/h)
    poreName= MapsDir+'thetas'              # porosity (-)
    thetaiName= MapsDir+'thetai'            # initial moisture content (-)
    psiName= MapsDir+'psi'                  # suction unsat zone (cm)
    soildep1Name= MapsDir+'soildep1.map'    # soil depth (mm), assumed constant
    soildep2Name= MapsDir+'soildep2.map'    # soil depth (mm), assumed constant

    cohName= MapsDir+'coh.map'
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
    compName= MapsDir+'compfrc.map'         # compacted soil (-), compacted roads

    # erosion maps
    cohsoilName= MapsDir+'coh.map'          # cohesion (kPa)
    cohplantName= MapsDir+'cohadd.map'      # added root cohesion (kPa)
    D50Name= MapsDir+'d50.map'              # median of texture for suspended (mu)
    D90Name= MapsDir+'d90.map'			    # 90% quantile of texture for bedload (mu)
    aggrstabName= MapsDir+'aggrstab.map'    # aggregate stability number (-)
    landunitName= MapsDir+'landunit.map'    # landuse/landcover for RR and manning
    plantHeightName=MapsDir+'ch.map'        # plant height (m)

    # channel maps
    lddchanName= MapsDir+'lddchan.map'      # channel 1D network
    chanwidthName= MapsDir+'chanwidt.map'   # channel width (m)
    changradName= MapsDir+'changrad.map'    # channel gradient, sine
    chanmanName= MapsDir+'chanman.map'      # channel manning (-)
    chansideName= MapsDir+'chanside.map'    # angle channel side walls, 0Name= MapsDir+'rectangular
    chanmaskName= MapsDir+'chanmask.map'    # copy of channel mask
    chancohName= MapsDir+'chancoh.map'      # channel cohesion (kPa)
    chandepthName= MapsDir+'chandepth.map'  # channel depth (m)
    chanmaxqName= MapsDir+'chanmaxq.map'    # maximum discharge (m3/s) in culvert locations in channel
    chanleveesName= MapsDir+'chanlevee.map' # main levees along channels
    chanksatName= MapsDir+'chanksat.map'    # ksat in case channel infiltrates, for dry channels
    baseflowName= MapsDir+'baseflow.map'    # stationary baseflow at end piints of river

    if not os.path.exists(MapsDir) :
        os.makedirs(MapsDir)
        
    os.chdir(BaseDir)  # change to base directory, not needed?

    print(">>> Reading base maps from {0}".format(BaseDir),flush=True)
    #print(">>> Reading base maps from {0}".format(useCorrText),flush=True)

    setclone(BaseDir+DEMbaseName) # set the overall mask for PCRaster operations
    # now we can do map = scalar(v) and other pcrcalc stuff

    rainMaskmapname = DEMbaseName

    # read base maps and create mask
    DEM_ = readmap(BaseDir+DEMbaseName)
    mask_ = (DEM_*0) + scalar(1)
    riverExists = os.path.isfile(BaseDir+riversbaseName)
    #isDirectory = os.path.dir(BaseDir+riversbaseName)
    if riverExists :
        rivers_ = readmap(BaseDir+riversbaseName)   
    else:
        rivers_ = 0*mask_
        
    mainout_ = scalar(readmap(BaseDir+outletsbaseName))
    mainoutpoint_ = scalar(readmap(BaseDir+outpointsbaseName))
    DAMS_= DEM_*0
       
    report(mask_, BaseDir+masknamemap_)
    report(mask_, MapsDir+masknamemap_)
    # create maps with 0 and 1 and add to both directories
    zero_ = mask_*0
    report(zero_,MapsDir+"zero.map")
    report(zero_,BaseDir+"zero.map")
    
    # find user defined outlets if any, else zero and lddchan is used
    watersheds_ = mask_
    if doUserOutlets == 1:
       watersheds_ = scalar(readmap(watershedsName))
       

    #maps that are needed in multiple classes
    soildepth1depth = rootzone*1000           # mm of first layer and minimal soildepth
    soildepth2depth = maxSoildepth*1000           # mm of first layer and minimal soildepth
    Ldd_ = ldd(0*mask_)
    
    Debug_ = False

    SG_names_ = ['sand','silt','clay','soc','cfvo','bdod']
    SG_layers_ =['_0-5cm_mean','_5-15cm_mean','_15-30cm_mean','_30-60cm_mean','_60-100cm_mean','_100-200cm_mean']
    
    #print(BaseDir+DEMbaseName)
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
    EPSG = int(EPSGnumber)
    
    # read landuse maps and/or NDVI and cur to size    
    if doProcessesLULC == 1:
        print('>>> Creating PCRaster land use map for area: '+landuseName, flush=True)
        LULCmap = lulcTIF 
        src = gdal.Open(LULCmap)
        #cutout and convert
        dst = gdal.GetDriverByName('PCRaster').Create(landuseName, nrCols, nrRows, 1,
                                    gdalconst.GDT_Int32,["PCRASTER_VALUESCALE=VS_NOMINAL"])
        dst.SetGeoTransform( maskgeotrans )
        dst.SetProjection( maskproj )
        gdal.ReprojectImage(src, dst, maskproj, maskproj, gdalconst.GRA_NearestNeighbour)
        dst = None
        src = None
        lun = readmap(landuseName)
        lun = spreadzone(lun,0,1) # fill in gaps in lu map with surroundng units 
        report(ifthen(mask_ == 1, lun),landuseName)
        report(ifthen(mask_ == 1, lun),landunitName)
        
        if doProcessesNDVI == 1:               
            src = gdal.Open(NDVIinName)
            #cutout and convert
            dst = gdal.GetDriverByName('PCRaster').Create(NDVIName, nrCols, nrRows, 1,
                                        gdalconst.GDT_Float32,["PCRASTER_VALUESCALE=VS_SCALAR"])
            dst.SetGeoTransform( maskgeotrans )
            dst.SetProjection( maskproj )
            gdal.ReprojectImage(src, dst, maskproj, maskproj, gdalconst.GRA_NearestNeighbour)
            dst = None
            src = None    
    
