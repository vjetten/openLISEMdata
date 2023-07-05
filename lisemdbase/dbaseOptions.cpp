#include "mainwindow.h"

void MainWindow::setIniStart()
{
    QSettings settings(qApp->applicationDirPath()+"/lisemdbase.ini",QSettings::IniFormat);
    settings.clear();
    for (int i = 0; i < combo_iniName->count(); i++) {
        settings.setValue(QString(i),combo_iniName->itemText(i));
    }
}

void MainWindow::getIniStart()
{
    QSettings settings(qApp->applicationDirPath()+"/lisemdbase.ini",QSettings::IniFormat);
    settings.sync();
    QStringList keys = settings.allKeys();
    QStringList skeys;
    for (int i = 0; i < keys.size(); i++) {
        QString s = settings.value(QString(i)).toString();
        if (QFileInfo(s).exists())
            skeys << s;
    }
    skeys.removeDuplicates();
    combo_iniName->addItems(skeys);
}

void MainWindow::setIni(QString sss, bool yes)
{
    QSettings settings(sss,QSettings::IniFormat);
    settings.clear();
    settings.sync();

    settings.setValue("CondaDirectory", CondaBaseDirName);
    settings.setValue("Script", ScriptFileName);
    settings.setValue("BaseDirectory", BaseDirName);
    settings.setValue("MapsDirectory", MapsDirName);
    settings.setValue("ESPGnumber", ESPGnumber);

    settings.setValue("BaseDEM", BaseDEMName);
    settings.setValue("BaseChannel", BaseChannelName);
    settings.setValue("BaseOutlets", BaseOutletsName);
    settings.setValue("BaseOutpoints",  BaseOutpointsName);

    settings.setValue("DEM/optionDEM",QString::number(optionDEM));
    settings.setValue("DEM/optionCatchments", QString::number(optionCatchments));
//    settings.setValue("DEM/CatchmentSize", QString::number(CatchmentSize, 'f', 2));
    settings.setValue("DEM/optionFillDEM", QString::number(optionFillDEM));
    settings.setValue("DEM/DEMfill", QString::number(DEMfill, 'f', 2));

    settings.setValue("CHANNEL/optionChannels", QString::number(optionChannels));
    settings.setValue("CHANNEL/BaseCulverts",  BaseCulvertsName);
    settings.setValue("CHANNEL/optionUseCulverts", QString::number(optionUseCulverts));
    settings.setValue("CHANNEL/optionPruneBranch", QString::number(optionPruneBranch));
    settings.setValue("CHANNEL/optionIncludeDams", QString::number(optionIncludeDams));
    settings.setValue("CHANNEL/BaseDams", BaseDamsName);
    settings.setValue("CHANNEL/optionUserOutlets", QString::number(optionUserOutlets));  //0=1 outlet, >0 is multiple
    settings.setValue("CHANNEL/chWidth", QString::number(chWidth, 'f', 2));
    settings.setValue("CHANNEL/chWidthS", QString::number(chWidthS, 'f', 2));
    settings.setValue("CHANNEL/chB", QString::number(chB, 'f', 3));
    settings.setValue("CHANNEL/chDepth", QString::number(chDepth, 'f', 2));
    settings.setValue("CHANNEL/chDepthS", QString::number(chDepthS, 'f', 2));
    settings.setValue("CHANNEL/chC", QString::number(chC, 'f', 3));
    settings.setValue("CHANNEL/chBaseflow", QString::number(chBaseflow, 'f', 3));
    settings.setValue("CHANNEL/chN", QString::number(chN, 'f', 3));
    settings.setValue("CHANNEL/Outletstable", OutletstableName);
    settings.setValue("CHANNEL/Watersheds", WatershedsName);

    settings.setValue("LULC/optionLULC", QString::number(optionLULC));
    settings.setValue("LULC/LULCmap", LULCmapName);
    if (yes)
        settings.setValue("LULC/LULCNNtable", LULCNNtableName);
    else
        settings.setValue("LULC/LULCtable", LULCtableName);
    settings.setValue("LULC/NDVImap", NDVImapName);
    settings.setValue("LULC/optionUseNDVI", QString::number(optionUseNDVI));

    settings.setValue("SOIL/optionInfil", QString::number(optionInfil));
    settings.setValue("SOIL/optionSG", QString::number(optionSG)); // do soilgrids
    settings.setValue("SOIL/optionSG1", QString::number(SG1));
    settings.setValue("SOIL/optionSG2", QString::number(SG2));
    settings.setValue("SOIL/optionSGInterpolation", QString::number(optionSGInterpolation)); // do soilgrids
    settings.setValue("SOIL/optionResample", QString::number(optionResample)); // do soilgrids

    //settings.setValue("SOIL/optionSGAverage", QString::number(optionSGAverage)); // do soilgrids
    settings.setValue("SOIL/optionNoGravel", QString::number(optionNoGravel)); // do soilgrids
    settings.setValue("SOIL/optionUseBD", QString::number(optionUseBD));
    settings.setValue("SOIL/optionUseCorrOM", QString::number(optionUseCorrOM));
    settings.setValue("SOIL/corrOM", QString::number(corrOM, 'f', 2));
    settings.setValue("SOIL/optionUseCorrTexture", QString::number(optionUseCorrTexture));
    settings.setValue("SOIL/corrClay", QString::number(corrClay, 'f', 2));
    settings.setValue("SOIL/corrSilt", QString::number(corrSilt, 'f', 2));
    settings.setValue("SOIL/corrSand", QString::number(corrSand, 'f', 2));
    settings.setValue("SOIL/optionUseDensity", QString::number(optionUseDensity));
    settings.setValue("SOIL/refBulkDens", QString::number(refBulkDens, 'f', 0));
    //settings.setValue("SOIL/optionUseBD2", QString::number(optionUseBD2));
    //settings.setValue("SOIL/refBulkDens2", QString::number(refBulkDens2, 'f', 0));
    settings.setValue("SOIL/refRootzone", QString::number(refRootzone, 'f', 2));
    settings.setValue("SOIL/refMaxSoildepth", QString::number(refMaxSoildepth, 'f', 2));
    settings.setValue("SOIL/initmoist", QString::number(initmoist, 'f', 2));

    settings.setValue("EROSION/optionErosion", QString::number(optionErosion));
    settings.setValue("EROSION/optionSplash", QString::number(optionSplash));
    settings.setValue("EROSION/optionD50", QString::number(optionD50));
    settings.setValue("EROSION/optionChannelsNoEros", QString::number(optionChannelsNoEros));

    settings.setValue("INFRA/optionUseInfrastructure", QString::number(optionUseInfrastructure));
    settings.setValue("INFRA/buildingsSHPName", buildingsSHPName);
    settings.setValue("INFRA/drumMap", drummapName);
    settings.setValue("INFRA/optionUseDrums", QString::number(optionUseDrums));
    settings.setValue("INFRA/roadsSHPName", roadsSHPName);
    settings.setValue("INFRA/roofStore", QString::number(roofStore, 'f', 1));

    settings.setValue("RAINFALL/optionRain", QString::number(optionRain));
  //  settings.setValue("RAINFALL/RainScript", RainScriptFileName);
    settings.setValue("RAINFALL/RainRefNameDEM", BaseDEMName);//RainRefNameDEM);
    settings.setValue("RAINFALL/RainBaseDirectory", RainBaseDirName);
    settings.setValue("RAINFALL/RainDirectory", RainDirName);
    settings.setValue("RAINFALL/RainFilename", RainFilename);
    settings.setValue("RAINFALL/RainEPSG", RainEPSG);
    for (int i=0; i < comboBox_rainString->count(); i++) {
        settings.setValue(QString("RAINFALL/RainString_%1").arg(i), comboBox_rainString->itemText(i));
    }
    settings.setValue("RAINFALL/RainString", RainString);
    settings.setValue("RAINFALL/SelectPointfromGPM", QString::number(optionGaugeGPM));
    settings.setValue("RAINFALL/RainGaugeFilename", RainGaugeFilename);
    settings.setValue("RAINFALL/RainGaugeFilenameIn", RainGaugeFilenameIn);
  //  settings.setValue("RAINFALL/IDMScript", IDMScriptFileName);
    settings.setValue("RAINFALL/IDMFilename", IDMFilename);
    settings.setValue("RAINFALL/RainFilenameHourIDM", RainFilenameHourIDM);
    settings.setValue("RAINFALL/dailyA", dailyA);
    settings.setValue("RAINFALL/dailyB", dailyB);
    settings.setValue("RAINFALL/day0", day0);
    settings.setValue("RAINFALL/dayn", dayn);
    settings.setValue("RAINFALL/30min", dt30min);
    settings.setValue("RAINFALL/conversionmm", QString::number(conversionmm, 'f', 2));
    settings.setValue("RAINFALL/timeinterval", QString::number(timeintervalGPM, 'f', 2));
    settings.setValue("RAINFALL/interpolation", QString::number(interpolationGPM, 'f', 2));
   // settings.setValue("RAINFALL/ERAScript", ERAScriptFileName);
    settings.setValue("RAINFALL/ERAFilename", ERAFilename);
    settings.setValue("RAINFALL/RainFilenameHourERA", RainFilenameHourERA);

    settings.sync();
}

QString MainWindow::checkName(int i, QString name)
{
    QString s = BaseDirName;
    if (i == 0)
        s = "";
    if (name.isEmpty())
        return("");

    if (!QFileInfo(s+name).exists())
        return("");

    return(name);
}

void MainWindow::getIni(QString name)
{
    QSettings settings(name,QSettings::IniFormat);
    settings.sync();

    CondaBaseDirName = checkName(0,settings.value("CondaDirectory").toString());

    ScriptFileName = checkName(0,settings.value("Script").toString());

    BaseDirName = checkName(0,settings.value("BaseDirectory").toString());
    MapsDirName = checkName(0,settings.value("MapsDirectory").toString());
    ESPGnumber = settings.value("ESPGnumber").toString();

    BaseDEMName = checkName(1,settings.value("BaseDEM").toString());
    BaseChannelName = checkName(1,settings.value("BaseChannel").toString());
    BaseOutletsName = checkName(1,settings.value("BaseOutlets").toString());
    BaseOutpointsName = checkName(1,settings.value("BaseOutpoints").toString());

    optionDEM = settings.value("DEM/optionDEM").toInt();
    optionCatchments = settings.value("DEM/optionCatchments").toInt();
    //CatchmentSize = settings.value("DEM/CatchmentSize").toDouble();
    optionFillDEM = settings.value("DEM/optionFillDEM").toInt();
    DEMfill = settings.value("DEM/DEMfill").toDouble();

    optionChannels = settings.value("CHANNEL/optionChannels").toInt();
    BaseCulvertsName = checkName(1,settings.value("CHANNEL/BaseCulverts").toString());
    optionUseCulverts = settings.value("CHANNEL/optionUseCulverts").toInt();
    optionPruneBranch = settings.value("CHANNEL/optionPruneBranch").toInt();
    optionIncludeDams = settings.value("CHANNEL/optionIncludeDams").toInt();
    BaseDamsName = checkName(1,settings.value("CHANNEL/BaseDams").toString());
    optionUserOutlets = settings.value("CHANNEL/optionUserOutlets").toInt();
    chWidth = settings.value("CHANNEL/chWidth").toDouble();
    chWidthS = settings.value("CHANNEL/chWidthS").toDouble();
    chB = settings.value("CHANNEL/chB").toDouble();
    chDepth = settings.value("CHANNEL/chDepth").toDouble();
    chDepthS = settings.value("CHANNEL/chDepthS").toDouble();
    chC = settings.value("CHANNEL/chC").toDouble();
    chN = settings.value("CHANNEL/chN").toDouble();
    chBaseflow = settings.value("CHANNEL/chBaseflow").toDouble();
    OutletstableName = settings.value("CHANNEL/Outletstable").toString();
    WatershedsName = settings.value("CHANNEL/Watersheds").toString();

    optionLULC = settings.value("LULC/optionLULC").toInt();
    LULCmapName = checkName(0,settings.value("LULC/LULCmap").toString());
    LULCtableName = checkName(0,settings.value("LULC/LULCtable").toString());
    NDVImapName = checkName(0,settings.value("LULC/NDVImap").toString());
    optionUseNDVI = settings.value("LULC/optionUseNDVI").toInt();

    optionInfil = settings.value("SOIL/optionInfil").toInt();
    optionSG = settings.value("SOIL/optionSG").toInt();
    SG1 = settings.value("SOIL/optionSG1").toInt();
    SG2 = settings.value("SOIL/optionSG2").toInt();
    optionSGInterpolation = settings.value("SOIL/optionSGInterpolation").toInt();
    optionResample = settings.value("SOIL/optionResample").toInt();
    //optionSGAverage = settings.value("SOIL/optionSGAverage").toInt();
    optionNoGravel = settings.value("SOIL/optionNoGravel").toInt();
    optionUseBD = 1;//settings.value("SOIL/optionUseBD").toInt();
    optionUseCorrOM = settings.value("SOIL/optionUseCorrOM").toInt();
    corrOM = settings.value("SOIL/corrOM").toDouble();
    optionUseCorrTexture = settings.value("SOIL/optionUseCorrTexture").toInt();
    corrClay = settings.value("SOIL/corrClay").toDouble();
    corrSilt = settings.value("SOIL/corrSilt").toDouble();
    corrSand = settings.value("SOIL/corrSand").toDouble();
    optionUseDensity = settings.value("SOIL/optionUseDensity").toInt();
    refBulkDens = settings.value("SOIL/refBulkDens").toDouble();
    //optionUseBD2 = settings.value("SOIL/optionUseBD2").toInt();
    //refBulkDens2 = settings.value("SOIL/refBulkDens2").toDouble();
    refRootzone = settings.value("SOIL/refRootzone").toDouble();
    refMaxSoildepth = settings.value("SOIL/refMaxSoildepth").toDouble();
    initmoist = settings.value("SOIL/initmoist").toDouble();

    optionErosion = settings.value("EROSION/optionErosion").toInt();
    optionD50 = settings.value("EROSION/optionD50").toInt();
    optionSplash = settings.value("EROSION/optionSplash").toInt();
    optionChannelsNoEros = settings.value("EROSION/optionChannelsNoEros").toInt();

    optionUseInfrastructure = settings.value("INFRA/optionUseInfrastructure").toInt();
    buildingsSHPName = checkName(1,settings.value("INFRA/buildingsSHPName").toString());
    optionUseDrums = settings.value("INFRA/optionUseDrums").toInt();
    drummapName = settings.value("INFRA/drumMap").toString();
    roadsSHPName = checkName(1,settings.value("INFRA/roadsSHPName").toString());
    roofStore = settings.value("INFRA/roofStore").toDouble();

    optionRain = settings.value("RAINFALL/optionRain").toInt();
    //RainScriptFileName = settings.value("RAINFALL/RainScript").toString();
    //RainRefNameDEM = checkName(1,settings.value("RAINFALL/RainRefNameDEM").toString());
    RainBaseDirName = checkName(0,settings.value("RAINFALL/RainBaseDirectory").toString());
    RainDirName = checkName(0,settings.value("RAINFALL/RainDirectory").toString());
    RainFilename =  settings.value("RAINFALL/RainFilename").toString();
    RainEPSG = settings.value("RAINFALL/RainEPSG").toString();
    //RainString = settings.value("RAINFALL/RainString").toString();
    comboBox_rainString->clear();
    for (int i=0; i < 10; i++) {
        QString s = settings.value(QString("RAINFALL/RainString_%1").arg(i)).toString();
        if (!s.isEmpty())
            comboBox_rainString->addItem(s);
    }

    optionGaugeGPM = settings.value("RAINFALL/SelectPointfromGPM").toInt();
    RainGaugeFilename = checkName(0,settings.value("RAINFALL/RainGaugeFilename").toString());
    RainGaugeFilenameIn = checkName(0,settings.value("RAINFALL/RainGaugeFilenameIn").toString());
  //  IDMScriptFileName = settings.value("RAINFALL/IDMScript").toString();
    IDMFilename = checkName(0,settings.value("RAINFALL/IDMFilename").toString());
    RainFilenameHourIDM = checkName(0,settings.value("RAINFALL/RainFilenameHourIDM").toString());
  //  ERAScriptFileName = settings.value("RAINFALL/ERAScript").toString();
    ERAFilename = checkName(0,settings.value("RAINFALL/ERAFilename").toString());
    RainFilenameHourERA = checkName(0,settings.value("RAINFALL/RainFilenameHourERA").toString());
    dailyA = settings.value("RAINFALL/dailyA").toDouble();
    dailyB = settings.value("RAINFALL/dailyB").toDouble();
    day0 = settings.value("RAINFALL/day0").toInt();
    dayn = settings.value("RAINFALL/dayn").toInt();
    dt30min = settings.value("RAINFALL/30min").toInt();
    conversionmm = settings.value("RAINFALL/conversionmm").toDouble();
    timeintervalGPM = settings.value("RAINFALL/timeinterval").toDouble();
    interpolationGPM = settings.value("RAINFALL/interpolation").toDouble();

}

void MainWindow::readValuesfromUI()
{
    CondaBaseDirName = combo_envs->currentText();
    ScriptFileName= lineEdit_Script->text();
    BaseDirName = lineEdit_Base->text();
    MapsDirName = lineEdit_Maps->text();
    ESPGnumber = E_ESPGnumber->text();

    BaseDEMName = lineEdit_baseDEM->text();
    BaseChannelName = lineEdit_baseChannel->text();
    BaseOutletsName = lineEdit_userOutlets->text();    
    BaseOutpointsName = lineEdit_userOutpoints->text();

    optionDEM = checkBox_DEM->isChecked() ? 1 : 0;
    optionFillDEM = checkBox_correctDEM->isChecked() ? 1 : 0;
    DEMfill = spin_DEMfill->value();

    optionChannels = checkBox_Channels->isChecked() ? 1 : 0;
    BaseCulvertsName = lineEdit_userCulverts->text();
    optionUseCulverts = checkBox_useCulverts->isChecked() ? 1 : 0;
    optionPruneBranch = 1; //checkBox_pruneBranch->isChecked() ? 1 : 0;
    optionIncludeDams = checkBox_createDams->isChecked() ? 1 : 0;
    BaseDamsName = lineEdit_Dams->text();
    optionUserOutlets = radioButton_OutletMultiple->isChecked() ? 1 : 0;
    chWidth = spin_chWidth->value();
    chWidthS = spin_chWidthS->value();
    chB = spin_chB->value();
    chDepth = spin_chDepth->value();
    chDepthS = spin_chDepthS->value();
    chC = spin_chC->value();
    chN = spin_chN->value();
    chBaseflow = spin_chBaseflow->value();
    OutletstableName = lineEdit_outletsTable->text();
    WatershedsName = lineEdit_userWatersheds->text();

    optionLULC = checkBox_LULC->isChecked() ? 1 : 0;
    LULCmapName = lineEdit_LULCMap->text();
    LULCtableName = lineEdit_LULCTable->text();
    NDVImapName = lineEdit_NDVIMap->text();
    optionUseNDVI = checkBox_useNDVI->isChecked() ? 1 : 0;

    optionInfil = checkBox_Infil->isChecked() ? 1 : 0;
    optionSG = checkBox_Soilgrids->isChecked() ? 1 : 0;
    SG1 = comboBox_SGlayer1->currentIndex();
    SG2 = comboBox_SGlayer2->currentIndex();
    optionSGInterpolation = checkBox_SGInterpolation->isChecked() ? 1 : 0;
    optionResample = comboBox_Resample->currentIndex();
  //  optionSGAverage = checkBox_SGAverage->isChecked() ? 1 : 0;
    optionNoGravel = checkBox_noGravel->isChecked() ? 1 : 0;
    optionUseBD = 1; //checkBox_userefBD->isChecked() ? 1 : 0;
    optionUseCorrOM  = checkBox_useCorrOM->isChecked() ? 1 : 0;
    corrOM = spin_corrOM->value();
    optionUseCorrTexture  = checkBox_useCorrTexture->isChecked() ? 1 : 0;
    corrClay = spin_corrClay->value();
    corrSilt = spin_corrSilt->value();
    corrSand = spin_corrSand->value();
    optionUseDensity = checkBox_useLUdensity->isChecked() ? 1 : 0;
    refBulkDens = spin_refBD->value();
    // optionUseBD2 = checkBox_userefBD2->isChecked() ? 1 : 0;
  //  refBulkDens2 = spin_refBD2->value();
    refRootzone = spin_Rootzone->value();
    refMaxSoildepth = spin_MaxSoildepth->value();
    initmoist = spin_initmoist->value();

    optionErosion = checkBox_erosion->isChecked() ? 1 : 0;
    optionD50 = checkBox_D50->isChecked() ? 1 : 0;
    optionSplash = spin_Splash->value();
    optionChannelsNoEros = checkBox_ChannelsNoErosion->isChecked() ? 1 : 0;

    optionUseInfrastructure = checkBox_useInfrastructure->isChecked() ? 1 : 0;
    buildingsSHPName = lineEdit_buildingsSHP->text();
    optionUseDrums = checkBox_useDrums->isChecked() ? 1 : 0;
    drummapName = lineEdit_drumMap->text();
    roadsSHPName = lineEdit_roadsSHP->text();
    roofStore = spin_roofStore->value();

    optionRain  = checkBox_Rain->isChecked() ? 1 : 0;
    RainBaseDirName = lineEdit_GPMdir->text();
    RainDirName = lineEdit_RainfallDir->text();
    //RainScriptFileName= lineEdit_GPMpy->text();
    RainRefNameDEM = BaseDEMName;//lineEdit_GPMrefmap->text();    
    RainFilename = lineEdit_RainFilename->text();
    RainEPSG = lineEdit_RainEPSG->text();
    RainString = comboBox_rainString->currentText();
    RainGaugeFilename = lineEdit_RainGaugeFilenameGPM->text();
    RainGaugeFilenameIn = lineEdit_RainGaugeFilenameGPMin->text();
    optionGaugeGPM = checkBox_writeGaugeData->isChecked() ? 1 : 0;
    //IDMScriptFileName = lineEdit_IMDpy->text();
    IDMFilename = lineEdit_IDMFilename->text();
    RainFilenameHourIDM = lineEdit_RainFilenameHourIDM->text();
    dailyA = spin_dailyA->value();
    dailyB = spin_dailyB->value();
    day0 = spin_day0->value();
    dayn = spin_dayn->value();
    dt30min = spin_30min->value();
    conversionmm = spin_conversionmm->value();
    timeintervalGPM = spin_timeinterval->value();
    interpolationGPM = spin_interpolation->value();
    //ERAScriptFileName = lineEdit_ERApy->text();
    RainFilenameHourERA = lineEdit_RainFilenameHourERA->text();
    ERAFilename = lineEdit_ERAFilename->text();
}

void MainWindow::writeValuestoUI()
{
    combo_envs->setCurrentText(CondaBaseDirName);
    lineEdit_Script->setText(ScriptFileName);
    lineEdit_Base->setText(BaseDirName );
    lineEdit_Maps->setText(MapsDirName);
    E_ESPGnumber->setText(ESPGnumber);

    lineEdit_baseDEM->setText(BaseDEMName);
    lineEdit_baseChannel->setText(BaseChannelName);
    lineEdit_userOutlets->setText(BaseOutletsName);
    lineEdit_userOutpoints->setText(BaseOutpointsName);

    checkBox_DEM->setChecked(optionDEM > 0) ;
    checkBox_correctDEM->setChecked(optionFillDEM > 0);
    spin_DEMfill->setValue(DEMfill);

    checkBox_Channels->setChecked(optionChannels > 0);
    lineEdit_userCulverts->setText(BaseCulvertsName);
    checkBox_useCulverts->setChecked(optionUseCulverts > 0);
    //checkBox_pruneBranch->setChecked(optionPruneBranch > 0);
    checkBox_createDams->setChecked(optionIncludeDams > 0);
    lineEdit_Dams->setText(BaseDamsName);
    radioButton_OutletSIngle->setChecked(optionUserOutlets == 0);
    radioButton_OutletMultiple->setChecked(optionUserOutlets > 0);
    spin_chWidth->setValue(chWidth);
    spin_chWidthS->setValue(chWidthS);
    spin_chB->setValue(chB);
    spin_chDepth->setValue(chDepth);
    spin_chDepthS->setValue(chDepthS);
    spin_chC->setValue(chC);
    spin_chN->setValue(chN);
    spin_chBaseflow->setValue(chBaseflow);
    lineEdit_outletsTable->setText(OutletstableName);
    lineEdit_userWatersheds->setText(WatershedsName);

    checkBox_LULC->setChecked(optionLULC > 0);
    lineEdit_LULCMap->setText(LULCmapName);
    lineEdit_LULCTable->setText(LULCtableName);
    lineEdit_NDVIMap->setText(NDVImapName);
    checkBox_useNDVI->setChecked(optionUseNDVI > 0);

    checkBox_Infil->setChecked(optionInfil > 0);
    checkBox_Soilgrids->setChecked(optionSG > 0);
    comboBox_SGlayer1->setCurrentIndex(SG1);
    comboBox_SGlayer2->setCurrentIndex(SG2);
    checkBox_SGInterpolation->setChecked(optionSGInterpolation > 0);
    //checkBox_SGAverage->setChecked(optionSGAverage > 0);
    comboBox_Resample->setCurrentIndex(optionResample);
    checkBox_noGravel->setChecked(optionNoGravel > 0);
    //checkBox_userefBD->setChecked(optionUseBD > 0);
    //checkBox_userefBD2->setChecked(optionUseBD2 > 0);
    checkBox_useCorrOM->setChecked(optionUseCorrOM > 0);
    spin_corrOM->setValue(corrOM);
    checkBox_useCorrTexture->setChecked(optionUseCorrTexture > 0);
    spin_corrClay->setValue(corrSand);
    spin_corrSilt->setValue(corrSilt);
    spin_corrSand->setValue(corrSand);
    checkBox_useLUdensity->setChecked(optionUseDensity > 0);
    spin_refBD->setValue(refBulkDens);
    //spin_refBD2->setValue(refBulkDens2);
    spin_Rootzone->setValue(refRootzone);
    spin_MaxSoildepth->setValue(refMaxSoildepth);
    spin_initmoist->setValue(initmoist);

    checkBox_erosion->setChecked(optionErosion > 0);
    checkBox_D50->setChecked(optionD50 > 0);
    spin_Splash->setValue(optionSplash);
    checkBox_ChannelsNoErosion->setChecked(optionChannelsNoEros > 0);
    spin_Splash->setValue(1);

    if (optionUserOutlets == 0) {
        on_radioButton_OutletMultiple_toggled(false);
        on_radioButton_OutletSIngle_toggled(true);
    } else {
        on_radioButton_OutletMultiple_toggled(true);
        on_radioButton_OutletSIngle_toggled(false);
    }    

    checkBox_useInfrastructure->setChecked(optionUseInfrastructure > 0);
    lineEdit_buildingsSHP->setText(buildingsSHPName);
    checkBox_useDrums->setChecked(optionUseDrums > 0);
    lineEdit_drumMap->setText(drummapName);
    lineEdit_roadsSHP->setText(roadsSHPName);
    spin_roofStore->setValue(roofStore);

    checkBox_Rain->setChecked(optionRain > 0);
    scrollArea_Rain->setEnabled(optionRain > 0);
    groupBox_raindata->setEnabled(optionRain > 0);
    groupBox_dailyraindata->setEnabled(optionRain > 0);

   // lineEdit_GPMpy->setText(RainScriptFileName);
    lineEdit_GPMrefmap->setText(BaseDEMName);//RainRefNameDEM);
    lineEdit_GPMdir->setText(RainBaseDirName);
    lineEdit_RainfallDir->setText(RainDirName);
    lineEdit_RainFilename->setText(RainFilename);
    lineEdit_RainEPSG->setText(RainEPSG);

    lineEdit_RainGaugeFilenameGPM->setText(RainGaugeFilename);
    lineEdit_RainGaugeFilenameGPMin->setText(RainGaugeFilenameIn);
    checkBox_writeGaugeData->setChecked(optionGaugeGPM > 0);
   // lineEdit_IMDpy->setText(IDMScriptFileName);
    lineEdit_IDMFilename->setText(IDMFilename);
    lineEdit_RainFilenameHourIDM->setText(RainFilenameHourIDM);
    spin_dailyA->setValue(dailyA);
    spin_dailyB->setValue(dailyB);
    spin_day0->setValue(day0);
    spin_dayn->setValue(dayn);
    spin_30min->setValue(dt30min);
    spin_conversionmm->setValue(conversionmm);
    spin_timeinterval->setValue(timeintervalGPM);
    spin_interpolation->setValue(interpolationGPM);
   // lineEdit_ERApy->setText(ERAScriptFileName);
    lineEdit_ERAFilename->setText(ERAFilename);
    lineEdit_RainFilenameHourERA->setText(RainFilenameHourERA);

}



