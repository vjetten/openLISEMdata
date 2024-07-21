#include "mainwindow.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    // QApplication* temp = new QApplication(argc, argv);
    // double width = QApplication::desktop()->width();
    // double height = QApplication::desktop()->height();

    // if (height < 1080) {
    //     // assumes that the default desktop resolution is 720p (scale of 1)
    //     int minWidth = 1280;

    //     double scale = width / minWidth;
    //     std::string scaleAsString = std::to_string(scale);
    //     QByteArray scaleAsQByteArray(scaleAsString.c_str(), scaleAsString.length());
    //     qputenv("QT_SCALE_FACTOR", scaleAsQByteArray);
    // }
    // delete temp;

    QApplication a(argc, argv);
    MainWindow w;

    a.setStyle("Fusion");

    w.show();
    return a.exec();
}
