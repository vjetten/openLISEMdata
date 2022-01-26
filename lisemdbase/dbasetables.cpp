#include "mainwindow.h"


//====LULC========================================================

void MainWindow::resetLULCTable()
{
    for (int r = 1; r < model->rowCount()+1; r++){
        QStringList names = LULCspare[r].split(QRegExp("="));
        QString s = names.at(1).simplified();
        QStringList fields = s.split(QRegExp("\\s+"));
        for (int c = 1; c < model->columnCount(); c++){
            model->item(r-1,c)->setText(fields.at(c));
        }
    }
}

void MainWindow::copyLULCTable()
{
    QFile file(LULCtableName);
    if(file.open(QIODevice::ReadOnly)) {

        QTextStream in(&file);

        LULCspare.clear();
        while(!in.atEnd()) {
            QString line = in.readLine().simplified();
            LULCspare << line;
          //  qDebug() << line;
        }

        file.close();
    }
}

void MainWindow::fillLULCTable()
{
    LULCNNtableName = QFileInfo(lineEdit_Base->text()).absolutePath() + "/NN" + QFileInfo(LULCtableName).fileName();
    //qDebug() << "new table"<<LULCNNtableName << LULCtableName;

    QFile file(LULCtableName);

    if(file.open(QIODevice::ReadOnly)) {

        QTextStream in(&file);

        int r = 0;
        while(!in.atEnd()) {
            QString line = in.readLine().simplified();

            if (!line.contains("=")) {
                //warning old format here
                return;
            }

            if (r > 0) {
                QStringList names = line.split(QRegExp("="));
                QString s = names.at(1).simplified();
                QStringList fields = s.split(QRegExp("\\s+"));

                model->setVerticalHeaderItem(r-1,new QStandardItem(names.at(0).simplified()));
                for (int i = 0; i < fields.count(); i++){
                    QStandardItem *Input = new QStandardItem(fields.at(i));
                    model->setItem(r-1,i,Input);
                }
            }
            r++;
        }

        file.close();
    }
}

void MainWindow::on_toolButton_saveLULC_clicked()
{
    QFile file(LULCtableName);

    if(file.open(QIODevice::WriteOnly | QIODevice::Text))
    {

        QTextStream stream(&file);
        int n = model->rowCount();
        int m = model->columnCount();

        QString sss = QString("LULC =   0   1   2   3   4   5   6   7\n");
        stream << sss;

        for (int i=0; i<n; ++i)
        {
            if (model->item(i,0)->text().isEmpty())
                continue;

            QStringList lll;
            lll << model->verticalHeaderItem(i)->text();//.split("-").at(0);
            lll << "=";

            for (int j=0; j<m; j++)
            {
                lll << model->item(i,j)->text();
               // qDebug() << model->item(i,j)->text();
            }
            QString sss = lll.join("\t")+"\n";
           // qDebug() << sss;
            stream << sss;
        }

        file.close();
    }
}

void MainWindow::on_toolButton_resetLULC_clicked()
{
    resetLULCTable();
}

void MainWindow::createNNLULCTable()
{
    QFile file(LULCNNtableName);
    if(file.open(QIODevice::WriteOnly | QIODevice::Text))
    {
        QTextStream stream(&file);
        int n = model->rowCount();
        int m = model->columnCount();

        QString sss = QString("0   1   2   3   4   5   6   7\n");
        stream << sss;

        for (int i=0; i<n; ++i) {
            QStringList lll;
            for (int j=0; j<m; j++) {
                lll << model->item(i,j)->text();
            }
            QString sss = lll.join("\t")+"\n";
            stream << sss;
        }
        file.close();
    }
}



//====OUTLETS========================================================


void MainWindow::fillOutletsTable()
{
   // label_Outletnames->setText(OutletstableName);

    QFile file(OutletstableName);
    if(file.open(QIODevice::ReadOnly)) {

        QTextStream in(&file);

        int r = 0;
        while(!in.atEnd()) {
            QString line = in.readLine();
            if (r > 0) {
                QStringList fields = line.split(QRegExp("\\s+"));

                for (int i = 0; i < fields.count(); i++){
                    if (i == 0)
                        modelOutlets->setVerticalHeaderItem(r-1,new QStandardItem(fields.at(0)));
                    else {
                        QStandardItem *Input = new QStandardItem(fields.at(i));
                        modelOutlets->setItem(r-1,i-1,Input);
                    }
                }
            }
            r++;
        }

        file.close();
    }

}

void MainWindow::resetOutletsTable()
{
   // label_Outletnames->setText(OutletstableName);
    QFile file(OutletstableName);

    QStringList sl;
    if(file.open(QIODevice::ReadOnly)) {

        QTextStream in(&file);

        while(!in.atEnd()) {
            QString line = in.readLine();
            sl << line;
        }
        file.close();
    }

    sl.removeAt(0);

    for (int r = 0; r < modelOutlets->rowCount(); r++){
        QStringList fields = sl[r].split(QRegExp("\\s+"));
        for (int c = 1; c < modelOutlets->columnCount()-1; c++){
            modelOutlets->item(r,c)->setText(fields.at(c+1));
        }
    }
}


void MainWindow::on_toolButton_saveOutlets_clicked()
{
    QFile file(OutletstableName);

    if(file.open(QIODevice::WriteOnly | QIODevice::Text))
    {

        QTextStream stream(&file);
        int n = modelOutlets->rowCount();
        int m = modelOutlets->columnCount();

        QString sss = QString("0 1 2 3\n");
        stream << sss;

        for (int i=0; i<n; ++i)
        {
            if (modelOutlets->item(i,0)->text().isEmpty())
                continue;

            QStringList lll;
            lll << modelOutlets->verticalHeaderItem(i)->text().split("-").at(0);

            for (int j=0; j<m; j++) {
                lll << modelOutlets->item(i,j)->text();
            }
            QString sss = lll.join(' ')+"\n";
            stream << sss;
        }

        file.close();
    }
}

void MainWindow::on_toolButton_resetOutlets_clicked()
{
    resetOutletsTable();
}


