# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loadWidgetpqMvMo.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QProgressBar,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_LoadWidget(object):
    def setupUi(self, LoadWidget):
        if not LoadWidget.objectName():
            LoadWidget.setObjectName(u"LoadWidget")
        LoadWidget.resize(411, 221)
        self.mainLayout = QVBoxLayout(LoadWidget)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainFrame = QFrame(LoadWidget)
        self.mainFrame.setObjectName(u"mainFrame")
        self.mainFrame.setFrameShape(QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QFrame.Raised)
        self.labelLayout = QVBoxLayout(self.mainFrame)
        self.labelLayout.setSpacing(0)
        self.labelLayout.setObjectName(u"labelLayout")
        self.labelLayout.setContentsMargins(0, 0, 0, 0)
        self.loading_label = QLabel(self.mainFrame)
        self.loading_label.setObjectName(u"loading_label")
        font = QFont()
        font.setPointSize(14)
        self.loading_label.setFont(font)
        self.loading_label.setAlignment(Qt.AlignCenter)

        self.labelLayout.addWidget(self.loading_label)

        self.progressBar = QProgressBar(self.mainFrame)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(80)

        self.labelLayout.addWidget(self.progressBar)


        self.mainLayout.addWidget(self.mainFrame)


        self.retranslateUi(LoadWidget)

        QMetaObject.connectSlotsByName(LoadWidget)
    # setupUi

    def retranslateUi(self, LoadWidget):
        LoadWidget.setWindowTitle(QCoreApplication.translate("LoadWidget", u"Form", None))
        self.loading_label.setText(QCoreApplication.translate("LoadWidget", u"A inicializar os Sistemas...", None))
        self.progressBar.setFormat(QCoreApplication.translate("LoadWidget", u"%p%", None))
    # retranslateUi

