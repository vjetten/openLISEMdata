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

    settings.setValue("CondaDirectory", CondaBaseDirName);
    settings.setValue("Script", ScriptFileName);
    settings.setValue("BaseDirectory", BaseDirName);
    settings.setValue("BaseDEM", BaseDEMName);
    settings.setValue("BaseChannel", BaseChannelName);
    settings.setValue("BaseOutlets", BaseOutletsName);
    settings.setValue("BaseDams", BaseDamsName);
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
    settings.setValue("optionIncludeDams", QString::number(optionIncludeDams));

    settings.setValue("refBulkDens", QString::number(refBulkDens, 'f', 0));
    settings.setValue("refRootzone", QString::number(refRootzone, 'f', 2));
    settings.setValue("initmoist", QString::number(initmoist, 'f', 2));
    settings.setValue("optionSG1", QString::number(SG1));
    settings.setValue("optionSG2", QString::number(SG2));
    settings.setValue("DEMfill", QString::number(DEMfill, 'f', 2));
    settings.setValue("CatchmentSize", QString::number(CatchmentSize, 'f', 2));
    settings.setValue("chA", QString::number(chWidth, 'f', 1));
    settings.setValue("chB", QString::number(chB, 'f', 3));
    settings.setValue("chC", QString::number(chC, 'f', 3));
    settings.setValue("chD", QString::number(chDepth, 'f', 1));
    settings.setValue("chWidth", QString::number(chWidth, 'f', 1));
    settings.setValue("chDepth", QString::number(chDepth, 'f', 1));

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
    BaseDamsName = settings.value("BaseDams").toString();
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
    optionIncludeDams = settings.value("optionIncludeDams").toInt();

    refBulkDens = settings.value("refBulkDens").toDouble();
    refRootzone = settings.value("refRootzone").toDouble();
    initmoist = settings.value("initmoist").toDouble();
    SG1 = settings.value("optionSG1").toInt();
    SG2 = settings.value("optionSG2").toInt();
    DEMfill = settings.value("DEMfill").toDouble();
    CatchmentSize = settings.value("CatchmentSize").toDouble();
    chA = settings.value("chA").toDouble();
    chB = settings.value("chB").toDouble();
    chC = settings.value("chC").toDouble();
    chD = settings.value("chD").toDouble();
    chWidth = settings.value("chWidth").toDouble();
    chDepth = settings.value("chDepth").toDouble();
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
    BaseDamsName = lineEdit_Dams->text();
    MapsDirName = lineEdit_Maps->text();
    LULCDirName = lineEdit_LULC->text();
    LULCmapName = lineEdit_LULCMap->text();
    LULCtableName = lineEdit_LULCTable->text();
    ESPGnumber = E_ESPGnumber->text();
    ScriptFileName= lineEdit_Script->text();
    initmoist = spin_initmoist->value();
    refBulkDens = spin_refBD->value();
    refRootzone = spin_Rootzone->value();
    DEMfill = E_DEMfill->text().toDouble();
    CatchmentSize = E_catchmentSize->text().toDouble();
    //chA = spin_chA->value();
    chB = spin_chB->value();
    chC = spin_chC->value();
    chWidth = spin_chWidth->value();
    chDepth = spin_chDepth->value();
    chBaseflow = spin_chBaseflow->value();

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
    optionPruneBranch = checkBox_pruneBranch->isChecked() ? 1 : 0;
    optionIncludeDams = checkBox_createDams->isChecked() ? 1 : 0;
    optionUserOutlets = radioButton_OutletMultiple->isChecked() ? 1 : 0;
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
    //spin_chA->setValue(chA);
    spin_chB->setValue(chB);
    spin_chC->setValue(chC);
    spin_chWidth->setValue(chWidth);
    spin_chDepth->setValue(chDepth);
    spin_chBaseflow->setValue(chBaseflow);
    spin_Rootzone->setValue(refRootzone);

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
    radioButton_OutletMultiple->setChecked(optionUserOutlets > 0);
    checkBox_pruneBranch->setChecked(optionPruneBranch > 0);
    checkBox_createDams->setChecked(optionIncludeDams > 0);
}

