#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    setupUi(this);

    CondaInstall = GetCondaEnvs();
    QStringList sss;
    sss << "0 - 5 cm" << "5 - 15 cm" << "15 - 30 cm" << "30 - 60 cm" << "60 - 120 cm" << "120 - 200 cm";
    comboBox_SGlayer1->addItems(sss);
    comboBox_SGlayer2->addItems(sss);

    label_16->setStyleSheet("background-image : url(:/Screenshot.png);");

    setupModel();

    getIni();
    ScriptDirName = QFileInfo(ScriptFileName).absolutePath();
    writeValuestoUI();
    readValuesfromUI();

    for (int i = 0; i < combo_envs->count(); i++){
        if (combo_envs->itemText(i) == CondaBaseDirName)
            combo_envs->setCurrentIndex(i);
    }
}

MainWindow::~MainWindow()
{
    readValuesfromUI();
    setIni(qApp->applicationDirPath()+"/LISEMdbase.ini");
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
            if (found)
                combo_envs->addItem(CondaBaseDirName+"/"+folders.at(i));
        }
        install = combo_envs->count() > 0;
    }
    return(install);
}

void MainWindow::on_toolButton_base_clicked()
{
    QStringList filters;
    BaseDirName = getFileorDir(lineEdit_Base->text(),"Select Base folder", filters, 0);
    if (!BaseDirName.isEmpty())
        lineEdit_Base->setText(BaseDirName);
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

void MainWindow::on_toolButton_LULC_clicked()
{
    QStringList filters({"GeoTiff maps(*.tif)","Any files (*)"});
    LULCDirName = getFileorDir(lineEdit_LULC->text(),"Select LULC folder", filters, 0);
    if (!LULCDirName.isEmpty())
        lineEdit_LULC->setText(LULCDirName);
}

void MainWindow::on_toolButton_LULCTable_clicked()
{
        QString tmp = LULCDirName+lineEdit_LULCTable->text();
    QStringList filters({"Table (*.tbl *.txt *.csv)","Any files (*)"});
    LULCtableName = getFileorDir(tmp,"Select LULC table", filters, 1);
    if (!LULCtableName.isEmpty())
        lineEdit_LULCTable->setText(LULCtableName);
}

void MainWindow::on_toolButton_LULCMap_clicked()
{
    QString tmp = LULCDirName+lineEdit_LULCMap->text();
    QStringList filters({"GeoTiff (*.tif)","Any files (*)"});
    LULCmapName = getFileorDir(tmp,"Select LULC map", filters, 1);
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


void MainWindow::on_toolButton_CheckAll_toggled(bool checked)
{
    checkBox_DEM->setChecked(checked);
    checkBox_Channels->setChecked(checked);
    checkBox_LULC->setChecked(checked);
    checkBox_Infil->setChecked(checked);
    checkBox_Soilgrids->setChecked(checked);
    checkBox_userefBD->setChecked(checked);
    checkBox_erosion->setChecked(checked);
    spin_initmoist->setValue(0.1);
    spin_refBD->setValue(1350);
}

void MainWindow::on_toolButton_clear_clicked()
{
    text_out->clear();
}

// select a file or directory
// doFile = 0: select a directory;
// dofile = 1 select a file and return file name only;
// dofile = 2 return filename wioth full path
QString MainWindow::getFileorDir(QString inputdir,QString title, QStringList filters, int doFile)
{
    QFileDialog dialog;
    QString dirout = inputdir;
    if (doFile > 0) {
        dialog.setNameFilters(filters);
        dialog.setDirectory(QFileInfo(inputdir).absoluteDir());
        dialog.setFileMode(QFileDialog::ExistingFile);
    } else {
        filters.clear();
        dialog.setNameFilters(filters);
        dialog.setDirectory(QDir(inputdir));
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
        dirout = dialog.selectedUrls().at(0).path();
        dirout.remove(0,1);
        if (dirout.lastIndexOf('/') != dirout.length())
            dirout = dirout + "/";
    }

    return dirout;
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
}

void MainWindow::on_checkBox_Soilgrids_toggled(bool checked)
{
    SGoptions->setEnabled(checked);
}

void MainWindow::on_toolButton_clicked()
{
    QString filename;
    filename=":/help1.html";
    QFile file(filename);
    file.open(QFile::ReadOnly | QFile::Text);
    QTextStream stream(&file);
    QTextEdit *helptxt = new QTextEdit;
    helptxt->setHtml(stream.readAll());

    QTextEdit *view = new QTextEdit(helptxt->toHtml());
    view->createStandardContextMenu();
    view->setWindowTitle("Option help");
    view->setMinimumWidth(640);
    view->setMinimumHeight(480);
    view->setAttribute(Qt::WA_DeleteOnClose);

    view->show();
}
