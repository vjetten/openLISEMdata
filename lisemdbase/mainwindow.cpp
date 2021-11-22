#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    setupUi(this);

    //CondaInstall = GetCondaEnvs();
    //CondaInstall = GetMiniCondaEnvs();

    CondaInstall = GetCondaAllEnvs(0);
    CondaInstall = GetCondaAllEnvs(1);
    CondaInstall = GetCondaAllEnvs(2);
    CondaInstall = GetCondaAllEnvs(3);

    QStringList sss;
    sss << "0 - 5 cm" << "5 - 15 cm" << "15 - 30 cm" << "30 - 60 cm" << "60 - 120 cm" << "120 - 200 cm";
    comboBox_SGlayer1->addItems(sss);
    comboBox_SGlayer2->addItems(sss);

    label_16->setStyleSheet("background-image : url(:/Screenshot.png);");

    setupModel();

    combo_iniName->clear();
    combo_iniName->setDuplicatesEnabled(false);

    getIniStart();
    /*
    QDirIterator it(qApp->applicationDirPath(), QStringList() << "*.ini", QDir::NoFilter);
    while (it.hasNext()) {
        QFile f(it.next());
        combo_iniName->addItem(f.fileName());
    }


    if (combo_iniName->currentText().isEmpty())
        combo_iniName->addItem(qApp->applicationDirPath()+"/lisemdbase.ini");
    */
    QString s = combo_iniName->currentText();
    if (QFileInfo(s).exists())
    {
        //lineEdit_iniName->setText(s);
        getIni(s);
        ScriptDirName = QFileInfo(ScriptFileName).absolutePath();
        writeValuestoUI();
        readValuesfromUI();
    }

    for (int i = 0; i < combo_envs->count(); i++){
        if (combo_envs->itemText(i) == CondaBaseDirName)
            combo_envs->setCurrentIndex(i);
    }


    tabWidgetOptions->setCurrentIndex(0);
    tabWidgetOptions->removeTab(3);

    int ncol = 6;
    int nrow = 0;
    model = new QStandardItemModel( nrow, ncol, this );  
    model->setHorizontalHeaderItem( 0, new QStandardItem("Random \nRoughness (cm)"));
    model->setHorizontalHeaderItem( 1, new QStandardItem("Manning's n\n (-)"));
    model->setHorizontalHeaderItem( 2, new QStandardItem("Plant Height\n (m)"));
    model->setHorizontalHeaderItem( 3, new QStandardItem("Plant Cover\n (-)"));
    model->setHorizontalHeaderItem( 4, new QStandardItem("Density\n factor (0.9-1.2)"));
    model->setHorizontalHeaderItem( 5, new QStandardItem("Smax type\n (1-7)"));
    model->setHorizontalHeaderItem( 6, new QStandardItem("Add. Cohesion\n (kPa)"));
    tableViewLULC->setModel(model);

    fillLULCTable();
    copyLULCTable();

    ncol = 3;
    nrow = 0;
    modelOutlets = new QStandardItemModel( nrow, ncol, this );
   // modelOutlets->setHorizontalHeaderItem( 0, new QStandardItem("Outlet \nname"));
   // modelOutlets->setHorizontalHeaderItem( 0, new QStandardItem("Outlet map \nnumber"));
    modelOutlets->setHorizontalHeaderItem( 0, new QStandardItem("Channel \nwidth (m)"));
    modelOutlets->setHorizontalHeaderItem( 1, new QStandardItem("Channel \nDepth (m)"));
    modelOutlets->setHorizontalHeaderItem( 2, new QStandardItem("Channel \nBaseflow (m3/s)"));
    tableViewOutlets->setModel(modelOutlets);

    fillOutletsTable();

}

MainWindow::~MainWindow()
{
    setIniStart();
}

bool MainWindow::GetCondaAllEnvs(int cda)
{
    bool install = false;
    QString name = qgetenv("USER");
    if (name.isEmpty())
        name = qgetenv("USERNAME");

    if (cda == 0) {
        CondaBaseDirName = QString("c:/Users/" +name + "/Miniconda3/envs");
    }
    if (cda == 1) {
        CondaBaseDirName = QString("c:/Users/" +name + "/Anaconda3/envs");
    }
    if (cda == 2) {
        CondaBaseDirName = QString("c:/ProgramData/Miniconda3/envs");
    }
    if (cda == 3) {
        CondaBaseDirName = QString("c:/ProgramData/Anaconda3/envs");
    }
    if (QFileInfo(CondaBaseDirName).dir().exists()) {
    //    qDebug() << CondaBaseDirName;
        QDir const source(CondaBaseDirName);
        QStringList const folders = source.entryList(QDir::NoDot | QDir::NoDotDot | QDir::Dirs);
  //      qDebug() << folders;
        for (int i = 0; i < folders.size(); i++) {
            QString str = CondaBaseDirName+"/"+folders.at(i)+"/python.exe";
            QString str1 = CondaBaseDirName+"/"+folders.at(i)+"/Library/bin/pcrcalc.exe";
            QString str2 = CondaBaseDirName+"/"+folders.at(i)+"/Library/bin/gdalinfo.exe";
            bool pythonfound = QFileInfo(str).exists();
            bool pcrasterfound = QFileInfo(str1).exists();
            bool gdalfound = QFileInfo(str2).exists();

            if (pythonfound && pcrasterfound && gdalfound)
                combo_envs->addItem(CondaBaseDirName+"/"+folders.at(i));
            else {
                QString error;
                if (!pythonfound) error = QString("Python not found in Anaconda environment "+folders.at(i)+"\nThis environment is ignored.");
                else
                if (!pcrasterfound) error = QString("PCRaster not found in Anaconda environment "+folders.at(i)+"\nThis environment is ignored.");
                else
                if (!gdalfound) error = QString("GDAL not found in Anaconda environment "+folders.at(i)+"\nThis environment is ignored.");

                QMessageBox msgBox;
                msgBox.setText(error);
                msgBox.exec();
            }
        }
        install = combo_envs->count() > 0;
    }
    return(install);
}


// select a file or directory
// doFile = 0: select a directory;
// dofile = 1 select a file and return file name only;
// dofile = 2 return filename wioth full path
QString MainWindow::getFileorDir(QString inputdir,QString title, QStringList filters, int doFile)
{
    QFileDialog dialog;
    QString dirout = inputdir;
    qDebug() <<"dir" << inputdir << QFileInfo(inputdir).absoluteDir();
    if (doFile > 0) {
        dialog.setNameFilters(filters);
        dialog.setDirectory(QFileInfo(inputdir).absoluteDir());
        dialog.setFileMode(QFileDialog::ExistingFile);
    } else {
        // get a file
        filters.clear();
        dialog.setNameFilters(filters);
        dialog.setDirectory(QFileInfo(inputdir).absoluteDir());
        dialog.setFileMode(QFileDialog::DirectoryOnly);
    }

    dialog.setLabelText(QFileDialog::LookIn,title);
    dialog.exec();

    if (doFile > 0) {
        dirout = "";
        if (dialog.selectedFiles().count() > 0)
            dirout = dialog.selectedFiles().at(0);
        if (doFile == 1)
            dirout = QFileInfo(dirout).fileName();
        if (doFile == 2)
            dirout = QFileInfo(dirout).absoluteFilePath();
        qDebug() << dirout;
    } else {
        QString S = dialog.selectedUrls().at(0).path();
        S.remove(0,1);
        if (!S.isEmpty())
            dirout = S;
        if (!dirout.endsWith('/') && !dirout.endsWith('\\'))
            dirout = dirout + "/";
    }

    return dirout;
}

//====================================================================================


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

void MainWindow::on_toolButton_OutletsTable_clicked()
{
    QString tmp = BaseDirName+lineEdit_userOutlets->text();
    QStringList filters({"Text table (*.tbl)","Any files (*)"});
    OutletstableName = getFileorDir(tmp,"Select outlet table", filters, 2);
    if (!OutletstableName.isEmpty())
        lineEdit_outletsTable->setText(OutletstableName);

    fillOutletsTable();
}
void MainWindow::on_toolButton_base_clicked()
{
    QStringList filters;
    QString S = lineEdit_Base->text();
    BaseDirName = getFileorDir(lineEdit_Base->text(),"Select Base folder", filters, 0);
    if (!BaseDirName.isEmpty())
        lineEdit_Base->setText(BaseDirName);
    else
        lineEdit_Base->setText(S);

}

void MainWindow::on_toolButton_maps_clicked()
{
    QStringList filters;
    MapsDirName = getFileorDir(lineEdit_Maps->text(),"Select Maps folder", filters, 0);
    if (!MapsDirName.isEmpty())
        lineEdit_Maps->setText(MapsDirName);

}

void MainWindow::on_toolButton_script_clicked()
{
    QStringList filters({"Python (*.py)","Any files (*)"});
    ScriptFileName = getFileorDir(ScriptFileName,"Select python script", filters, 2);
    if (!ScriptFileName.isEmpty())
        lineEdit_Script->setText(ScriptFileName);
}

void MainWindow::on_toolButton_LULCTable_clicked()
{
    //QString tmp = LULCDirName+lineEdit_LULCTable->text();
    QString tmp = lineEdit_LULCTable->text();
    QStringList filters({"Table (*.tbl *.txt *.csv)","Any files (*)"});
    LULCtableName = getFileorDir(tmp,"Select LULC table", filters, 2);
    if (!LULCtableName.isEmpty())
        lineEdit_LULCTable->setText(LULCtableName);

    if (!LULCtableName.isEmpty())
        fillLULCTable();
}

void MainWindow::on_toolButton_LULCMap_clicked()
{
    //QString tmp = LULCDirName+lineEdit_LULCMap->text();
    QString tmp = lineEdit_LULCMap->text();
    QStringList filters({"GeoTiff (*.tif)","Any files (*)"});
    LULCmapName = getFileorDir(tmp,"Select LULC map", filters, 2);
    if (!LULCmapName.isEmpty())
        lineEdit_LULCMap->setText(LULCmapName);
}

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
    BaseOutletsName = getFileorDir(tmp,"Select outlet map", filters, 2);
    if (!BaseOutletsName.isEmpty())
        lineEdit_userOutlets->setText(BaseOutletsName);
}

void MainWindow::on_toolButton_Dams_clicked()
{
    QString tmp = BaseDirName+lineEdit_Dams->text();
    QStringList filters({"PCRaster maps (*.map)","Any files (*)"});
    BaseDamsName = getFileorDir(tmp,"Select dams map", filters, 1);
    if (!BaseDamsName.isEmpty())
        lineEdit_Dams->setText(BaseDamsName);
}

void MainWindow::on_toolButton_clear_clicked()
{
    text_out->clear();
}

void MainWindow::on_comboBox_SGlayer1_currentIndexChanged(int index)
{
    SG1 = index;//comboBox_SGlayer1->currentIndex();
}

void MainWindow::on_comboBox_SGlayer2_currentIndexChanged(int index)
{
    SG2 = index;//comboBox_SGlayer2->currentIndex();
}

void MainWindow::on_checkBox_Infil_toggled(bool checked)
{
    infiloptions->setEnabled(checked);
    SGoptions->setEnabled(checked);
    checkBox_SGInterpolation->setEnabled(checked);
    checkBox_Soilgrids->setEnabled(checked);
}

void MainWindow::on_checkBox_Soilgrids_toggled(bool checked)
{
    SGoptions->setEnabled(checked);
}

void MainWindow::on_checkBox_DEM_toggled(bool checked)
{
    DEMoptions->setEnabled(checked);
}

void MainWindow::on_toolButton_SaveIni_clicked()
{
    readValuesfromUI();
    if (combo_iniName->currentText().isEmpty())
        combo_iniName->addItem(qApp->applicationDirPath()+"/lisemdbase.ini");
    QString sss = combo_iniName->currentText();
    qDebug() << sss;
    setIni(combo_iniName->currentText());
}

void MainWindow::on_toolButton_stop_clicked()
{
    Process->kill();
    text_out->appendPlainText("User interrupt");
}


void MainWindow::on_combo_iniName_currentIndexChanged(int index)
{
    getIni(combo_iniName->currentText());
    writeValuestoUI();
    readValuesfromUI();
}

void MainWindow::on_toolButton_saveas_clicked()
{
    QString fileName = QFileDialog::getSaveFileName(this, "Save File as ini",
                               qApp->applicationDirPath(),
                               "*.ini");
    if (!fileName.isEmpty()) {
        readValuesfromUI();
        setIni(fileName);
        combo_iniName->addItem(fileName);
    }
}

void MainWindow::on_toolButton_CheckAll_clicked()
{
    spin_initmoist->setValue(0.0);
    spin_refBD->setValue(1350);
    //E_DEMfill->setText(QString::number(10,'f',1));
    spin_DEMfill->setValue(10);
    E_catchmentSize->setText(QString::number(10000,'f',1));
    spin_chB->setValue(0.459);
    spin_chC->setValue(0.300);
    spin_chWidth->setValue(500.0);
    spin_chDepth->setValue(10.0);
    spin_chBaseflow->setValue(0.0);
    spin_Rootzone->setValue(0.6);

    bool checked = true;
    checkBox_DEM->setChecked(checked);
    checkBox_Channels->setChecked(checked);
    checkBox_LULC->setChecked(checked);
    checkBox_Infil->setChecked(checked);
    checkBox_Soilgrids->setChecked(checked);
    checkBox_userefBD->setChecked(checked);
    checkBox_useLUdensity->setChecked(!checked);
    checkBox_erosion->setChecked(checked);
    checkBox_D50->setChecked(checked);
}


void MainWindow::on_checkBox_useLUdensity_toggled(bool checked)
{
 //   checkBox_userefBD->setChecked(!checked);
}

void MainWindow::on_checkBox_userefBD_toggled(bool checked)
{
   // checkBox_useLUdensity->setChecked(!checked);
}


void MainWindow::on_radioButton_OutletSIngle_toggled(bool checked)
{
   widgetSingleWS->setEnabled(checked);
}

void MainWindow::on_radioButton_OutletMultiple_toggled(bool checked)
{
    widgetMultipleWS->setEnabled(checked);
}

void MainWindow::on_checkBox_erosion_toggled(bool checked)
{
    erosionoptions->setEnabled(checked);
}


