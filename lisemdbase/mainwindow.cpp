#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    setupUi(this);

    CondaInstall = GetCondaEnvs();

    setupModel();
    lineEdit_Script->setText("C:/prgc/lisempy/inputlisem0.7options.py");
    lineEdit_Base->setText("C:/CRCLisem/Base/");
    lineEdit_baseDEM->setText("dem0.map");
    lineEdit_baseChannel->setText("chanmask0.map");
    lineEdit_Maps->setText("C:/CRCLisem/maps/");
    lineEdit_LULC->setText("C:/data/India/Decadal_LULC_India_1336/data/LULC_2005.tif");
    lineEdit_LULCTable->setText("ludata.tbl");
    QStringList sss;

    sss << "0 - 5 cm" << "5 - 15 cm" << "15 - 30 cm" << "30 - 60 cm" << "60 - 120 cm" << "120 - 200 cm";

    comboBox_SGlayer1->addItems(sss);
    comboBox_SGlayer2->addItems(sss);

    comboBox_SGlayer1->setCurrentIndex(2);
    comboBox_SGlayer2->setCurrentIndex(4);
    BaseDirName = lineEdit_Base->text();
    MapsDirName = lineEdit_Maps->text();
    LULCmapName = lineEdit_LULC->text();
    LULCDirName = QFileInfo(LULCmapName).absolutePath();
    LULCtableName = lineEdit_LULCTable->text();
    BaseChannelName = lineEdit_baseChannel->text();
    BaseDEMName = lineEdit_baseDEM->text();

}

bool MainWindow::GetCondaEnvs()
{
    bool install = false;
    QString name = qgetenv("USER");
    if (name.isEmpty())
        name = qgetenv("USERNAME");
    CondaBaseDirName = QString("c:/Users/" +name + "/miniconda3/envs");
    if (QFileInfo(CondaBaseDirName).dir().exists()) {
        QDir const source(CondaBaseDirName);
        QStringList const folders = source.entryList(QDir::NoDot | QDir::NoDotDot | QDir::Dirs);
        for (int i = 0; i < folders.size(); i++) {
            QString str = CondaBaseDirName+"/"+folders.at(i)+"/python.exe";
            QString str1 = CondaBaseDirName+"/"+folders.at(i)+"/Library/bin/pcrcalc.exe";
            bool found = QFileInfo(str).exists() && QFileInfo(str1).exists();
            // qDebug() << str;
            if (found)
                combo_envs->addItem(CondaBaseDirName+"/"+folders.at(i));
        }
        install = combo_envs->count() > 0;
    }
    return(install);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_toolButton_base_clicked()
{
    QStringList filters({"PCRaster map (*.map)","Any files (*)"});
    BaseDirName = getFileorDir(lineEdit_Base->text(),"Select Base folder", filters, false);
    if (!BaseDirName.isEmpty())
        lineEdit_Base->setText(BaseDirName);
}

void MainWindow::on_toolButton_maps_clicked()
{
    QStringList filters({"PCRaster maps (*.map)","Any files (*)"});
    MapsDirName = getFileorDir(lineEdit_Maps->text(),"Select Maps folder", filters, false);
    if (!MapsDirName.isEmpty())
        lineEdit_Maps->setText(MapsDirName);

}

void MainWindow::on_toolButton_script_clicked()
{
    ScriptFileName = lineEdit_Script->text();
    QStringList filters({"Python (*.py)","Any files (*)"});

    ScriptFileName = getFileorDir(ScriptFileName,"Select python script", filters, true);
    qDebug() << ScriptFileName;
    if (!ScriptFileName.isEmpty())
        lineEdit_Script->setText(ScriptFileName);
}

void MainWindow::on_toolButton_LULC_clicked()
{
    QStringList filters({"GeoTiff maps(*.tif)","Any files (*)"});
    LULCmapName = getFileorDir(lineEdit_LULC->text(),"Select LULC map", filters, true);
    if (!LULCmapName.isEmpty())
        lineEdit_LULC->setText(LULCmapName);
    LULCDirName = QFileInfo(LULCmapName).absoluteDir().absolutePath();
}

void MainWindow::on_toolButton_LULCTable_clicked()
{
    QStringList filters({"Table (*.tbl *.txt *.csv)","Any files (*)"});
    LULCtableName = getFileorDir(lineEdit_LULCTable->text(),"Select LULC table", filters, true);
    if (!LULCtableName.isEmpty())
        lineEdit_LULCTable->setText(LULCtableName);
  //  LULCDirName = QFileInfo(LULCtableName).absoluteDir().absolutePath();

}


void MainWindow::on_toolButton_baseDEM_clicked()
{
    QString tmp = BaseDirName+lineEdit_baseDEM->text();
    QStringList filters({"PCRaster maps (*.map)","Any files (*)"});
    tmp = getFileorDir(tmp,"Select Base DEM", filters, true);
    BaseDEMName = QFileInfo(tmp).fileName();
    if (!BaseDEMName.isEmpty())
        lineEdit_baseDEM->setText(BaseDEMName);
}

void MainWindow::on_toolButton_baseChannel_clicked()
{
    QString tmp = BaseDirName+lineEdit_baseChannel->text();
    QStringList filters({"PCRaster maps (*.map)","Any files (*)"});
    tmp = getFileorDir(tmp,"Select Channel mask", filters, true);
    BaseChannelName = QFileInfo(tmp).fileName();
    if (!BaseChannelName.isEmpty())
        lineEdit_baseChannel->setText(BaseChannelName);
}


void MainWindow::on_toolButton_CheckAll_toggled(bool checked)
{
    checkBox_DEM->setChecked(checked);
    checkBox_Channels->setChecked(checked);
    checkBox_LULC->setChecked(checked);
    checkBox_Infil->setChecked(checked);
    checkBox_Soilgrids->setChecked(checked);
}

void MainWindow::on_toolButton_clear_clicked()
{
    text_out->clear();
}


void MainWindow::setPyOptions()
{
    QSettings settings(qApp->applicationDirPath()+"/lisemdbaseoptions.cfg",QSettings::IniFormat);
    settings.clear();
    //settings.setValue("CondaDirectory", CondaBaseDirName);
    settings.setValue("BaseDirectory", BaseDirName);
    settings.setValue("MapsDirectory", MapsDirName);
    settings.setValue("LULCDirectory", LULCDirName);
    settings.setValue("LULCmap", LULCmapName);
    settings.setValue("LULCtable", LULCtableName);
    settings.setValue("optionDEM", checkBox_DEM->isChecked() ? "1":"0");
    settings.setValue("optionChannels", checkBox_Channels->isChecked() ? "1":"0");
    settings.setValue("optionInfil", checkBox_Infil->isChecked() ? "1":"0");
    settings.setValue("optionSG", checkBox_Soilgrids->isChecked() ? "1":"0");
    settings.setValue("optionLULC", checkBox_LULC->isChecked() ? "1":"0");
    int i = comboBox_SGlayer1->currentIndex();
    settings.setValue("optionSG1", QStringLiteral("%1").arg(i));
    i = comboBox_SGlayer2->currentIndex();
    settings.setValue("optionSG2", QStringLiteral("%1").arg(i));
    settings.sync();
}

QString MainWindow::getFileorDir(QString inputdir,QString title, QStringList filters, bool doFile)
{
    QFileDialog dialog;
    dialog.setNameFilters(filters);
    QString dirout = inputdir;
    if (doFile) {
        dialog.setDirectory(QFileInfo(inputdir).absoluteDir());
        dialog.setFileMode(QFileDialog::ExistingFile);
    } else {
        dialog.setDirectory(QDir(inputdir));
        dialog.setFileMode(QFileDialog::DirectoryOnly);
    }

    dialog.setOption(QFileDialog::DontUseNativeDialog, true);
    dialog.setOption(QFileDialog::ShowDirsOnly, false);
    dialog.setLabelText(QFileDialog::LookIn,title);
    dialog.exec();

    if (doFile) {
        dirout = "";
        if (dialog.selectedFiles().count() > 0)
            dirout = dialog.selectedFiles().at(0);
    } else
        dirout = QDir::toNativeSeparators(dialog.directory().absolutePath());
    return dirout;//.absolutePath();
}

