#include "mainwindow.h"

void MainWindow::setupModel()
{
    Process = new QProcess(this);
    Process->setReadChannel ( QProcess::StandardError );

    connect(Process, SIGNAL(readyReadStandardError()),this, SLOT(readFromStderr()) );
    connect(Process, SIGNAL(readyReadStandardOutput()),this, SLOT(readFromOutput()) );

    bufstart = false;
}


int MainWindow::checkNameandOption(QString name, bool option, QString message)
{
    //qDebug() << name;
    if (option && !QFileInfo(name).exists()) {
        QMessageBox::warning(this,"", message);
        return 1;
    } else
        return 0;

}

bool MainWindow::checkAllNames()
{
    int quit = 0;
    //if (ESPGnumber.isEmpty())

    quit += checkNameandOption(ScriptDirName + ScriptFileName, true, "Python Scripts not found."); // should not happen at this point
    quit += checkNameandOption(BaseDirName, true, "Base folder not found.");
    quit += checkNameandOption(MapsDirName, true, "Maps folder not found.");

    if (quit > 0)
        return false;

    quit += checkNameandOption(BaseDirName+BaseDEMName,  optionDEM == 1, "1. Catchment: DEM not found.");
    quit += checkNameandOption(BaseDirName+BaseChannelName,  optionDEM == 1, "1. Catchment: River map not found.");
    quit += checkNameandOption(BaseDirName+BaseOutletsName,  optionDEM == 1, "1. Catchment: Outlet map not found.");
    quit += checkNameandOption(BaseDirName+BaseOutpointsName,  optionDEM == 1, "1. Catchment: Observation point(s) map not found.");

    quit += checkNameandOption(BaseDirName+BaseCulvertsName,optionUseCulverts == 1 && optionDEM == 1,"2. Channels: Culverts map not found.");
    quit += checkNameandOption(BaseDirName+BaseDamsName    ,optionIncludeDams == 1 && optionDEM == 1,"2. Channels: Dams map not found.");
    quit += checkNameandOption(BaseDirName+WatershedsName  ,optionUserOutlets == 1 && optionDEM == 1,"2. Channels: Watersheds map not found.");
    quit += checkNameandOption(BaseDirName+OutletstableName,optionUserOutlets == 1 && optionDEM == 1,"2. Channels: Outlets map not found.");
    // vegetation stuff is not assumed to be in base dir so full pathnames already
    quit += checkNameandOption(LULCmapName  ,optionLULC == 1,"3. Land use: LULC map not found.");
    quit += checkNameandOption(LULCtableName,optionLULC == 1,"3. Land use: LULC table not found.");
    //qDebug() << NDVImapName << optionUseNDVI << optionLULC;
    quit += checkNameandOption(NDVImapName  ,optionUseNDVI == 1 && optionLULC == 1,"3. Land use: NDVI map not found.");
    quit += checkNameandOption(BaseDirName+buildingsSHPName,optionUseInfrastructure == 1,"7. Buildings: buildings shapefile not found.");
    quit += checkNameandOption(BaseDirName+roadsSHPName,optionUseInfrastructure == 1,"7. Buildings: roads shapefile not found.");

  //  quit += checkNameandOption(RainRefNameDEM     ,optionUseInfrastructure,"8. Rainfall: reference DEM for rainfall not found.");
    quit += checkNameandOption(RainBaseDirName    ,optionRain == 1,"8. Rainfall: Folder with GPM data (tif files) not found.");
    quit += checkNameandOption(RainDirName        ,optionRain == 1,"8. Rainfall: Output folder for rainfall maps not found.");
   // quit += checkNameandOption(RainFilename       ,optionRain == 1,"8. Rainfall: reference DEM for rainfall not found.");
    quit += checkNameandOption(RainGaugeFilename  ,optionRain == 1 && optionGaugeGPM == 1,"8. Rainfall: map with location(s) for GPM point output not found.");
   // quit += checkNameandOption(RainGaugeFilenameIn,optionRain == 1 && optionGaugeGPM == 1,"8. Rainfall: reference DEM for rainfall not found.");
    qDebug() << checkBox_Infil->isChecked() << checkBox_Soilgrids->isChecked() << QFileInfo(BaseDirName+"sand1.tif").exists();
    if(checkBox_Infil->isChecked() && !checkBox_Soilgrids->isChecked() && !QFileInfo(BaseDirName+"sand1.tif").exists()) {
         QMessageBox::warning(this,"", "4. Infiltration: WARNING Cannot find SOILGRIDS downloaded maps (sand1.tif etc.), make sure to check the dowload option.");
    }

    if (quit > 0)
        return false;

    return true;



//    if (!QFileInfo(RainRefNameDEM     ).exists() && optionUseInfrastructure)
//    if (!QFileInfo(RainBaseDirName    ).exists() && optionRain == 1)
//    if (!QFileInfo(RainDirName        ).exists() && optionRain == 1)
//    if (!QFileInfo(RainFilename       ).exists() && optionRain == 1)
//    if (!QFileInfo(RainGaugeFilename  ).exists() && optionRain == 1 && optionGaugeGPM == 1)
//    if (!QFileInfo(RainGaugeFilenameIn).exists() && optionRain == 1 && optionGaugeGPM == 1)
    //if (!QFileInfo(IDMFilename        ).exists() && optionRain == 1)
    //if (!QFileInfo(RainFilenameHourIDM).exists() && optionRain == 1)
    //if (!QFileInfo(ERAFilename        ).exists() && optionRain == 1)
    //if (!QFileInfo(RainFilenameHourERA).exists() && optionRain == 1)
}

/*
 *
CONDA_DEFAULT_ENV=lisem
CONDA_EXE=C:\Users\vjett\miniconda3\Scripts\conda.exe
CONDA_PREFIX=C:\Users\vjett\miniconda3\envs\lisem
CONDA_PREFIX_1=C:\Users\vjett\miniconda3
CONDA_PYTHON_EXE=C:\Users\vjett\miniconda3\python.exe
CONDA_SHLVL=2
GDAL_DATA=C:\Users\vjett\miniconda3\envs\lisem\Library\share\gdal
GDAL_DRIVER_PATH=C:\Users\vjett\miniconda3\envs\lisem\Library\lib\gdalplugins
GEOTIFF_CSV=C:\Users\vjett\miniconda3\envs\lisem\Library\share\epsg_csv

path +
C:\Users\vjett\miniconda3\envs\lisem;
C:\Users\vjett\miniconda3\envs\lisem\Library\mingw-w64\bin;
C:\Users\vjett\miniconda3\envs\lisem\Library\usr\bin;
C:\Users\vjett\miniconda3\envs\lisem\Library\bin;
C:\Users\vjett\miniconda3\envs\lisem\Scripts;
C:\Users\vjett\miniconda3\envs\lisem\bin;
C:\Users\vjett\miniconda3\condabin;

PROJ_DATA=C:\Users\vjett\miniconda3\envs\lisem\Library\share\proj
PROJ_NETWORK=ON
 */
void MainWindow::runModel()
{
    text_out->clear();
    text_out->insertPlainText(">>> Preparing python libraries\n");


    // add the env path names, copied from Spyder. Maybe overkill but it works
    QString condaenv = combo_envs->currentText();
    QStringList Sn = condaenv.split('/');
    QString envname = Sn.at(Sn.count()-2);

    QString condabase = QDir(condaenv+"/../..").absolutePath();
    QString condascripts = QDir(condabase+"/Scripts").absolutePath();

    QProcessEnvironment env = QProcessEnvironment::systemEnvironment();
    env.insert("CONDA_DEAFULT_ENV",envname);
    env.insert("CONDA_EXE",condascripts+"conda.exe");
    env.insert("CONDA_PREFIX", condaenv);
    env.insert("CONDA_PREFIX_1", condabase);
    env.insert("CONDA_PYTHON_EXE",condabase+"/python.exe");
    env.insert("CONDA_SHLVL","2"); // 1 ?

    env.insert("USE_PATH_FOR_GDAL_PYTHON","YES");
    env.insert("CONDA_ACTIVATE_SCRIPT",condascripts+"/activate");
    env.insert("CONDA_ENV_PATH",condaenv);
    env.insert("CONDA_ENV_PYTHON",condaenv+"python.exe");

    env.insert("GDAL_DATA",condaenv+"Library/share/gdal");
    env.insert("GDAL_DRIVER",condaenv+"Library/share/gdal");
    env.insert("GDAL_DRIVER_PATH",condaenv+ "Library/lib/gdalplugins");
    env.insert("GEOTIFF_CSV",condaenv+"Library/share/epsg_csv");
    QString addpath = condaenv+";"
            +condaenv+"Library/bin/minw-w64/bin;"
            +condaenv+"Library/usr/bin;"
            +condaenv+"Library/bin;"
            +condaenv+"Scripts;"
            +condaenv+"bin;"
            +condaenv+"condabin;"
            +condaenv+"/Scripts;";

    env.insert("PATH", addpath + env.value("Path"));
    Process->setProcessEnvironment(env);

//    qDebug() << condabase ;
//    qDebug() << condascripts+ "/activate";
//    qDebug() << condaenv+"python.exe";
//    qDebug() << condabase+"/python.exe";
//    qDebug() << condaenv+"Library/share/gdal";


  //  if (runOptionsscript)
    createNNLULCTable();

    readValuesfromUI();

    if (!checkAllNames())
        return;

    QString Ss = qApp->applicationDirPath(); //QDir::tempPath()
    if (QFileInfo(Ss+"/lisemdbaseoptions.cfg").exists()) {
        QFile file (Ss+"/lisemdbaseoptions.cfg");
        file.remove();
    }

    setIni(Ss+"/lisemdbaseoptions.cfg");


    QStringList pythonCommandArguments;

    //if (runOptionsscript)
    pythonCommandArguments << ScriptDirName + ScriptFileName;

    pythonCommandArguments << Ss+ "/lisemdbaseoptions.cfg";

    //qDebug() << pythonCommandArguments;

    Process->start (condaenv+"/python", pythonCommandArguments);
    Process->setReadChannel(QProcess::StandardOutput);

}

void MainWindow::readFromStderr()
{
    QString buffer = QString(Process->readAllStandardError());

    bufprev=text_out->toPlainText();

    //text_out->clear();
    text_out->appendPlainText(buffer);
}

void MainWindow::readFromOutput()
{
    QString buffer = QString(Process->readAllStandardOutput());
    QString bufshow;


    if (buffer.contains("Processing")){
        if (bufstart) {
            bufprev = text_out->toPlainText();
            bufstart = false;
            bufprev += buffer;
            bufprev.remove('\r');
            QStringList SL = bufprev.split("\n");
            SL.removeLast();
            bufprev = SL.join('\n');
        }

        bufshow = bufprev+buffer;
    } else {
        bufshow = text_out->toPlainText() + buffer;
        bufstart = true;

    }

    text_out->clear();
    text_out->appendPlainText(bufshow);
}
