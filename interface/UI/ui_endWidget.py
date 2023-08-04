# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'endWidgetsLiMLn.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from ..qt_core import *

class Ui_EndWindow(object):
    def setupUi(self, EndWindow):
        if not EndWindow.objectName():
            EndWindow.setObjectName(u"EndWindow")
        EndWindow.resize(400, 300)
        self.verticalLayout = QVBoxLayout(EndWindow)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.mainFrame = QFrame(EndWindow)
        self.mainFrame.setObjectName(u"mainFrame")
        self.mainFrame.setFrameShape(QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.mainFrame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, -1, 0, 0)
        self.url = QLabel(self.mainFrame)
        self.url.setObjectName(u"url")
        self.url.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.url)

        self.frame = QFrame(self.mainFrame)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.copy_url = QPushButton(self.frame)
        self.copy_url.setObjectName(u"copy_url")

        self.verticalLayout_3.addWidget(self.copy_url)

        self.open_Link = QPushButton(self.frame)
        self.open_Link.setObjectName(u"open_Link")

        self.verticalLayout_3.addWidget(self.open_Link)

        self.open_QrCode = QPushButton(self.frame)
        self.open_QrCode.setObjectName(u"open_QrCode")

        self.verticalLayout_3.addWidget(self.open_QrCode)


        self.verticalLayout_2.addWidget(self.frame)


        self.verticalLayout.addWidget(self.mainFrame)


        self.retranslateUi(EndWindow)

        QMetaObject.connectSlotsByName(EndWindow)
    # setupUi

    def retranslateUi(self, EndWindow):
        EndWindow.setWindowTitle(QCoreApplication.translate("EndWindow", u"Form", None))
        self.url.setText("")
        self.copy_url.setText(QCoreApplication.translate("EndWindow", u"Copiar Link", None))
        self.open_Link.setText(QCoreApplication.translate("EndWindow", u"Abir Link", None))
        self.open_QrCode.setText(QCoreApplication.translate("EndWindow", u"Abrir QrCode", None))
    # retranslateUi

