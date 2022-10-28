#include "mainwindow.h"



void MainWindow::on_toolButton_help5_clicked()
{
    ShowHelp(5);
}

void MainWindow::on_toolButton_help4_clicked()
{
    ShowHelp(4);
}

void MainWindow::on_toolButton_help3_clicked()
{
    ShowHelp(3);
}

void MainWindow::on_toolButton_help2_clicked()
{
    ShowHelp(2);
}

void MainWindow::on_toolButton_help1_clicked()
{
    ShowHelp(1);
}

void MainWindow::on_toolButton_help6_clicked()
{
    ShowHelp(6);
}

void MainWindow::ShowHelp(int i)
{
    QString filename;
    if (i == 1) filename=":/help1.html";
    if (i == 2) filename=":/help2.html";
    if (i == 3) filename=":/help3.html";
    if (i == 4) filename=":/help4.html";
    if (i == 5) filename=":/help5.html";
    //if (i == 6) filename=":/help6.html";
    QFile file(filename);
    file.open(QFile::ReadOnly | QFile::Text);
    QTextStream stream(&file);
    QTextEdit *helptxt = new QTextEdit;
    helptxt->setHtml(stream.readAll());

    QTextEdit *view = new QTextEdit(helptxt->toHtml());
    view->createStandardContextMenu();
    view->setWindowTitle("Option help");
    view->setMinimumWidth(800);
    view->setMinimumHeight(600);
    view->setAttribute(Qt::WA_DeleteOnClose);

    view->show();
}
