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
        skeys << s;
    }
    skeys.removeDuplicates();
    combo_iniName->addItems(skeys);

//    qDebug() << keys;
//    keys.removeDuplicates();
//    qDebug() << keys;
//    combo_iniName->clear();
//    for (int i = 0; i < keys.size(); i++) {
//        QString s = settings.value(QString(i)).toString();
//        if (!s.isEmpty())
//            combo_iniName->addItem(s);
//        //settings.setValue(QString(i),combo_iniName->itemText(i));
//    }
}

void MainWindow::setIni(QString sss)
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

    settings.setValue("DEM/optionCatchments", QString::number(optionCatchments));
    settings.setValue("DEM/optionDEM", QString::number(optionDEM));
    settings.setValue("DEM/CatchmentSize", QString::number(CatchmentSize, 'f', 2));
    settings.setValue("DEM/optionFillDEM", QString::number(optionFillDEM));
    settings.setValue("DEM/DEMfill", QString::number(DEMfill, 'f', 2));

    settings.setValue("CHANNEL/optionChannels", QString::number(optionChannels));
    settings.setValue("CHANNEL/optionPruneBranch", QString::number(optionPruneBranch));
    settings.setValue("CHANNEL/optionIncludeDams", QString::number(optionIncludeDams));
    settings.setValue("CHANNEL/BaseDams", BaseDamsName);
    settings.setValue("CHANNEL/optionUserOutlets", QString::number(optionUserOutlets));  //0=1 outlet, >0 is multiple
   // settings.setValue("CHANNEL/chA", QString::number(chWidth, 'f', 1));
  //  settings.setValue("CHANNEL/chD", QString::number(chDepth, 'f', 1));
    settings.setValue("CHANNEL/chWidth", QString::number(chWidth, 'f', 1));
    settings.setValue("CHANNEL/chB", QString::number(chB, 'f', 3));
    settings.setValue("CHANNEL/chDepth", QString::number(chDepth, 'f', 1));
    settings.setValue("CHANNEL/chC", QString::number(chC, 'f', 3));
    settings.setValue("CHANNEL/chBaseflow", QString::number(chBaseflow, 'f', 1));
    settings.setValue("CHANNEL/BaseOutlets", BaseOutletsName);
    settings.setValue("CHANNEL/Outletstable", OutletstableName);

    settings.setValue("LULC/optionLULC", QString::number(optionLULC));
  //  settings.setValue("LULCDirectory", LULCDirName);
    settings.setValue("LULC/LULCmap", LULCmapName);
    settings.setValue("LULC/LULCtable", LULCtableName);

    settings.setValue("SOIL/optionInfil", QString::number(optionInfil));
    settings.setValue("SOIL/optionSG", QString::number(optionSG)); // do soilgrids
    settings.setValue("SOIL/optionSG1", QString::number(SG1));
    settings.setValue("SOIL/optionSG2", QString::number(SG2));
    settings.setValue("SOIL/optionSGInterpolation", QString::number(optionSGInterpolation)); // do soilgrids
    settings.setValue("SOIL/optionUseBD", QString::number(optionUseBD));
    settings.setValue("SOIL/optionUseDensity", QString::number(optionUseDensity));
    settings.setValue("SOIL/refBulkDens", QString::number(refBulkDens, 'f', 0));
    settings.setValue("SOIL/refRootzone", QString::number(refRootzone, 'f', 2));
    settings.setValue("SOIL/refMaxSoildepth", QString::number(refMaxSoildepth, 'f', 2));
    settings.setValue("SOIL/initmoist", QString::number(initmoist, 'f', 2));

    settings.setValue("EROSION/optionErosion", QString::number(optionErosion));
    settings.setValue("EROSION/optionD50", QString::number(optionD50));
    settings.setValue("EROSION/optionChannelsNoEros", QString::number(optionChannelsNoEros));

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

    optionCatchments = settings.value("DEM/optionCatchments").toInt();
    optionDEM = settings.value("DEM/optionDEM").toInt();
    CatchmentSize = settings.value("DEM/CatchmentSize").toDouble();
    optionFillDEM = settings.value("DEM/optionFillDEM").toInt();
    DEMfill = settings.value("DEM/DEMfill").toDouble();

    optionChannels = settings.value("CHANNEL/optionChannels").toInt();
    optionPruneBranch = settings.value("CHANNEL/optionPruneBranch").toInt();
    optionIncludeDams = settings.value("CHANNEL/optionIncludeDams").toInt();
    BaseDamsName = settings.value("CHANNEL/BaseDams").toString();
    optionUserOutlets = settings.value("CHANNEL/optionUserOutlets").toInt();
   // chA = settings.value("CHANNEL/chA").toDouble();
   // chD = settings.value("CHANNEL/chD").toDouble();
    chWidth = settings.value("CHANNEL/chWidth").toDouble();
    chB = settings.value("CHANNEL/chB").toDouble();
    chDepth = settings.value("CHANNEL/chDepth").toDouble();
    chC = settings.value("CHANNEL/chC").toDouble();
    chBaseflow = settings.value("CHANNEL/chBaseflow").toDouble();
    BaseOutletsName = settings.value("CHANNEL/BaseOutlets").toString();
    OutletstableName = settings.value("CHANNEL/Outletstable").toString();

    optionLULC = settings.value("LULC/optionLULC").toInt();
    LULCmapName = settings.value("LULC/LULCmap").toString();
    LULCtableName = settings.value("LULC/LULCtable").toString();

    optionInfil = settings.value("SOIL/optionInfil").toInt();
    optionSG = settings.value("SOIL/optionSG").toInt();
    SG1 = settings.value("SOIL/optionSG1").toInt();
    SG2 = settings.value("SOIL/optionSG2").toInt();
    optionSGInterpolation = settings.value("SOIL/optionSGInterpolation").toInt();
    optionUseBD = settings.value("SOIL/optionUseBD").toInt();
    optionUseDensity = settings.value("SOIL/optionUseDensity").toInt();
    refBulkDens = settings.value("SOIL/refBulkDens").toDouble();
    refRootzone = settings.value("SOIL/refRootzone").toDouble();
    refMaxSoildepth = settings.value("SOIL/refMaxSoildepth").toDouble();
    initmoist = settings.value("SOIL/initmoist").toDouble();

    optionErosion = settings.value("EROSION/optionErosion").toInt();
    optionD50 = settings.value("EROSION/optionD50").toInt();
    optionChannelsNoEros = settings.value("EROSION/optionChannelNoEros").toInt();

}

void MainWindow::readValuesfromUI()
{
    CondaBaseDirName = combo_envs->currentText();
    ScriptFileName= lineEdit_Script->text();
    BaseDirName = lineEdit_Base->text();
    MapsDirName = lineEdit_Maps->text();
    BaseDEMName = lineEdit_baseDEM->text();
    BaseChannelName = lineEdit_baseChannel->text();
    ESPGnumber = E_ESPGnumber->text();

    optionCatchments = checkBox_Catchments->isChecked() ? 1 : 0;
    optionDEM = checkBox_DEM->isChecked() ? 1 : 0;
    CatchmentSize = E_catchmentSize->text().toDouble();
    optionFillDEM = checkBox_correctDEM->isChecked() ? 1 : 0;
    DEMfill = spin_DEMfill->value();

    optionChannels = checkBox_Channels->isChecked() ? 1 : 0;
    optionPruneBranch = 1; //checkBox_pruneBranch->isChecked() ? 1 : 0;
    optionIncludeDams = checkBox_createDams->isChecked() ? 1 : 0;
    BaseDamsName = lineEdit_Dams->text();
    optionUserOutlets = radioButton_OutletMultiple->isChecked() ? 1 : 0;
    chWidth = spin_chWidth->value();
    chB = spin_chB->value();
    chDepth = spin_chDepth->value();
    chC = spin_chC->value();
    chBaseflow = spin_chBaseflow->value();
    BaseOutletsName = lineEdit_userOutlets->text();
    OutletstableName = lineEdit_outletsTable->text();

    optionLULC = checkBox_LULC->isChecked() ? 1 : 0;
    LULCmapName = lineEdit_LULCMap->text();
    LULCtableName = lineEdit_LULCTable->text();

    optionInfil = checkBox_Infil->isChecked() ? 1 : 0;
    optionSG = checkBox_Soilgrids->isChecked() ? 1 : 0;
    SG1 = comboBox_SGlayer1->currentIndex();
    SG2 = comboBox_SGlayer2->currentIndex();
    optionSGInterpolation = checkBox_SGInterpolation->isChecked() ? 1 : 0;
    optionUseBD = checkBox_userefBD->isChecked() ? 1 : 0;
    optionUseDensity = checkBox_useLUdensity->isChecked() ? 1 : 0;
    refBulkDens = spin_refBD->value();
    refRootzone = spin_Rootzone->value();
    refMaxSoildepth = spin_MaxSoildepth->value();
    initmoist = spin_initmoist->value();

    optionErosion = checkBox_erosion->isChecked() ? 1 : 0;
    optionD50 = checkBox_D50->isChecked() ? 1 : 0;
    optionChannelsNoEros = checkBox_ChannelsNoErosion->isChecked() ? 1 : 0;

}

void MainWindow::writeValuestoUI()
{
    combo_envs->setCurrentText(CondaBaseDirName);
    comboBox_SGlayer1->setCurrentIndex(SG1);
    comboBox_SGlayer2->setCurrentIndex(SG2);

    lineEdit_Base->setText(BaseDirName );
    lineEdit_baseChannel->setText(BaseChannelName);
    lineEdit_baseDEM->setText(BaseDEMName);
    lineEdit_Maps->setText(MapsDirName);
    //lineEdit_LULC->setText(LULCDirName);
    lineEdit_LULCMap->setText(LULCmapName);
    lineEdit_LULCTable->setText(LULCtableName);

    lineEdit_outletsTable->setText(OutletstableName);

    lineEdit_Script->setText(ScriptFileName);
    E_ESPGnumber->setText(ESPGnumber);

    spin_initmoist->setValue(initmoist);
    spin_refBD->setValue(refBulkDens);
    //E_DEMfill->setText(QString::number(DEMfill,'f',1));
    spin_DEMfill->setValue(DEMfill);
    E_catchmentSize->setText(QString::number(CatchmentSize,'f',1));
    //spin_chA->setValue(chA);
    spin_chB->setValue(chB);
    spin_chC->setValue(chC);
    spin_chWidth->setValue(chWidth);
    spin_chDepth->setValue(chDepth);
    spin_chBaseflow->setValue(chBaseflow);
    spin_Rootzone->setValue(refRootzone);
    spin_MaxSoildepth->setValue(refMaxSoildepth);

    checkBox_DEM->setChecked(optionDEM > 0);
    checkBox_Channels->setChecked(optionChannels > 0);
    checkBox_LULC->setChecked(optionLULC > 0);
    checkBox_Soilgrids->setChecked(optionSG > 0);
    checkBox_Infil->setChecked(optionInfil > 0);
    checkBox_erosion->setChecked(optionErosion > 0);
    checkBox_D50->setChecked(optionD50 > 0);
    checkBox_userefBD->setChecked(optionUseBD > 0);
    checkBox_useLUdensity->setChecked(optionUseDensity > 0);
    checkBox_correctDEM->setChecked(optionFillDEM > 0);
    checkBox_Catchments->setChecked(optionCatchments > 0);
    checkBox_ChannelsNoErosion->setChecked(optionChannelsNoEros > 0);
    radioButton_OutletMultiple->setChecked(optionUserOutlets > 0);
    radioButton_OutletSIngle->setChecked(optionUserOutlets == 0);
    //checkBox_pruneBranch->setChecked(optionPruneBranch > 0);
    checkBox_createDams->setChecked(optionIncludeDams > 0);
    checkBox_SGInterpolation->setChecked(optionSGInterpolation > 0);

    if (optionUserOutlets == 0) {
        on_radioButton_OutletMultiple_toggled(false);
        on_radioButton_OutletSIngle_toggled(true);
    } else {
        on_radioButton_OutletMultiple_toggled(true);
        on_radioButton_OutletSIngle_toggled(false);
    }

}



