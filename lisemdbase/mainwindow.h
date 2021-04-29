#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QtGui>
#include <QtWidgets>

#include "ui_mainwindow.h"

class MainWindow : public QMainWindow, private Ui::MainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    QString CondaBaseDirName;

    QString ScriptFileName;
    QString LULCDirName;
    QString BaseDirName;
    QString BaseDEMName;
    QString BaseChannelName;
    QString MapsDirName;
    QString LULCmapName;
    QString LULCtableName;
    bool CondaInstall;
    int SG1;
    int SG2;
    double initmoist;
    double refBulkDens;
    int optionDEM;
    int optionChannels;
    int optionLULC;
    int optionSG;
    int optionInfil;
    int optionErosion;
    int optionUseBD;

    void setupModel();
    bool GetCondaEnvs();
    QProcess *Process;

    int layer1;
    int layer2;

    QString bufprev;

    void setIni(QString sss);
    void getIni();
    void readValuesfromUI();
    void writeValuestoUI();
    QString getFileorDir(QString inputdir,QString title, QStringList filters, bool doFile);

private slots:

    void on_toolButton_base_clicked();
    void on_toolButton_maps_clicked();
    void on_toolButton_script_clicked();
    void on_toolButton_LULC_clicked();

    void on_toolButton_CheckAll_toggled(bool checked);
    void runModel();
    void readFromStderr();
    void readFromOutput();

    void on_toolButton_clear_clicked();

    void on_toolButton_LULCTable_clicked();

    void on_toolButton_baseDEM_clicked();

    void on_toolButton_baseChannel_clicked();

    void on_toolButton_LULCMap_clicked();

    void on_comboBox_SGlayer1_currentIndexChanged(int index);

    void on_comboBox_SGlayer2_currentIndexChanged(int index);

    void on_checkBox_Infil_toggled(bool checked);

    void on_checkBox_Soilgrids_toggled(bool checked);

    void on_toolButton_clicked();

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
