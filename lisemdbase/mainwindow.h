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
    QString bufprev;

    void setupModel();
    bool GetCondaEnvs();
    QProcess *Process;

    int layer1;
    int layer2;

    void setPyOptions();
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

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
