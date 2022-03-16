#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QtGui>
#include <QtWidgets>

#include "ui_mainwindow.h"

#define WarningMsg(s) QMessageBox::warning(this,"NutShell WARNING",QString(s),QMessageBox::Yes)

class MainWindow : public QMainWindow, private Ui::MainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    QString CondaBaseDirName;
    QString iniName;
    QString ScriptFileName;
   // QString LULCDirName;
    QString BaseDirName;
    QString ScriptDirName;
    QString BaseDEMName;
    QString BaseChannelName;
    QString BaseOutletsName;
    QString OutletstableName;
    QString WatershedsName;
    QString BaseDamsName;
    QString MapsDirName;
    QString LULCmapName;
    QString LULCtableName;
    QString LULCNNtableName;

    QString RainScriptFileName;
    QString RainRefName;
    QString RainBaseDirName;
    QString RainDirName;
    QString RainFilename;
    double conversionmm;
    double timeintervalGPM;
    double interpolationGPM;

    QString LULCNames;
    QString ESPGnumber;
    bool CondaInstall;
    int SG1;
    int SG2;
    double initmoist;
    double refBulkDens;
    double DEMfill;
    double CatchmentSize;
    int optionDEM;
    int optionChannels;
    int optionLULC;
    int optionSG;
    int optionSGInterpolation;
    int optionNoGravel;
    int optionInfil;
    int optionErosion;
    int optionD50;
    int optionUseBD;
    int optionUseDensity;
    int optionFillDEM;
    int optionCatchments;
    int optionUserOutlets;
    int optionPruneBranch;
    int optionIncludeDams;
    int optionChannelsNoEros;
    double chB;
    double chC;
    double chWidth;
    double chDepth;
    double chBaseflow;
    double refRootzone;
    double refMaxSoildepth;

    int genfontsize;

    QStringList LULCspare;

    void setupModel();
    bool GetCondaAllEnvs(int cda);
    bool GetCondaEnvs();
    void findDPIscale();
    QProcess *Process;

    int layer1;
    int layer2;

    QString bufprev;

    void setIniStart();
    void getIniStart();
    void setIni(QString sss, bool yes);
    void getIni(QString name);
    void readValuesfromUI();
    void writeValuestoUI();
    QString getFileorDir(QString inputdir,QString title, QStringList filters, int doFile);
    QStringList findFiles(const QStringList &files, const QString &text);
    void ShowHelp(int i);
    QStandardItemModel *model;
    void fillLULCTable();
    void copyLULCTable();
    void resetLULCTable();
    void createNNLULCTable();
    void fillOutletsTable();
    void resetOutletsTable();


    QStandardItemModel *modelOutlets;

private slots:

    void on_toolButton_base_clicked();
    void on_toolButton_maps_clicked();
    void on_toolButton_script_clicked();
 //   void on_toolButton_LULC_clicked();

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

    void on_checkBox_DEM_toggled(bool checked);

    void on_toolButton_SaveIni_clicked();


    void on_toolButton_userOutlets_clicked();

    void on_toolButton_stop_clicked();

    //void on_toolButton_loadIni_clicked();

    void on_combo_iniName_currentIndexChanged(int index);

    void on_toolButton_saveas_clicked();

    void on_toolButton_CheckAll_clicked();

    void on_checkBox_useLUdensity_toggled(bool checked);

    void on_checkBox_userefBD_toggled(bool checked);

    void on_toolButton_Dams_clicked();

    void on_toolButton_openIni_clicked();

    void on_toolButton_help2_clicked();

    void on_toolButton_help1_clicked();

    //void on_toolButton_loadLULCtable_clicked();

    //void on_lineEdit_LULCTable_textChanged(const QString &arg1);

    void on_toolButton_saveLULC_clicked();

    void on_toolButton_resetLULC_clicked();

    void on_toolButton_saveOutlets_clicked();

    void on_toolButton_resetOutlets_clicked();

    void on_toolButton_OutletsTable_clicked();

    void on_radioButton_OutletSIngle_toggled(bool checked);

    void on_radioButton_OutletMultiple_toggled(bool checked);

    void on_checkBox_erosion_toggled(bool checked);

    void on_toolButton_userWatersheds_clicked();

    void on_checkBox_createRainfall_clicked(bool checked);

    void on_toolButton_GPMpy_clicked();

    void on_toolButton_GPMin_clicked();

    void on_toolButton_GPMout_clicked();

    void on_toolButton_help3_clicked();

    void on_toolButton_help4_clicked();

    void on_toolButton_help5_clicked();

    void on_checkBox_createDams_clicked(bool checked);

    void on_toolButton_GPMrefmap_clicked();

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
