#include "mainwindow.h"



void MainWindow::on_toolButton_openIni_clicked()
{
    QStringList filters({"dbase ini file (*.ini)","Any files (*)"});
    QString S = combo_iniName->currentText();
    QString FileName = getFileorDir(S,"Select database ini file", filters, 2);
    if (!FileName.isEmpty()) {
        combo_iniName->insertItem(0,FileName);
        combo_iniName->setCurrentIndex(0);
        setIniStart();
    }
}


void MainWindow::on_toolButton_SaveIni_clicked()
{
    readValuesfromUI();
    if (combo_iniName->currentText().isEmpty())
        on_toolButton_saveas_clicked();
        //combo_iniName->addItem(qApp->applicationDirPath()+"/lisemdbase.ini");

    setIni(combo_iniName->currentText(), false);
}


void MainWindow::on_toolButton_saveas_clicked()
{
    QString fileName = QFileDialog::getSaveFileName(this, "Give a new project INI filename to save all options",
                               qApp->applicationDirPath(),
                               "*.ini");
    if (!fileName.isEmpty()) {
        readValuesfromUI();
        setIni(fileName, false);
        combo_iniName->insertItem(0, fileName);
        combo_iniName->setCurrentIndex(0);
    }
}


void MainWindow::on_toolButton_script_clicked()
{
    QStringList filters({"Python (*.py)","Any files (*)"});
    ScriptFileName = getFileorDir(ScriptFileName,"Select python script", filters, 2);
    if (!ScriptFileName.isEmpty())
        lineEdit_Script->setText(ScriptFileName);
}

//==============================================================================
void MainWindow::on_toolButton_base_clicked()
{
    QStringList filters;
    QString S = lineEdit_Base->text();
    BaseDirName = getFileorDir(lineEdit_Base->text(),"Select Base folder", filters, 0);
    if (!BaseDirName.isEmpty())
        lineEdit_Base->setText(BaseDirName);
    else
        lineEdit_Base->setText(S);

    if (!QFileInfo(ProjectDirName).exists())
        ProjectDirName = QDir(QDir(BaseDirName).absolutePath()+"/..").absolutePath()+"/";
}


void MainWindow::on_toolButton_maps_clicked()
{
    QString tmp = lineEdit_Maps->text();
    if (!QFileInfo(tmp).exists())
        tmp = ProjectDirName;
    QStringList filters;
    MapsDirName = getFileorDir(tmp,"Select Maps folder", filters, 0);
    if (!MapsDirName.isEmpty())
        lineEdit_Maps->setText(MapsDirName);

    if (!QFileInfo(ProjectDirName).exists())
        ProjectDirName = QDir(QDir(MapsDirName).absolutePath()+"/..").absolutePath()+"/";
}


void MainWindow::on_toolButton_GPMout_clicked()
{
    QString tmp = lineEdit_RainfallDir->text();
    if (!QFileInfo(tmp).exists())
        tmp = ProjectDirName;

    QStringList filters;
    RainDirName = getFileorDir(tmp,"Select Rain folder", filters, 0);
    if (!RainDirName.isEmpty())
        lineEdit_RainfallDir->setText(RainDirName);

    if (!QFileInfo(ProjectDirName).exists())
        ProjectDirName = QDir(QDir(RainDirName).absolutePath()+"/..").absolutePath()+"/";
}


//==============================================================================
void MainWindow::on_toolButton_baseDEM_clicked()
{
    QString tmp = BaseDirName+lineEdit_baseDEM->text();
    QStringList filters({"PCRaster maps (*.map)","Any files (*)"});
    BaseDEMName = getFileorDir(tmp,"Select Base DEM", filters, 1);
    if (!BaseDEMName.isEmpty())
        lineEdit_baseDEM->setText(BaseDEMName);
}


void MainWindow::on_toolButton_baseChannel_clicked()
{
    QString tmp = BaseDirName+lineEdit_baseChannel->text();
    QStringList filters({"PCRaster maps (*.map)","Any files (*)"});
    BaseChannelName = getFileorDir(tmp,"Select Channel mask", filters, 1);
    if (!BaseChannelName.isEmpty())
        lineEdit_baseChannel->setText(BaseChannelName);
}


void MainWindow::on_toolButton_userOutlets_clicked()
{
    QString tmp = BaseDirName+lineEdit_userOutlets->text();
    QStringList filters({"PCRaster maps (*.map)","Any files (*)"});
    BaseOutletsName = getFileorDir(tmp,"Select outlet(s) map", filters, 1);
    if (!BaseOutletsName.isEmpty())
        lineEdit_userOutlets->setText(BaseOutletsName);
}


void MainWindow::on_toolButton_userOutpoints_clicked()
{
    QString tmp = BaseDirName+lineEdit_userOutpoints->text();
    QStringList filters({"PCRaster maps (*.map)","Any files (*)"});
    BaseOutpointsName = getFileorDir(tmp,"Select outpoints map", filters, 1);
    if (!BaseOutpointsName.isEmpty())
        lineEdit_userOutpoints->setText(BaseOutpointsName);
}


void MainWindow::on_toolButton_OutletsTable_clicked()
{
    QString tmp = BaseDirName+lineEdit_userOutlets->text();
    QStringList filters({"Text table (*.tbl)","Any files (*)"});
    OutletstableName = getFileorDir(tmp,"Select outlet table", filters, 2);
    if (!OutletstableName.isEmpty())
        lineEdit_outletsTable->setText(OutletstableName);

    fillOutletsTable();
}


void MainWindow::on_toolButton_Dams_clicked()
{
    QString tmp = BaseDirName+lineEdit_Dams->text();
    QStringList filters({"PCRaster maps (*.map)","Any files (*)"});
    BaseDamsName = getFileorDir(tmp,"Select dams map", filters, 1);
    if (!BaseDamsName.isEmpty())
        lineEdit_Dams->setText(BaseDamsName);
}


void MainWindow::on_toolButton_userWatersheds_clicked()
{
    QString tmp = BaseDirName+lineEdit_userWatersheds->text();
    QStringList filters({"PCRaster maps (*.map)","Any files (*)"});
    WatershedsName = getFileorDir(tmp,"Select watershed map", filters, 2);
    if (!WatershedsName.isEmpty())
        lineEdit_userWatersheds->setText(WatershedsName);
}


//==============================================================================
void MainWindow::on_toolButton_LULCTable_clicked()
{

    QString tmp = lineEdit_LULCTable->text();
    if (!QFileInfo(tmp).exists())
        tmp = ProjectDirName;

    QStringList filters({"Table (*.tbl *.txt *.csv)","Any files (*)"});
    LULCtableName = getFileorDir(tmp,"Select LULC table", filters, 2);
    if (!LULCtableName.isEmpty())
        lineEdit_LULCTable->setText(LULCtableName);

    if (!LULCtableName.isEmpty()) {
        fillLULCTable();
        copyLULCTable();
    }
}


void MainWindow::on_toolButton_LULCMap_clicked()
{
    QString tmp = lineEdit_LULCMap->text();
    if (!QFileInfo(tmp).exists())
        tmp = ProjectDirName;

    QStringList filters({"GeoTiff or PCRaster (*.tif *.map)","Any files (*)"});
    LULCmapName = getFileorDir(tmp,"Select LULC map", filters, 2);
    if (!LULCmapName.isEmpty())
        lineEdit_LULCMap->setText(LULCmapName);

}


//==============================================================================
void MainWindow::on_toolButton_GPMpy_clicked()
{
    QStringList filters({"Python (*.py)","Any files (*)"});
    RainScriptFileName = getFileorDir(RainScriptFileName,"Select python script", filters, 2);
    if (!RainScriptFileName.isEmpty())
        lineEdit_GPMpy->setText(RainScriptFileName);
}


void MainWindow::on_toolButton_GPMin_clicked()
{
    QString tmp = lineEdit_GPMdir->text();
    if (!QFileInfo(tmp).exists())
        tmp = ProjectDirName;
    QStringList filters;
    RainBaseDirName = getFileorDir(tmp,"Select global GPM Data folder", filters, 0);
    if (!RainBaseDirName.isEmpty())
        lineEdit_GPMdir->setText(RainBaseDirName);

}


void MainWindow::on_toolButton_GPMrefmap_clicked()
{
    QString tmp = BaseDirName+lineEdit_GPMrefmap->text();
    QStringList filters({"PCRaster maps (*.map)","Any files (*)"});
    RainRefNameDEM = getFileorDir(tmp,"Select reference map for resampling", filters, 1);
    if (!RainRefNameDEM.isEmpty())
        lineEdit_GPMrefmap->setText(RainRefNameDEM);
}


void MainWindow::on_toolButton_dailyRain_clicked()
{
    QStringList filters({"NetCDF maps (*.nc)","Any files (*)"});
    IDMFilename = getFileorDir(IDMFilename,"Select IDM NetCDF map with daily rainfall", filters, 2);
    if (!IDMFilename.isEmpty())
        lineEdit_IDMFilename->setText(IDMFilename);
}


void MainWindow::on_IMDpy_clicked()
{
    QStringList filters({"Python (*.py)","Any files (*)"});
    IDMScriptFileName = getFileorDir(IDMScriptFileName,"Select python script", filters, 2);
    if (!IDMScriptFileName.isEmpty())
        lineEdit_IMDpy->setText(IDMScriptFileName);
}



void MainWindow::on_toolButtontoolButton_RainERA_clicked()
{

    QStringList filters({"NetCDF maps (*.nc)","Any files (*)"});
    ERAFilename = getFileorDir(ERAFilename,"Select IDM NetCDF map with daily rainfall", filters, 2);
    if (!ERAFilename.isEmpty())
        lineEdit_ERAFilename->setText(ERAFilename);
}


void MainWindow::on_ERApy_clicked()
{
    QStringList filters({"Python (*.py)","Any files (*)"});
    ERAScriptFileName = getFileorDir(ERAScriptFileName,"Select python script", filters, 2);
    if (!ERAScriptFileName.isEmpty())
        lineEdit_ERApy->setText(ERAScriptFileName);
}

