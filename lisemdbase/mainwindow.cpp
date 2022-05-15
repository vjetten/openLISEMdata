#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    setupUi(this);
//resize(QDesktopWidget().availableGeometry(this).size() * 0.9);

  //  setMinimumSize(1280, 800);
setWindowState(Qt::WindowMaximized);
    CondaInstall = GetCondaEnvs();

    QStringList sss;
    sss << "0 - 5 cm" << "5 - 15 cm" << "15 - 30 cm" << "30 - 60 cm" << "60 - 120 cm" << "120 - 200 cm";
    comboBox_SGlayer1->addItems(sss);
    comboBox_SGlayer2->addItems(sss);
    dailyA = 0.6162;
    dailyB = 0.8909;

    label_16->setStyleSheet("background-image : url(:/Screenshot.png);");

    setupModel();

    combo_iniName->clear();
    combo_iniName->setDuplicatesEnabled(false);

    getIniStart();

    QString s = combo_iniName->currentText();
    if (QFileInfo(s).exists())
    {
        getIni(s);

        writeValuestoUI();
        readValuesfromUI();
    }

    for (int i = 0; i < combo_envs->count(); i++){
        if (combo_envs->itemText(i) == CondaBaseDirName)
            combo_envs->setCurrentIndex(i);
    }

    tabWidgetOptions->setCurrentIndex(0);
    tabWidgetOptions->removeTab(4);

    QFont codeFont("Consolas", 8, QFont::Normal);
    tableViewLULC->setFont(codeFont);
    tableViewOutlets->setFont(codeFont);
    text_out->setFont(codeFont);

    //findDPIscale();
    //groupBox_ETdata1->setVisible(false);
    //groupBox_NDVIdata->setVisible(false);
}

MainWindow::~MainWindow()
{
    setIniStart();
}


void MainWindow::findDPIscale()
{
    QRect rect = QGuiApplication::primaryScreen()->availableGeometry();
    int _H = rect.height();
    if (_H > 600) {
        genfontsize = -1;//12;
    }
    if (_H > 800) {
        genfontsize = 0;//12;
    }
    if (_H > 1080-5) {
        genfontsize = 1;// 14;
    }
    if (_H > 1440) {
        genfontsize = 2;//12;
    }

    const QWidgetList allWidgets = QApplication::allWidgets();
    for (QWidget *widget : allWidgets) {
        QFont font = widget->font();
        //qDebug() << font;
        int ps = 7 + genfontsize;
        font.setPointSize(ps);
        widget->setFont(font);
        widget->update();
    }
}


bool MainWindow::GetCondaEnvs()
{
    QStringList folders;
    QString name = qgetenv("USERPROFILE");
    combo_envs->clear();

    name.replace("\\","/");
    name = name+"/.conda/environments.txt";

    if (QFileInfo(name).exists()) {
        QFile fin(name);

        if (fin.open(QIODevice::ReadOnly | QIODevice::Text)){
            while (!fin.atEnd())
            {
                QString S = fin.readLine();
                if (S.contains("envs")) {
                    S.remove(QChar('\n'));
                    S.replace("\\","/");
                    S = S + "/";
                    folders << S;
                }
            }
        }
        fin.close();
    } else {
        WarningMsg("No conda environment found.");
        return false;
    }

    for (int i = 0; i < folders.size(); i++) {
        QString str = folders.at(i)+"python.exe";
        QString str1 = folders.at(i)+"Library/bin/pcrcalc.exe";
        QString str2 = folders.at(i)+"Library/bin/gdalinfo.exe";
        bool pythonfound = QFileInfo(str).exists();
        bool pcrasterfound = QFileInfo(str1).exists();
        bool gdalfound = QFileInfo(str2).exists();

        if (pythonfound && pcrasterfound && gdalfound)
            combo_envs->addItem(folders.at(i));
        else {
            QString error = "";
            if (!pythonfound) error = QString("Python not found in Anaconda environment "+folders.at(i)+"\nThis environment is ignored.");
            else
                if (!pcrasterfound) error = QString("PCRaster not found in Anaconda environment "+folders.at(i)+"\nThis environment is ignored.");
                else
                    if (!gdalfound) error = QString("GDAL not found in Anaconda environment "+folders.at(i)+"\nThis environment is ignored.");
            //WarningMsg(error);
        }
    }
    if (combo_envs->count() > 0)
        CondaBaseDirName = combo_envs->currentText();
    else
        WarningMsg("No valid conda installation found.");

    return(combo_envs->count() > 0);
}

// does not woirk for non english PCs
bool MainWindow::GetCondaAllEnvs(int cda)
{
    bool install = false;
    QString name = qgetenv("USERPROFILE");

    if (cda == 0) {
        CondaBaseDirName = name + "/Miniconda3/envs";
    }
    if (cda == 1) {
        CondaBaseDirName = name + "/Anaconda3/envs";
    }
    if (cda == 2) {
        CondaBaseDirName = QString("c:/ProgramData/Miniconda3/envs");
    }
    if (cda == 3) {
        CondaBaseDirName = QString("c:/ProgramData/Anaconda3/envs");
    }
    if (QFileInfo(CondaBaseDirName).dir().exists()) {
        QDir const source(CondaBaseDirName);
        QStringList const folders = source.entryList(QDir::NoDot | QDir::NoDotDot | QDir::Dirs);
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
    QString startdir = QFileInfo(inputdir).absoluteDir().absolutePath();
    qDebug() <<"dir" << inputdir<< startdir ;
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
    QString tmp = lineEdit_LULCTable->text();
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
    //QString tmp = LULCDirName+lineEdit_LULCMap->text();
    QString tmp = lineEdit_LULCMap->text();
    QStringList filters({"GeoTiff or PCRaster (*.tif *.map)","Any files (*)"});
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
    BaseOutletsName = getFileorDir(tmp,"Select outlet(s) map", filters, 1);
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


void MainWindow::on_toolButton_userWatersheds_clicked()
{
    QString tmp = BaseDirName+lineEdit_userWatersheds->text();
    QStringList filters({"PCRaster maps (*.map)","Any files (*)"});
    WatershedsName = getFileorDir(tmp,"Select watershed map", filters, 2);
    if (!WatershedsName.isEmpty())
        lineEdit_userWatersheds->setText(WatershedsName);
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
    setIni(combo_iniName->currentText(), false);
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

    Process->kill();
    text_out->appendPlainText("User interrupt");

    text_out->clear();

//    if (LULCNames.isEmpty()) {
//        LULCNames = QString(qApp->applicationDirPath()+"/lulcnames.ini");
//        lineEdit_LULCNames->setText(LULCNames);
//    }

    int ncol = 6;
    int nrow = 0;
    int i = 0;
    model = new QStandardItemModel( nrow, ncol, this );
   // model->setHorizontalHeaderItem( i++, new QStandardItem("LULC type"));
    model->setHorizontalHeaderItem( i++, new QStandardItem("#"));
    model->setHorizontalHeaderItem( i++, new QStandardItem("Random\nRoughness (cm)"));
    model->setHorizontalHeaderItem( i++, new QStandardItem("Manning's n\n (-)"));
    model->setHorizontalHeaderItem( i++, new QStandardItem("Plant Height\n (m)"));
    model->setHorizontalHeaderItem( i++, new QStandardItem("Plant Cover\n (-)"));
    model->setHorizontalHeaderItem( i++, new QStandardItem("Density\n factor (0.9-1.2)"));
    model->setHorizontalHeaderItem( i++, new QStandardItem("Smax type\n (1-8)"));
    model->setHorizontalHeaderItem( i, new QStandardItem("Add. Cohesion\n (kPa)"));
    tableViewLULC->setModel(model);

    LULCNNtableName.clear();
    fillLULCTable();
    copyLULCTable();

    ncol = 3;
    nrow = 0;
    modelOutlets = new QStandardItemModel( nrow, ncol, this );
    modelOutlets->setHorizontalHeaderItem( 0, new QStandardItem("Channel \nwidth (m)"));
    modelOutlets->setHorizontalHeaderItem( 1, new QStandardItem("Channel \nDepth (m)"));
    modelOutlets->setHorizontalHeaderItem( 2, new QStandardItem("Channel \nBaseflow (m3/s)"));
    tableViewOutlets->setModel(modelOutlets);

    fillOutletsTable();
}

void MainWindow::on_toolButton_saveas_clicked()
{
    QString fileName = QFileDialog::getSaveFileName(this, "Save File as ini",
                               qApp->applicationDirPath(),
                               "*.ini");
    if (!fileName.isEmpty()) {
        readValuesfromUI();
        setIni(fileName, false);
        combo_iniName->insertItem(0, fileName);
        combo_iniName->setCurrentIndex(0);
    }
}

void MainWindow::on_toolButton_resetRain_clicked()
{
    spin_conversionmm->setValue(10);
    spin_timeinterval->setValue(30);
    spin_interpolation->setValue(1);
    spin_dailyA->setValue(0.6261);
    spin_dailyB->setValue(0.8909);
}

void MainWindow::on_toolButton_resetsoil_clicked()
{
    spin_Rootzone->setValue(0.6);
    spin_MaxSoildepth->setValue(5.0);
    spin_refBD->setValue(1350);
    //spin_refBD2->setValue(1350);
    spin_initmoist->setValue(0);

    checkBox_SGInterpolation->setChecked(false);
    checkBox_noGravel->setChecked(true);
    checkBox_Soilgrids->setChecked(false);
    checkBox_userefBD->setChecked(true);
    //checkBox_userefBD2->setChecked(true);
    checkBox_useLUdensity->setChecked(true);
    checkBox_erosion->setChecked(true);
    checkBox_D50->setChecked(true);
    checkBox_ChannelsNoErosion->setChecked(true);
}

void MainWindow::on_toolButton_CheckAll_clicked()
{
    spin_initmoist->setValue(0.0);
    spin_refBD->setValue(1350);
    //E_DEMfill->setText(QString::number(10,'f',1));
    spin_DEMfill->setValue(10);
    spin_chB->setValue(0.459);
    spin_chC->setValue(0.300);
    spin_chWidth->setValue(500.0);
    spin_chDepth->setValue(10.0);
    spin_chBaseflow->setValue(0.0);


    bool checked = true;
    checkBox_DEM->setChecked(checked);
    checkBox_Channels->setChecked(checked);
    checkBox_LULC->setChecked(checked);
    checkBox_Infil->setChecked(checked);
    checkBox_erosion->setChecked(checked);
//    checkBox_D50->setChecked(checked);
//    checkBox_ChannelsNoErosion->setChecked(checked);
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


void MainWindow::on_checkBox_createRainfall_clicked(bool checked)
{
    groupBox_raindata->setEnabled(checked);
    groupBox_dailyraindata->setEnabled(checked);
}


void MainWindow::on_toolButton_GPMpy_clicked()
{
    QStringList filters({"Python (*.py)","Any files (*)"});
    RainScriptFileName = getFileorDir(RainScriptFileName,"Select python script", filters, 2);
    if (!RainScriptFileName.isEmpty())
        lineEdit_GPMpy->setText(RainScriptFileName);
}


void MainWindow::on_toolButton_GPMin_clicked()
{
    QStringList filters;
    RainBaseDirName = getFileorDir(lineEdit_GPMdir->text(),"Select GPM Rain folder", filters, 0);
    if (!RainBaseDirName.isEmpty())
        lineEdit_GPMdir->setText(RainBaseDirName);
}


void MainWindow::on_toolButton_GPMout_clicked()
{
    QStringList filters;
    RainDirName = getFileorDir(lineEdit_Maps->text(),"Select Rain folder", filters, 0);
    if (!RainDirName.isEmpty())
        lineEdit_RainfallDir->setText(RainDirName);
}


void MainWindow::on_checkBox_createDams_clicked(bool checked)
{
    lineEdit_Dams->setEnabled(checked);
    toolButton_Dams->setEnabled(checked);
}


void MainWindow::on_toolButton_GPMrefmap_clicked()
{
    QString tmp = BaseDirName+lineEdit_GPMrefmap->text();
    QStringList filters({"PCRaster maps (*.map)","Any files (*)"});
    RainRefName = getFileorDir(tmp,"Select reference map for resmapling", filters, 1);
    if (!RainRefName.isEmpty())
        lineEdit_GPMrefmap->setText(RainRefName);
}





void MainWindow::on_toolButton_dailyRain_clicked()
{
    QStringList filters({"Text (*.txt)","Any files (*)"});
    RainDailyFilename = getFileorDir(RainDirName,"Select file with daily rainfall", filters, 2);
    if (!RainDailyFilename.isEmpty())
        lineEdit_RainDailyFilename->setText(RainDailyFilename);
}


bool MainWindow::convertDailyPrecipitation()
{
    QFile filein(RainDailyFilename);
    if (RainDailyFilename.isEmpty() || !QFileInfo(RainDailyFilename).exists())
        return false;

    filein.open(QIODevice::ReadOnly | QIODevice::Text);


    QStringList sl;
    while (!filein.atEnd()) {
        QString S = filein.readLine();
        if (!S.trimmed().isEmpty())
        {
            sl << S;
        }
    }
    filein.close();

    QString fno;
    if (RainFilenameHour != lineEdit_RainFilenameHour->text())
        fno = RainDirName+lineEdit_RainFilenameHour->text();
    else
        fno = RainDirName+RainFilenameHour;
    QFile fileout(fno);
    qDebug() << fno;
    fileout.open(QIODevice::WriteOnly | QIODevice::Text);
    QTextStream eout(&fileout);
    eout.setRealNumberPrecision(2);
    eout.setFieldWidth(8);
    eout.setRealNumberNotation(QTextStream::FixedNotation);

    eout << "#generated from daily rainfall\n";
    eout << "2\n";
    eout << "time (ddd:mmmm)\n";
    eout << "P (mm/h)\n";
    //parsing
    for (int i = 4; i < sl.count(); i++) {
        QStringList line = sl.at(i).split(QRegExp("\\s+"));
        int day = line.at(0).toInt();
        double P = line.at(1).toDouble();
        if (P >0) {

//        double I1 = dailyA*qPow(P,dailyB);
//        double I2 = I1/2;
//        double I3 = I2/2;
//        double I4 = I3/2;
//        double I5 = I4/2;
//        double I6 = I5/2;
//        double I6 = I5/2;
        double I[11];
        double sum = 0;

        for (int i = 0; i < 11; i++) {
            I[i] = P/12.0*dailyA*qPow(i+0.5,dailyB);
            sum += I[i];
                   // qDebug()  <<i << I[i] << sum << P;
        }
        double dt = sum > 0 ? 60*P/sum : 60;

       // int hour = 11;//qrand() % ((15 + 1) - 3) + 3;
        int hour = QRandomGenerator::global()->bounded(9)+1;
        double start = hour*60;

        text_out->appendPlainText(QString("%1:%2").arg(day).arg(start,4,'f',0,'0'));
        for (int i = 0; i < 11; i++) {
            eout << QString("%1:%2 ").arg(day).arg(start+(i+1)*dt,4,'f',0,'0') << I[i] << "\n";

        }
        eout << QString("%1:%2 ").arg(day).arg(start+12*dt,4,'f',0,'0') << "0.00\n";
//        eout << QString("%1:%2 ").arg(day).arg(start+j*dt,4,'f',0,'0') << I3 << "\n";j++;
//        eout << QString("%1:%2 ").arg(day).arg(start+j*dt,4,'f',0,'0') << I1 << "\n";j++;
//        eout << QString("%1:%2 ").arg(day).arg(start+j*dt,4,'f',0,'0') << I2 << "\n";j++;
//        eout << QString("%1:%2 ").arg(day).arg(start+j*dt,4,'f',0,'0') << I4 << "\n";j++;
//        eout << QString("%1:%2 ").arg(day).arg(start+j*dt,4,'f',0,'0') << I5 << "\n";j++;
//        eout << QString("%1:%2 ").arg(day).arg(start+j*dt,4,'f',0,'0') << I6 << "\n";j++;
//        eout << QString("%1:%2 ").arg(day).arg(start+j*dt,4,'f',0,'0') << "0.00\n";

        } else {
            eout << QString("%1:%2 ").arg(day).arg(720,4,'f',0,'0') << "0.00\n";
        }


    }
    fileout.close();
    return true;
}


void MainWindow::on_pushButton_generateGPMRain_clicked()
{
    runModel();
}


void MainWindow::on_pushButton_gennerateSyntheticRain_clicked()
{
    bool res = convertDailyPrecipitation();
    if (res)
        text_out->appendPlainText("Synthetic rainfall generated.");
    else
        text_out->appendPlainText("Error encountered, file not generated.");
}


void MainWindow::on_tabWidgetOptions_currentChanged(int index)
{
    toolButton_clear->setVisible(index < 3);
    toolButton_stop->setVisible(index < 3);
    pushButton_start->setVisible(index < 3);
}


void MainWindow::on_toolButton_stopGPM_clicked()
{
    Process->kill();
    text_out->appendPlainText("User interrupt");
}



void MainWindow::on_toolButton_userOutpoints_clicked()
{
    QString tmp = BaseDirName+lineEdit_userOutpoints->text();
    QStringList filters({"PCRaster maps (*.map)","Any files (*)"});
    BaseOutpointsName = getFileorDir(tmp,"Select outpoints map", filters, 1);
    if (!BaseOutpointsName.isEmpty())
        lineEdit_userOutpoints->setText(BaseOutpointsName);
}

