#include "mainwindow.h"



void MainWindow::setIni(QString sss)
{
    QSettings settings(qApp->applicationDirPath()+"/"+sss,QSettings::IniFormat);
    settings.clear();

    settings.setValue("CondaDirectory", CondaBaseDirName);
    settings.setValue("Script", ScriptFileName);
    settings.setValue("BaseDirectory", BaseDirName);
    settings.setValue("BaseDEM", BaseDEMName);
    settings.setValue("BaseChannel", BaseChannelName);
    settings.setValue("MapsDirectory", MapsDirName);
    settings.setValue("LULCDirectory", LULCDirName);
    settings.setValue("LULCmap", LULCmapName);
    settings.setValue("LULCtable", LULCtableName);

    settings.setValue("optionDEM", QString::number(optionDEM));
    settings.setValue("optionChannels", QString::number(optionChannels));
    settings.setValue("optionInfil", QString::number(optionInfil));
    settings.setValue("optionErosion", QString::number(optionErosion));
    settings.setValue("optionSG", QString::number(optionSG));
    settings.setValue("optionLULC", QString::number(optionLULC));
    settings.setValue("optionUseBD", QString::number(optionUseBD));

    double v = spin_refBD->value();
    settings.setValue("refBulkDens", QString::number(v, 'f', 0));
    v = spin_initmoist->value();
    settings.setValue("initmoist", QString::number(v, 'f', 1));
    int i = comboBox_SGlayer1->currentIndex();
    settings.setValue("optionSG1", QString::number(i));
    i = comboBox_SGlayer2->currentIndex();
    settings.setValue("optionSG2", QString::number(i));

    settings.sync();
}

void MainWindow::getIni()
{
    QSettings settings(qApp->applicationDirPath()+"/LISEMdbase.ini",QSettings::IniFormat);
    settings.sync();

    CondaBaseDirName = settings.value("CondaDirectory").toString();
    ScriptFileName = settings.value("Script").toString();
    BaseDirName = settings.value("BaseDirectory").toString();
    BaseDEMName = settings.value("BaseDEM").toString();
    BaseChannelName = settings.value("BaseChannel").toString();
    MapsDirName = settings.value("MapsDirectory").toString();
    LULCDirName = settings.value("LULCDirectory").toString();
    LULCmapName = settings.value("LULCmap").toString();
    LULCtableName = settings.value("LULCtable").toString();

    optionDEM = settings.value("optionDEM").toInt();
    optionChannels = settings.value("optionChannels").toInt();
    optionInfil = settings.value("optionInfil").toInt();
    optionSG = settings.value("optionSG").toInt();
    optionLULC = settings.value("optionLULC").toInt();
    optionErosion = settings.value("optionErosion").toInt();
    optionUseBD = settings.value("optionUseBD").toInt();

    refBulkDens = settings.value("refBulkDens").toDouble();
    initmoist = settings.value("initmoist").toDouble();
    SG1 = settings.value("optionSG1").toInt();
    SG2 = settings.value("optionSG2").toInt();
}

void MainWindow::readValuesfromUI()
{
    CondaBaseDirName = combo_envs->currentText();
    SG1 = comboBox_SGlayer1->currentIndex();
    SG2 = comboBox_SGlayer2->currentIndex();
    BaseDirName = lineEdit_Base->text();
    BaseChannelName = lineEdit_baseChannel->text();
    BaseDEMName = lineEdit_baseDEM->text();
    MapsDirName = lineEdit_Maps->text();
    LULCDirName = lineEdit_LULC->text();
    LULCmapName = lineEdit_LULCMap->text();
    LULCtableName = lineEdit_LULCTable->text();
    ScriptFileName= lineEdit_Script->text();
    initmoist = spin_initmoist->value();
    refBulkDens = spin_refBD->value();

    optionUseBD = checkBox_userefBD->isChecked() ? 1 : 0;
    optionDEM = checkBox_DEM->isChecked() ? 1 : 0;
    optionChannels = checkBox_Channels->isChecked() ? 1 : 0;
    optionLULC = checkBox_LULC->isChecked() ? 1 : 0;
    optionSG = checkBox_Soilgrids->isChecked() ? 1 : 0;
    optionInfil = checkBox_Infil->isChecked() ? 1 : 0;
    optionErosion = checkBox_erosion->isChecked() ? 1 : 0;
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
    spin_initmoist->setValue(initmoist);
    spin_refBD->setValue(refBulkDens);
    checkBox_DEM->setChecked(optionDEM > 0);
    checkBox_Channels->setChecked(optionChannels > 0);
    checkBox_LULC->setChecked(optionLULC > 0);
    checkBox_Soilgrids->setChecked(optionSG > 0);
    checkBox_Infil->setChecked(optionInfil > 0);
    checkBox_erosion->setChecked(optionErosion > 0);
    checkBox_userefBD->setChecked(optionUseBD > 0);
}

