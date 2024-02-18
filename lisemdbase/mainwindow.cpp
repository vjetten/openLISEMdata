#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    setupUi(this);
    //  resize(QDesktopWidget().availableGeometry(this).size() * 0.9);

    //  setMinimumSize(1280, 800);
    //  setWindowState(Qt::WindowMaximized);
    CondaInstall = GetCondaEnvs();

    QStringList sss;
    sss << "0 - 5 cm" << "5 - 15 cm" << "15 - 30 cm" << "30 - 60 cm" << "60 - 120 cm" << "120 - 200 cm";
    comboBox_SGlayer1->addItems(sss);
    comboBox_SGlayer2->addItems(sss);

    sss.clear();
    sss << "Nearest Neighbourhood" << "Bilinear" << "Cubic";
    comboBox_Resample->addItems(sss);

    dailyA = 0.14;
    dailyB = -0.374;
    day0 = 1;
    dayn = 365;
    dt30min = 30;
    bufstart = false;

    label_16->setStyleSheet("background-image : url(:/Screenshot.png);");

    setupModel(); // read standard output etc

    combo_iniName->clear();
    combo_iniName->setDuplicatesEnabled(false);

    getIniStart();

    QString s = combo_iniName->currentText();
    if (QFileInfo(s).exists()) {

        getIni(s);
        comboBox_rainString->addItem("3B-HHR-L.MS.MRG.3IMERG");
        comboBox_rainString->addItem("YW_2017.002_");
        QSet<QString> uniqueItems;

        // Iterate through the items in the QComboBox
        for (int i = 0; i < comboBox_rainString->count(); ++i) {
            QString itemText = comboBox_rainString->itemText(i);
            uniqueItems.insert(itemText);
        }

        // Clear the QComboBox
        comboBox_rainString->clear();

        // Add unique items back to the QComboBox
        for (const QString &uniqueItem : uniqueItems) {
            comboBox_rainString->addItem(uniqueItem);
        }


      //  if (comboBox_rainString->count() == 0) {
//            comboBox_rainString->addItem("3B-HHR-L.MS.MRG.3IMERG");
//            comboBox_rainString->addItem("YW_2017.002_");
//        }

        comboBox_rainString->setCurrentIndex(0);//Text(RainString);
        writeValuestoUI();
        readValuesfromUI();
    }

    ScriptDirName = qApp->applicationDirPath()+"/scripts/";
    ScriptFileName = "lisemDBASEgenerator.py";
    if (QFileInfo(ScriptDirName+ScriptFileName).exists()) {
        lineEdit_Script->setText(ScriptDirName+ScriptFileName);
    }


    for (int i = 0; i < combo_envs->count(); i++){
        if (combo_envs->itemText(i) == CondaBaseDirName)
            combo_envs->setCurrentIndex(i);
    }

    if (QFileInfo(BaseDirName).exists())
        ProjectDirName = QDir(QDir(BaseDirName).absolutePath()+"/..").absolutePath()+"/";



    tabWidgetOptions->setCurrentIndex(0);
    tabWidgetOptions->removeTab(7);

    QFont codeFont("Consolas", 9, QFont::Normal);
    tableViewLULC->setFont(codeFont);
    tableViewOutlets->setFont(codeFont);
    text_out->setFont(codeFont);
    checkBox_noGravel->setVisible(false);
    findDPIscale();

    groupBox_dailyraindata->setVisible(false);
    groupBox_ERAdata->setVisible(false);
    //groupBox_ETdata1->setVisible(false);
    //groupBox_NDVIdata->setVisible(false);

}

MainWindow::~MainWindow()
{
    setIniStart();
}


void MainWindow::findDPIscale()
{
    //QRect rect = QGuiApplication::primaryScreen()->availableGeometry();
    int _H = QApplication::desktop()->height();
    //int _H = rect.height();
    if (_H > 600) {
        genfontsize = -1;//12;
    }
    if (_H > 800) {
        genfontsize = 0;//12;
    }
    if (_H > 1080) {
        genfontsize = 1;// 14;
    }
    if (_H > 1440) {
        genfontsize = 2;//12;
    }

    const QWidgetList allWidgets = QApplication::allWidgets();
    for (QWidget *widget : allWidgets) {
        QFont font = widget->font();
        //qDebug() << font;
        int ps = 8 + genfontsize;
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
// dofile = 2 return filename with full path
QString MainWindow::getFileorDir(QString inputdir,QString title, QStringList filters, int doFile)
{
    QFileDialog dialog;
    QString dirout = inputdir;
    // QString startdir = QFileInfo(inputdir).absoluteDir().absolutePath();
    //  qDebug() <<"dir" << inputdir<< startdir ;
    if (doFile > 0) {
        dialog.setNameFilters(filters);
        dialog.setDirectory(QFileInfo(inputdir).absoluteDir());
        dialog.setFileMode(QFileDialog::ExistingFile);
    } else {
        //  filters.clear();
        dialog.setNameFilters(filters);
        dialog.setDirectory(QFileInfo(inputdir).absoluteDir());
        if (doFile == 0)
            dialog.setFileMode(QFileDialog::DirectoryOnly);
        if (doFile == -1)
            dialog.setFileMode(QFileDialog::ExistingFile);
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
        //qDebug() << dirout;
    } else {
        QString S = dialog.selectedUrls().at(0).path();
        S.remove(0,1);
        qDebug() << QFileInfo(S).dir();
        if (!S.isEmpty()) {
            if (!QFileInfo(S).exists()) S = S + "/";
            dirout = QFileInfo(S).dir().absolutePath();
            if (dirout.contains("\\") && !dirout.endsWith("\\"))
                dirout=dirout+"\\";
            if (dirout.contains("/") && !dirout.endsWith("/"))
                dirout=dirout+"/";

        }

    }

    return dirout;
}

//====================================================================================


void MainWindow::on_comboBox_Resample_currentIndexChanged(int index)
{
    optionResample = index;
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
    //checkBox_SGAverage->setEnabled(checked);
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

void MainWindow::on_toolButton_stop_clicked()
{
    Process->kill();
    text_out->appendPlainText("User interrupt");
}


void MainWindow::on_combo_iniName_currentIndexChanged(int index)
{
    getIni(combo_iniName->currentText());

    comboBox_rainString->addItem("3B-HHR-L.MS.MRG.3IMERG");
    comboBox_rainString->addItem("YW_2017.002_");
    QSet<QString> uniqueItems;

    // Iterate through the items in the QComboBox
    for (int i = 0; i < comboBox_rainString->count(); ++i) {
        QString itemText = comboBox_rainString->itemText(i);
        uniqueItems.insert(itemText);
    }

    // Clear the QComboBox
    comboBox_rainString->clear();

    // Add unique items back to the QComboBox
    for (const QString &uniqueItem : uniqueItems) {
        comboBox_rainString->addItem(uniqueItem);
    }

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
    model->setHorizontalHeaderItem( i++, new QStandardItem("Add. Cohesion\n (kPa)"));
    model->setHorizontalHeaderItem( i  , new QStandardItem("Add. Org Mat\n (%)"));
    tableViewLULC->setModel(model);

    LULCNNtableName.clear();
    fillLULCTable();
    copyLULCTable();

    ncol = 6;
    nrow = 0;
    modelOutlets = new QStandardItemModel( nrow, ncol, this );
    modelOutlets->setHorizontalHeaderItem( 0, new QStandardItem("Outlet \nWidth (m)"));
    modelOutlets->setHorizontalHeaderItem( 1, new QStandardItem("Start \nwidth (m)"));
    modelOutlets->setHorizontalHeaderItem( 2, new QStandardItem("Outlet \nDepth (m)"));
    modelOutlets->setHorizontalHeaderItem( 3, new QStandardItem("Start \nDepth (m)"));
    modelOutlets->setHorizontalHeaderItem( 4, new QStandardItem("Manning n (-)"));
    modelOutlets->setHorizontalHeaderItem( 5, new QStandardItem("Baseflow (m3/s)"));
    tableViewOutlets->setModel(modelOutlets);

    fillOutletsTable();

}

void MainWindow::on_toolButton_resetRain_clicked()
{
    spin_conversionmm->setValue(0.1);
    spin_timeinterval->setValue(30);
    spin_interpolation->setValue(1);
    spin_dailyA->setValue(0.14);
    spin_dailyB->setValue(-0.374);
    spin_day0->setValue(152);
    spin_dayn->setValue(273);
}

void MainWindow::on_toolButton_resetsoil_clicked()
{
    spin_Rootzone->setValue(0.6);
    spin_MaxSoildepth->setValue(5.0);
    spin_refBD->setValue(1350);
    spin_initmoist->setValue(0);

    checkBox_SGInterpolation->setChecked(false);
    //checkBox_SGAverage->setChecked(false);
    checkBox_noGravel->setChecked(true);
    checkBox_Soilgrids->setChecked(false);
    checkBox_useLUdensity->setChecked(true);

}

void MainWindow::on_toolButton_resetEros_clicked()
{
    checkBox_D50->setChecked(true);
    checkBox_ChannelsNoErosion->setChecked(true);
}

void MainWindow::on_toolButton_resetInfra_clicked()
{
    spin_roofStore->setValue(1.0);
    checkBox_useDrums->setChecked(false);

    radioStormdrainCirc->setChecked(false);
    radioStormdrainRect->setChecked(true);
    spinDrainDiameter->setValue(0.65);
    spinDrainHeight->setValue(0.5);
    spinDrainWidth->setValue(0.5);
    spinDrainInletDistance->setValue(30);
    spinDrainInletSize->setValue(0.5);


}

void MainWindow::on_toolButton_CheckAll_clicked()
{
    spin_initmoist->setValue(0.0);
    spin_refBD->setValue(1350);
    spin_DEMfill->setValue(1);
    spin_chB->setValue(0.459);
    spin_chC->setValue(0.300);
    spin_chWidth->setValue(100.0);
    spin_chWidthS->setValue(2.0);
    spin_chDepth->setValue(10.0);
    spin_chDepthS->setValue(2.0);
    spin_chBaseflow->setValue(0.0);
    spin_chN->setValue(0.05);
    spin_corrOM->setValue(0.0);
    spin_Rootzone->setValue(0.6);
    spin_MaxSoildepth->setValue(5);

    //bool checked = true;
    //checkBox_DEM->setChecked(checked);
    //checkBox_Channels->setChecked(checked);
    //checkBox_LULC->setChecked(checked);
    //checkBox_Infil->setChecked(checked);
    //checkBox_erosion->setChecked(checked);
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


void MainWindow::on_checkBox_Rain_clicked(bool checked)
{
    scrollArea_Rain->setEnabled(checked);
    groupBox_raindata->setEnabled(checked);
    groupBox_dailyraindata->setEnabled(checked);
}


void MainWindow::on_checkBox_createDams_clicked(bool checked)
{
    lineEdit_Dams->setEnabled(checked);
    toolButton_Dams->setEnabled(checked);
}

//OBSOLETE
bool MainWindow::convertDailyPrecipitation()
{
    QFile filein(IDMFilename);
    if (IDMFilename.isEmpty() || !QFileInfo(IDMFilename).exists())
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
    if (RainFilenameHourIDM != lineEdit_RainFilenameHourIDM->text())
        fno = RainDirName+lineEdit_RainFilenameHourIDM->text();
    else
        fno = RainDirName+RainFilenameHourIDM;
    QFile fileout(fno);
    //qDebug() << fno;
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


void MainWindow::on_tabWidgetOptions_currentChanged(int index)
{
    //toolButton_clear->setVisible(index < 3);
    //    toolButton_stop->setVisible(index < 3);
    //    pushButton_start->setVisible(index < 3);
}


//void MainWindow::on_toolButton_stopGPM_clicked()
//{
//    Process->kill();
//    text_out->appendPlainText("User interrupt");
//}



//void MainWindow::on_toolButton_stopIDM_clicked()
//{
//    Process->kill();
//    text_out->appendPlainText("User interrupt");
//}


void MainWindow::on_pushButton_start_clicked()
{
    //  runGPMscript =false;
    //  runIDMscript = false;
    //   runOptionsscript = true;
    //   runERAscript = false;

    runModel();
}


//void MainWindow::on_pushButton_generateGPMRain_clicked()
//{
//    runGPMscript = true;
//    runERAscript = false;
//    runIDMscript = false;
//    runOptionsscript = false;
//    runModel();
//}


//void MainWindow::on_pushButton_gennerateSyntheticRain_clicked()
//{
//    runERAscript = false;
//    runGPMscript =false;
//    runIDMscript = true;
//    runOptionsscript = false;

//    runModel();
//}



//void MainWindow::on_pushButton_generateERARain_clicked()
//{
//    runERAscript = true;
//    runGPMscript =false;
//    runIDMscript = false;
//    runOptionsscript = false;

//    runModel();
//}


//void MainWindow::on_toolButton_stopERA_clicked()
//{
//    Process->kill();
//    text_out->appendPlainText("User interrupt");
//}

void MainWindow::on_checkBox_writeGaugeData_toggled(bool checked)
{
    gaugeFrame->setEnabled(checked);
}


void MainWindow::on_checkBox_useStormDrain_toggled(bool checked)
{
    widget_drain->setEnabled(checked);
}

