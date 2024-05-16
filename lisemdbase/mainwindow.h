#ifndef MAINWINDOW_H
#define MAINWINDOW_H

//#include <QMainWindow>
#include <QtGui>
#include <QtWidgets>

#include "ui_mainwindow.h"

#define WarningMsg(s) QMessageBox::warning(this,"LISEM DBASE generator WARNING",QString(s),QMessageBox::Yes)

class MainWindow : public QMainWindow, private Ui::MainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    QString ProjectDirName;
    QString CondaBaseDirName;
    QString iniName;
    QString ScriptFileName;
    QString ScriptDirName;
    QString BaseDirName;
    QString BaseDEMName;
    QString BaseChannelName;
    QString BaseOutletsName;
    QString BaseOutpointsName;
    QString BaseCulvertsName;
    QString OutletstableName;
    QString WatershedsName;
    QString BaseDamsName;
    QString MapsDirName;
    QString LULCmapName;
    QString LULCtableName;
    QString LULCNNtableName;
    QString NDVImapName;
    QString roadsSHPName;
    QString buildingsSHPName;
    QString drummapName;
    QString BuiltUpAreaName;

    QString optionList;

   // QString RainScriptFileName;
   // QString IDMScriptFileName;
   // QString ERAScriptFileName;
    QString RainRefNameDEM;
    QString RainBaseDirName;
    QString RainDirName;
    QString RainFilename;
    QString RainEPSG;
    QString RainString;
    QString RainGaugeFilename;
    QString RainGaugeFilenameIn;
    QString RainFilenameHourIDM;
    QString RainFilenameHourERA;
    QString IDMFilename;
    QString ERAFilename;
    double conversionmm;
    double timeintervalGPM;
    double interpolationGPM;
    double dailyA;
    double dailyB;
    int day0;
    int dayn;
    int dt30min;

    QString LULCNames;
    QString ESPGnumber;
    bool CondaInstall;
    int SG1;
    int SG2;
    double initmoist;
    double refBulkDens;
    double refBulkDens2;
    double DEMfill;
    double CatchmentSize;
    double CorrOM;
    int optionDEM;
    int optionChannels;
    int optionLULC;
    int optionSG;
    int optionSGInterpolation;
    int optionSGAverage;
    int optionNoGravel;
    int optionInfil;
    int optionErosion;
    int optionD50;
    int optionSplash;
    int optionUseBD;
    int optionUseBD2;
    int optionUseCorrOM;
    int optionUseCorrTexture;
    int optionUseDensity;
    int optionFillDEM;
    int optionCatchments;
    int optionUserOutlets;
    int optionPruneBranch;
    int optionIncludeDams;
    int optionUseCulverts;
    int optionChannelsNoEros;
    int optionRain;
    int optionGaugeGPM;
    int optionUseNDVI;
    int optionUseInfrastructure;
    int optionSpLash;
    int optionResample;
    int optionUseDrums;
    int optionUseStormDrain;
    int optionDrainShape;
    double chB;
    double chC;
    double chWidth;
    double chDepth;
    double chWidthS;
    double chDepthS;
    double chN;
    double chBaseflow;
    double refRootzone;
    double refMaxSoildepth;
    double corrOM;
    double corrClay;
    double corrSilt;
    double corrSand;
    double roofStore;
    double drainWidth;
    double drainHeight;
    double drainDiameter;
    double drainInletDistance;
    double drainInletSize;
   // bool runGPMscript;
   // bool runIDMscript;
    bool runOptionsscript;
  //  bool runERAscript;

    int genfontsize;

    QStringList LULCspare;

    int checkNameandOption(QString name, bool option, QString message);
    bool checkAllNames();
    void setupModel();
    bool GetCondaAllEnvs(int cda);
    bool GetCondaEnvs();
    void findDPIscale();
    QProcess *Process;

    int layer1;
    int layer2;

    QString bufprev;
    bool bufstart;

    void setIniStart();
    void getIniStart();
    void setIni(QString sss);
    QString checkName(int i, QString name);
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

    bool convertDailyPrecipitation();


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

    void on_toolButton_GPMin_clicked();

    void on_toolButton_GPMout_clicked();

    void on_toolButton_help3_clicked();

    void on_toolButton_help4_clicked();

    void on_toolButton_help5_clicked();

    void on_checkBox_createDams_clicked(bool checked);

    void on_toolButton_GPMrefmap_clicked();

    void on_toolButton_dailyRain_clicked();

  //  void on_pushButton_generateGPMRain_clicked();

 //  void on_pushButton_gennerateSyntheticRain_clicked();

 //   void on_tabWidgetOptions_currentChanged(int index);

 //   void on_toolButton_stopGPM_clicked();

    void on_toolButton_resetsoil_clicked();

    void on_toolButton_resetRain_clicked();

    void on_toolButton_userOutpoints_clicked();

  //  void on_toolButton_stopIDM_clicked();

    void on_pushButton_start_clicked();

 //   void on_pushButton_generateERARain_clicked();

 //   void on_toolButton_stopERA_clicked();

    void on_toolButton_GPMGauge_clicked();

    void on_checkBox_writeGaugeData_toggled(bool checked);

    void on_toolButton_userCulverts_clicked();

    void on_toolButton_deleteIni_clicked();

    void on_toolButton_NDVIMap_clicked();

    void on_toolButton_buildingsSHP_clicked();

    void on_toolButton_drumMap_clicked();

    void on_toolButton_roadsSHP_clicked();

    void on_toolButton_resetInfra_clicked();

    void on_toolButton_help6_clicked();

    void on_toolButton_resetEros_clicked();


    void on_checkBox_Rain_clicked(bool checked);

    void on_comboBox_Resample_currentIndexChanged(int index);

    void on_toolButton_RainFilename_clicked();

    void on_checkBox_useStormDrain_toggled(bool checked);

    void on_toolButton_BuiltUp_clicked();

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
