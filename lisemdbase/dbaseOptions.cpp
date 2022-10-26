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

    settings.setValue("DEM/optionCatchments", QString::number(optionCatchments));
    settings.setValue("DEM/optionDEM","1");// QString::number(optionDEM));
//    settings.setValue("DEM/CatchmentSize", QString::number(CatchmentSize, 'f', 2));
    settings.setValue("DEM/optionFillDEM", QString::number(optionFillDEM));
    settings.setValue("DEM/DEMfill", QString::number(DEMfill, 'f', 2));

    settings.setValue("CHANNEL/BaseCulverts",  BaseCulvertsName);
    settings.setValue("CHANNEL/optionUseCulverts", QString::number(optionUseCulverts));
    settings.setValue("CHANNEL/optionChannels", "1");//QString::number(optionChannels));
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
    settings.setValue("SOIL/optionSGAverage", QString::number(optionSGAverage)); // do soilgrids
    settings.setValue("SOIL/optionNoGravel", QString::number(optionNoGravel)); // do soilgrids
    settings.setValue("SOIL/optionUseBD", QString::number(optionUseBD));
    settings.setValue("SOIL/optionUseCorrOM", QString::number(optionUseCorrOM));
    settings.setValue("SOIL/corrOM", QString::number(corrOM, 'f', 2));
    //settings.setValue("SOIL/optionUseBD2", QString::number(optionUseBD2));
    settings.setValue("SOIL/optionUseDensity", QString::number(optionUseDensity));
    settings.setValue("SOIL/refBulkDens", QString::number(refBulkDens, 'f', 0));
    //settings.setValue("SOIL/refBulkDens2", QString::number(refBulkDens2, 'f', 0));
    settings.setValue("SOIL/refRootzone", QString::number(refRootzone, 'f', 2));
    settings.setValue("SOIL/refMaxSoildepth", QString::number(refMaxSoildepth, 'f', 2));
    settings.setValue("SOIL/initmoist", QString::number(initmoist, 'f', 2));

    settings.setValue("EROSION/optionErosion", QString::number(optionErosion));
    settings.setValue("EROSION/optionD50", QString::number(optionD50));
    settings.setValue("EROSION/optionChannelsNoEros", QString::number(optionChannelsNoEros));

    settings.setValue("RAINFALL/RainScript", RainScriptFileName);    
    settings.setValue("RAINFALL/RainRefNameDEM", RainRefNameDEM);
    settings.setValue("RAINFALL/RainBaseDirectory", RainBaseDirName);
    settings.setValue("RAINFALL/RainDirectory", RainDirName);
    settings.setValue("RAINFALL/RainFilename", RainFilename);
    settings.setValue("RAINFALL/SelectPointfromGPM", QString::number(optionGaugeGPM));
    settings.setValue("RAINFALL/RainGaugeFilename", RainGaugeFilename);
    settings.setValue("RAINFALL/RainGaugeFilenameIn", RainGaugeFilenameIn);
    settings.setValue("RAINFALL/IDMScript", IDMScriptFileName);
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
    settings.setValue("RAINFALL/ERAScript", ERAScriptFileName);
    settings.setValue("RAINFALL/ERAFilename", ERAFilename);
    settings.setValue("RAINFALL/RainFilenameHourERA", RainFilenameHourERA);


    settings.sync();
}

void MainWindow::getIni(QString name)
{
    QSettings settings(name,QSettings::IniFormat);
    settings.sync();

    CondaBaseDirName = settings.value("CondaDirectory").toString();
    ScriptFileName = settings.value("Script").toString();
    BaseDirName = settings.value("BaseDirectory").toString();
    MapsDirName = settings.value("MapsDirectory").toString();
    ESPGnumber = settings.value("ESPGnumber").toString();

    BaseDEMName = settings.value("BaseDEM").toString();
    BaseChannelName = settings.value("BaseChannel").toString();
    BaseOutletsName = settings.value("BaseOutlets").toString();
    BaseOutpointsName = settings.value("BaseOutpoints").toString();

    optionCatchments = settings.value("DEM/optionCatchments").toInt();
    //optionDEM = settings.value("DEM/optionDEM").toInt();
    //CatchmentSize = settings.value("DEM/CatchmentSize").toDouble();
    optionFillDEM = settings.value("DEM/optionFillDEM").toInt();
    DEMfill = settings.value("DEM/DEMfill").toDouble();

    BaseCulvertsName = settings.value("CHANNEL/BaseCulverts").toString();
    optionUseCulverts = settings.value("CHANNEL/optionUseCulverts").toInt();
    //optionChannels = settings.value("CHANNEL/optionChannels").toInt();
    optionPruneBranch = settings.value("CHANNEL/optionPruneBranch").toInt();
    optionIncludeDams = settings.value("CHANNEL/optionIncludeDams").toInt();
    BaseDamsName = settings.value("CHANNEL/BaseDams").toString();
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
    LULCmapName = settings.value("LULC/LULCmap").toString();
    LULCtableName = settings.value("LULC/LULCtable").toString();
    NDVImapName = settings.value("LULC/NDVImap").toString();
    optionUseNDVI = settings.value("LULC/optionUseNDVI").toInt();

    optionInfil = settings.value("SOIL/optionInfil").toInt();
    optionSG = settings.value("SOIL/optionSG").toInt();
    SG1 = settings.value("SOIL/optionSG1").toInt();
    SG2 = settings.value("SOIL/optionSG2").toInt();
    optionSGInterpolation = settings.value("SOIL/optionSGInterpolation").toInt();
    optionSGAverage = settings.value("SOIL/optionSGAverage").toInt();
    optionNoGravel = settings.value("SOIL/optionNoGravel").toInt();
    optionUseBD = 1;//settings.value("SOIL/optionUseBD").toInt();
    //optionUseBD2 = settings.value("SOIL/optionUseBD2").toInt();
    optionUseCorrOM = settings.value("SOIL/optionUseCorrOM ").toInt();
    corrOM = settings.value("SOIL/corrOM").toDouble();
    optionUseDensity = settings.value("SOIL/optionUseDensity").toInt();
    refBulkDens = settings.value("SOIL/refBulkDens").toDouble();

    //refBulkDens2 = settings.value("SOIL/refBulkDens2").toDouble();
    refRootzone = settings.value("SOIL/refRootzone").toDouble();
    refMaxSoildepth = settings.value("SOIL/refMaxSoildepth").toDouble();
    initmoist = settings.value("SOIL/initmoist").toDouble();

    optionErosion = settings.value("EROSION/optionErosion").toInt();
    optionD50 = settings.value("EROSION/optionD50").toInt();
    optionChannelsNoEros = settings.value("EROSION/optionChannelsNoEros").toInt();

    RainScriptFileName = settings.value("RAINFALL/RainScript").toString();
    RainRefNameDEM = settings.value("RAINFALL/RainRefNameDEM").toString();
    RainBaseDirName = settings.value("RAINFALL/RainBaseDirectory").toString();
    RainDirName = settings.value("RAINFALL/RainDirectory").toString();
    RainFilename = settings.value("RAINFALL/RainFilename").toString();

    optionGaugeGPM = settings.value("RAINFALL/SelectPointfromGPM").toInt();
    RainGaugeFilename = settings.value("RAINFALL/RainGaugeFilename").toString();
    RainGaugeFilenameIn = settings.value("RAINFALL/RainGaugeFilenameIn").toString();
    IDMScriptFileName = settings.value("RAINFALL/IDMScript").toString();
    IDMFilename = settings.value("RAINFALL/IDMFilename").toString();
    RainFilenameHourIDM = settings.value("RAINFALL/RainFilenameHourIDM").toString();
    ERAScriptFileName = settings.value("RAINFALL/ERAScript").toString();
    ERAFilename = settings.value("RAINFALL/ERAFilename").toString();
    RainFilenameHourERA = settings.value("RAINFALL/RainFilenameHourERA").toString();

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

    optionDEM = 1;//checkBox_DEM->isChecked() ? 1 : 0;
    optionFillDEM = checkBox_correctDEM->isChecked() ? 1 : 0;
    DEMfill = spin_DEMfill->value();

    BaseCulvertsName = lineEdit_userCulverts->text();
    optionUseCulverts = checkBox_useCulverts->isChecked() ? 1 : 0;
    optionChannels = 1;//checkBox_Channels->isChecked() ? 1 : 0;
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

    optionLULC = 1;//checkBox_LULC->isChecked() ? 1 : 0;
    LULCmapName = lineEdit_LULCMap->text();
    LULCtableName = lineEdit_LULCTable->text();
    NDVImapName = lineEdit_NDVIMap->text();
    optionUseNDVI = checkBox_useNDVI->isChecked() ? 1 : 0;

    optionInfil = 1;//checkBox_Infil->isChecked() ? 1 : 0;
    optionSG = checkBox_Soilgrids->isChecked() ? 1 : 0;
    SG1 = comboBox_SGlayer1->currentIndex();
    SG2 = comboBox_SGlayer2->currentIndex();
    optionSGInterpolation = checkBox_SGInterpolation->isChecked() ? 1 : 0;
    optionSGAverage = checkBox_SGAverage->isChecked() ? 1 : 0;
    optionNoGravel = checkBox_noGravel->isChecked() ? 1 : 0;
    optionUseBD = 1; //checkBox_userefBD->isChecked() ? 1 : 0;
   // optionUseBD2 = checkBox_userefBD2->isChecked() ? 1 : 0;
    optionUseCorrOM  = checkBox_useCorrOM->isChecked() ? 1 : 0;
    corrOM = spin_corrOM->value();
    optionUseDensity = checkBox_useLUdensity->isChecked() ? 1 : 0;
    refBulkDens = spin_refBD->value();
  //  refBulkDens2 = spin_refBD2->value();
    refRootzone = spin_Rootzone->value();
    refMaxSoildepth = spin_MaxSoildepth->value();
    initmoist = spin_initmoist->value();

    optionErosion = 1;//checkBox_erosion->isChecked() ? 1 : 0;
    optionD50 = checkBox_D50->isChecked() ? 1 : 0;
    optionChannelsNoEros = checkBox_ChannelsNoErosion->isChecked() ? 1 : 0;

    RainBaseDirName = lineEdit_GPMdir->text();
    RainDirName = lineEdit_RainfallDir->text();

    RainScriptFileName= lineEdit_GPMpy->text();
    RainRefNameDEM = lineEdit_GPMrefmap->text();
    RainFilename = lineEdit_RainFilenameGPM->text();
    RainGaugeFilename = lineEdit_RainGaugeFilenameGPM->text();
    RainGaugeFilenameIn = lineEdit_RainGaugeFilenameGPMin->text();
    optionGaugeGPM = checkBox_writeGaugeData->isChecked() ? 1 : 0;

    IDMScriptFileName = lineEdit_IMDpy->text();
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

    ERAScriptFileName = lineEdit_ERApy->text();
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
    lineEdit_userCulverts->setText(BaseCulvertsName);
    checkBox_useCulverts->setChecked(optionUseCulverts > 0);

    checkBox_correctDEM->setChecked(optionFillDEM > 0);
    spin_DEMfill->setValue(DEMfill);

    //checkBox_Channels->setChecked(optionChannels > 0);
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

    //checkBox_LULC->setChecked(optionLULC > 0);
    lineEdit_LULCMap->setText(LULCmapName);
    lineEdit_LULCTable->setText(LULCtableName);
    lineEdit_NDVIMap->setText(NDVImapName);
    checkBox_useNDVI->setChecked(optionUseNDVI > 0);

    //checkBox_Infil->setChecked(optionInfil > 0);
    checkBox_Soilgrids->setChecked(optionSG > 0);
    comboBox_SGlayer1->setCurrentIndex(SG1);
    comboBox_SGlayer2->setCurrentIndex(SG2);
    checkBox_SGInterpolation->setChecked(optionSGInterpolation > 0);
    checkBox_SGAverage->setChecked(optionSGAverage > 0);
    checkBox_noGravel->setChecked(optionNoGravel > 0);
    //checkBox_userefBD->setChecked(optionUseBD > 0);
    //checkBox_userefBD2->setChecked(optionUseBD2 > 0);
    checkBox_useCorrOM->setChecked(optionUseCorrOM > 0);
    spin_corrOM->setValue(corrOM);
    checkBox_useLUdensity->setChecked(optionUseDensity > 0);
    spin_refBD->setValue(refBulkDens);
    //spin_refBD2->setValue(refBulkDens2);
    spin_Rootzone->setValue(refRootzone);
    spin_MaxSoildepth->setValue(refMaxSoildepth);
    spin_initmoist->setValue(initmoist);

   // checkBox_erosion->setChecked(optionErosion > 0);
    checkBox_D50->setChecked(optionD50 > 0);
    checkBox_ChannelsNoErosion->setChecked(optionChannelsNoEros > 0);

    if (optionUserOutlets == 0) {
        on_radioButton_OutletMultiple_toggled(false);
        on_radioButton_OutletSIngle_toggled(true);
    } else {
        on_radioButton_OutletMultiple_toggled(true);
        on_radioButton_OutletSIngle_toggled(false);
    }    

    lineEdit_GPMpy->setText(RainScriptFileName);
    lineEdit_GPMrefmap->setText(RainRefNameDEM);
    lineEdit_GPMdir->setText(RainBaseDirName);
    lineEdit_RainfallDir->setText(RainDirName);
    lineEdit_RainFilenameGPM->setText(RainFilename);
    lineEdit_RainGaugeFilenameGPM->setText(RainGaugeFilename);
    lineEdit_RainGaugeFilenameGPMin->setText(RainGaugeFilenameIn);
    checkBox_writeGaugeData->setChecked(optionGaugeGPM > 0);

    lineEdit_IMDpy->setText(IDMScriptFileName);
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

    lineEdit_ERApy->setText(ERAScriptFileName);
    lineEdit_ERAFilename->setText(ERAFilename);
    lineEdit_RainFilenameHourERA->setText(RainFilenameHourERA);

}



