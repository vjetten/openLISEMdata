QT += core gui
QT += widgets
CONFIG += c++11

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    dbaseDirs.cpp \
    dbaseHelp.cpp \
    dbaseOptions.cpp \
    dbaseProcess.cpp \
    dbasetables.cpp \
    main.cpp \
    mainwindow.cpp

HEADERS += \
    mainwindow.h

FORMS += \
    mainwindow.ui

RESOURCES += resources/lisemdbase.qrc
RC_FILE = lisemdbase.rc

# Default rules for deployment.
#qnx: target.path = /tmp/$${TARGET}/bin
#else: unix:!android: target.path = /opt/$${TARGET}/bin
#!isEmpty(target.path): INSTALLS += target

DISTFILES += \
    scripts/lisChannels.py \
    scripts/lisDams.py \
    scripts/lisDemDerivatives.py \
    scripts/lisErosion.py \
    scripts/lisGlobals.py \
    scripts/lisInfrastructure.py \
    scripts/lisRainfall.py \
    scripts/lisSoils.py \
    scripts/lisSurface.py \
    scripts/lisemDBASEgenerator.py



