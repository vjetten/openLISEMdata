#include "mainwindow.h"

void MainWindow::on_toolButton_help2_clicked()
{
    ShowHelp(2);
}

void MainWindow::on_toolButton_help1_clicked()
{
    ShowHelp(1);
}

void MainWindow::ShowHelp(int i)
{
    QString filename;
    if (i == 1) filename=":/help1.html";
    if (i == 2) filename=":/help2.html";
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
