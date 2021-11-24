#include "mainwindow.h"


//====LULC========================================================

void MainWindow::resetLULCTable()
{
    for (int r = 0; r < model->rowCount(); r++){
        QStringList fields = LULCspare[r].split(QRegExp("\\s+"));
        for (int c = 1; c < model->columnCount()-1; c++){
            model->item(r,c)->setText(fields.at(c+1));
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
        }

        file.close();
    }
}

void MainWindow::fillLULCTable()
{
    QFile file(LULCtableName);

    if(file.open(QIODevice::ReadOnly)) {

        QTextStream in(&file);

        int r = 0;
        while(!in.atEnd()) {
            QString line = in.readLine().simplified();
            qDebug() << line;
            if (r > 0) {
                QStringList fields = line.split(QRegExp("\\s+"));

                for (int i = 0; i < fields.count(); i++){
                    if (i == 0)
                        model->setVerticalHeaderItem(r-1,new QStandardItem(fields.at(0)));
                    else {
                        QStandardItem *Input = new QStandardItem(fields.at(i));
                        model->setItem(r-1,i-1,Input);
                    }
                }
            }
            r++;
        }

        file.close();
    }
    loadLULCnames();
}

void MainWindow::on_toolButton_saveLULC_clicked()
{
    QFile file(LULCtableName);

    if(file.open(QIODevice::WriteOnly | QIODevice::Text))
    {

        QTextStream stream(&file);
        int n = model->rowCount();
        int m = model->columnCount();

        QString sss = QString("0 1 2 3 4 5 6 7\n");
        stream << sss;

        for (int i=0; i<n; ++i)
        {
            if (model->item(i,0)->text().isEmpty())
                continue;

            QStringList lll;
            lll << model->verticalHeaderItem(i)->text().split("-").at(0);

            for (int j=0; j<m; j++)
            {
                lll << model->item(i,j)->text();
               // qDebug() << model->item(i,j)->text();
            }
            QString sss = lll.join(' ')+"\n";
            stream << sss;
        }

        file.close();
    }
}

void MainWindow::loadLULCnames()
{
    QString name = LULCNames;//QString(qApp->applicationDirPath()+"/lulcnames.ini");

    QFile file(name);
    QStringList sl;
    if(file.open(QIODevice::ReadOnly)) {

        QTextStream in(&file);

        while(!in.atEnd()) {
            QString line = in.readLine();
            sl << line;
        }
        file.close();

        for (int i = 0; i < model->rowCount(); i++) {
            QString S = "";
            int m = model->verticalHeaderItem(i)->text().toInt();
            for (int j=0; j < sl.count(); j++) {
                if (sl[j].split("-").at(0).toInt() == m)
                    S = sl[j];
            }
            model->verticalHeaderItem(i)->setText(S);
        }
    }

    //assumes
//            1- Deciduous Broadleaf Forest
//            2- Cropland
//            3- Built-up Land
//            4- Mixed Forest
//            5- Shrubland
//            6- Barren Land
//            7- Fallow Land
//            8- Wasteland
//            9- Water Bodies
//            10- Plantations
//            11- Aquaculture
//            12- Mangrove Forest
//            13- Salt Pan
//            14- Grassland
//            15- Evergreen Broadleaf Forest
//            16- Deciduous Needleleaf Forest
//            17- Permanent Wetlands
//            18- Snow & Ice
//            19- Evergreen Needleleaf Forest

}

void MainWindow::on_toolButton_resetLULC_clicked()
{
    resetLULCTable();
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


