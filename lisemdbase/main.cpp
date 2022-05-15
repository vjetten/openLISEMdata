#include "mainwindow.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication* temp = new QApplication(argc, argv);
    double width = QApplication::desktop()->width();
    double height = QApplication::desktop()->height();

    if (height < 1080) {
        // assumes that the default desktop resolution is 720p (scale of 1)
        int minWidth = 1280;

        double scale = width / minWidth;
        std::string scaleAsString = std::to_string(scale);
        QByteArray scaleAsQByteArray(scaleAsString.c_str(), scaleAsString.length());
        qputenv("QT_SCALE_FACTOR", scaleAsQByteArray);
    }
    delete temp;

    QApplication a(argc, argv);
    MainWindow w;

    a.setStyle("Fusion");

    // set style
//    qApp->setStyle(QStyleFactory::create("Fusion"));
//    // increase font size for better reading
//    QFont defaultFont = QApplication::font();
//    defaultFont.setPointSize(defaultFont.pointSize()+2);
//    qApp->setFont(defaultFont);
//    // modify palette to dark
//    QPalette darkPalette;
//    darkPalette.setColor(QPalette::Window,QColor(53,53,53));
//    darkPalette.setColor(QPalette::WindowText,Qt::white);
//    darkPalette.setColor(QPalette::Disabled,QPalette::WindowText,QColor(127,127,127));
//    darkPalette.setColor(QPalette::Base,QColor(42,42,42));
//    darkPalette.setColor(QPalette::AlternateBase,QColor(66,66,66));
//    darkPalette.setColor(QPalette::ToolTipBase,Qt::white);
//    darkPalette.setColor(QPalette::ToolTipText,Qt::white);
//    darkPalette.setColor(QPalette::Text,Qt::white);
//    darkPalette.setColor(QPalette::Disabled,QPalette::Text,QColor(127,127,127));
//    darkPalette.setColor(QPalette::Dark,QColor(35,35,35));
//    darkPalette.setColor(QPalette::Shadow,QColor(20,20,20));
//    darkPalette.setColor(QPalette::Button,QColor(53,53,53));
//    darkPalette.setColor(QPalette::ButtonText,Qt::white);
//    darkPalette.setColor(QPalette::Disabled,QPalette::ButtonText,QColor(127,127,127));
//    darkPalette.setColor(QPalette::BrightText,Qt::red);
//    darkPalette.setColor(QPalette::Link,QColor(42,130,218));
//    darkPalette.setColor(QPalette::Highlight,QColor(42,130,218));
//    darkPalette.setColor(QPalette::Disabled,QPalette::Highlight,QColor(80,80,80));
//    darkPalette.setColor(QPalette::HighlightedText,Qt::white);
//    darkPalette.setColor(QPalette::Disabled,QPalette::HighlightedText,QColor(127,127,127));

//    qApp->setPalette(darkPalette);

    w.show();
    return a.exec();
}
