#include "mainwindow.h"

void MainWindow::setupModel()
{
    Process = new QProcess(this);
    Process->setReadChannel ( QProcess::StandardError );

    connect(Process, SIGNAL(readyReadStandardError()),this, SLOT(readFromStderr()) );
    connect(Process, SIGNAL(readyReadStandardOutput()),this, SLOT(readFromOutput()) );
    connect(pushButton_start, SIGNAL(clicked()), this, SLOT(runModel()));
}

void MainWindow::runModel()
{
    text_out->clear();

    createNNLULCTable();

    // add the env path names, copied from Spyder. Maybe overkill but it works
    QString condaenv = combo_envs->currentText();
    QString condascripts = QDir(condaenv+"/../Scripts").absolutePath();
    QString condabase = QDir(condaenv+"/../..").absolutePath();
    QProcessEnvironment env = QProcessEnvironment::systemEnvironment();
    env.insert("USE_PATH_FOR_GDAL_PYTHON","YES");
    env.insert("CONDA_ACTIVATE_SCRIPT",condascripts+"/activate");
    env.insert("CONDA_ENV_PATH",condaenv);
    env.insert("CONDA_ENV_PYTHON",condaenv+"/python.exe");
    env.insert("CONDA_EXE",condascripts+"/conda.exe");
    env.insert("CONDA_PREFIX",condaenv);
    env.insert("CONDA_PYTHON_EXE",condabase+"/python.exe");
    env.insert("CONDA_SHLVL","1");
    env.insert("GDAL_DATA",condaenv+"/Library/share/gdal");
    env.insert("GEOTIFF_CSV",condaenv+"/Library/share/epsg_csv");
    QString addpath = condaenv+";"+condaenv+"/Library/bin;"+condaenv+"/Scripts;";
    env.insert("PATH", addpath + env.value("Path"));
    Process->setProcessEnvironment(env);

    readValuesfromUI();
    setIni(QDir::tempPath()+"/lisemdbaseoptions.cfg");
    QStringList pythonCommandArguments;
    pythonCommandArguments << ScriptFileName;
    pythonCommandArguments << QDir::tempPath() + "/lisemdbaseoptions.cfg";
    Process->start (condaenv+"/python", pythonCommandArguments);
    Process->setReadChannel(QProcess::StandardOutput);
}

void MainWindow::readFromStderr()
{
    QString buffer = QString(Process->readAllStandardError());

    bufprev=text_out->toPlainText();

    text_out->clear();
    text_out->appendPlainText(buffer);
}

void MainWindow::readFromOutput()
{
    QString buffer = QString(Process->readAllStandardOutput());

    bufprev=text_out->toPlainText();

    if (buffer.contains("D50-D90")){
//        QStringList S = bufprev.split("\r\n");
//        if (S.last().contains("D50"))
//            S.removeLast();
//        S << buffer;
//        bufprev = S.join("\r\n");
        bufprev.remove(bufprev.indexOf("D50")-1,100);
        bufprev+=buffer;
    } else {
        bufprev+=buffer;
    }

    text_out->clear();
    text_out->appendPlainText(bufprev);
}
