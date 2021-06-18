#include "mainwindow.h"



void MainWindow::setIni(QString sss)
{
    QSettings settings(sss,QSettings::IniFormat);
    settings.clear();

    settings.setValue("CondaDirectory", CondaBaseDirName);
    settings.setValue("Script", ScriptFileName);
    settings.setValue("BaseDirectory", BaseDirName);
    settings.setValue("BaseDEM", BaseDEMName);
    settings.setValue("BaseChannel", BaseChannelName);
    settings.setValue("BaseOutlets", BaseOutletsName);
    settings.setValue("MapsDirectory", MapsDirName);
    settings.setValue("LULCDirectory", LULCDirName);
    settings.setValue("LULCmap", LULCmapName);
    settings.setValue("LULCtable", LULCtableName);
    settings.setValue("ESPGnumber", ESPGnumber);

    settings.setValue("optionDEM", QString::number(optionDEM));
    settings.setValue("optionChannels", QString::number(optionChannels));
    settings.setValue("optionInfil", QString::number(optionInfil));
    settings.setValue("optionErosion", QString::number(optionErosion));
    settings.setValue("optionD50", QString::number(optionD50));
    settings.setValue("optionSG", QString::number(optionSG));
    settings.setValue("optionLULC", QString::number(optionLULC));
    settings.setValue("optionUseBD", QString::number(optionUseBD));
    settings.setValue("optionUseDensity", QString::number(optionUseDensity));
    settings.setValue("optionFillDEM", QString::number(optionFillDEM));
    settings.setValue("optionCatchments", QString::number(optionCatchments));
    settings.setValue("optionUserOutlets", QString::number(optionUserOutlets));
    settings.setValue("optionPruneBranch", QString::number(optionPruneBranch));

    double v = spin_refBD->value();
    settings.setValue("refBulkDens", QString::number(v, 'f', 0));
    v = spin_initmoist->value();
    settings.setValue("initmoist", QString::number(v, 'f', 1));
    int i = comboBox_SGlayer1->currentIndex();
    settings.setValue("optionSG1", QString::number(i));
    i = comboBox_SGlayer2->currentIndex();
    settings.setValue("optionSG2", QString::number(i));
    v = DEMfill;// E_DEMfill->text().toDouble();
    settings.setValue("DEMfill", QString::number(v, 'f', 1));
    v = CatchmentSize;//E_catchmentSize->text().toDouble();
    settings.setValue("CatchmentSize", QString::number(v, 'f', 1));

    settings.sync();
}

void MainWindow::getIni(QString name)
{
    QSettings settings(name,QSettings::IniFormat);
    settings.sync();

    CondaBaseDirName = settings.value("CondaDirectory").toString();
    ScriptFileName = settings.value("Script").toString();
    BaseDirName = settings.value("BaseDirectory").toString();
    BaseDEMName = settings.value("BaseDEM").toString();
    BaseChannelName = settings.value("BaseChannel").toString();
    BaseOutletsName = settings.value("BaseOutlets").toString();
    MapsDirName = settings.value("MapsDirectory").toString();
    LULCDirName = settings.value("LULCDirectory").toString();
    LULCmapName = settings.value("LULCmap").toString();
    LULCtableName = settings.value("LULCtable").toString();
    ESPGnumber = settings.value("ESPGnumber").toString();

    optionDEM = settings.value("optionDEM").toInt();
    optionChannels = settings.value("optionChannels").toInt();
    optionInfil = settings.value("optionInfil").toInt();
    optionSG = settings.value("optionSG").toInt();
    optionLULC = settings.value("optionLULC").toInt();
    optionErosion = settings.value("optionErosion").toInt();
    optionD50 = settings.value("optionD50").toInt();
    optionUseBD = settings.value("optionUseBD").toInt();
    optionUseDensity = settings.value("optionUseDensity").toInt();
    optionFillDEM = settings.value("optionFillDEM").toInt();
    optionCatchments = settings.value("optionCatchments").toInt();
    optionUserOutlets = settings.value("optionUserOutlets").toInt();
    optionPruneBranch = settings.value("optionPruneBranch").toInt();

    refBulkDens = settings.value("refBulkDens").toDouble();
    initmoist = settings.value("initmoist").toDouble();
    SG1 = settings.value("optionSG1").toInt();
    SG2 = settings.value("optionSG2").toInt();
    DEMfill = settings.value("DEMfill").toDouble();
    CatchmentSize = settings.value("CatchmentSize").toDouble();
}

void MainWindow::readValuesfromUI()
{
    CondaBaseDirName = combo_envs->currentText();
    SG1 = comboBox_SGlayer1->currentIndex();
    SG2 = comboBox_SGlayer2->currentIndex();
    BaseDirName = lineEdit_Base->text();
    BaseDEMName = lineEdit_baseDEM->text();
    BaseChannelName = lineEdit_baseChannel->text();
    BaseOutletsName = lineEdit_userOutlets->text();
    MapsDirName = lineEdit_Maps->text();
    LULCDirName = lineEdit_LULC->text();
    LULCmapName = lineEdit_LULCMap->text();
    LULCtableName = lineEdit_LULCTable->text();
    ESPGnumber = E_ESPGnumber->text();
    ScriptFileName= lineEdit_Script->text();
    initmoist = spin_initmoist->value();
    refBulkDens = spin_refBD->value();
    DEMfill = E_DEMfill->text().toDouble();
    CatchmentSize = E_catchmentSize->text().toDouble();

    optionUseBD = checkBox_userefBD->isChecked() ? 1 : 0;
    optionUseDensity = checkBox_useLUdensity->isChecked() ? 1 : 0;
    optionDEM = checkBox_DEM->isChecked() ? 1 : 0;
    optionChannels = checkBox_Channels->isChecked() ? 1 : 0;
    optionLULC = checkBox_LULC->isChecked() ? 1 : 0;
    optionSG = checkBox_Soilgrids->isChecked() ? 1 : 0;
    optionInfil = checkBox_Infil->isChecked() ? 1 : 0;
    optionErosion = checkBox_erosion->isChecked() ? 1 : 0;
    optionD50 = checkBox_D50->isChecked() ? 1 : 0;
    optionFillDEM = checkBox_correctDEM->isChecked() ? 1 : 0;
    optionCatchments = checkBox_Catchments->isChecked() ? 1 : 0;
    optionUserOutlets = checkBox_userOutlets->isChecked() ? 1 : 0;
    optionPruneBranch = checkBox_pruneBranch->isChecked() ? 1 : 0;
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
    lineEdit_LULC->setText(LULCDirName);
    lineEdit_LULCMap->setText(LULCmapName);
    lineEdit_LULCTable->setText(LULCtableName);
    lineEdit_Script->setText(ScriptFileName);
    E_ESPGnumber->setText(ESPGnumber);

    spin_initmoist->setValue(initmoist);
    spin_refBD->setValue(refBulkDens);
    E_DEMfill->setText(QString::number(DEMfill,'e',1));
    E_catchmentSize->setText(QString::number(CatchmentSize,'e',1));

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
    checkBox_userOutlets->setChecked(optionUserOutlets > 0);
    checkBox_pruneBranch->setChecked(optionPruneBranch > 0);
}

