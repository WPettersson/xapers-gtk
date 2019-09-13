# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_ImportWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ImportWindow(object):
    def setupUi(self, ImportWindow):
        ImportWindow.setObjectName("ImportWindow")
        ImportWindow.resize(759, 46)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(ImportWindow)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.source_string = QtWidgets.QLineEdit(ImportWindow)
        self.source_string.setObjectName("source_string")
        self.horizontalLayout_2.addWidget(self.source_string)
        self.buttonBox = QtWidgets.QDialogButtonBox(ImportWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(ImportWindow)
        QtCore.QMetaObject.connectSlotsByName(ImportWindow)

    def retranslateUi(self, ImportWindow):
        _translate = QtCore.QCoreApplication.translate
        ImportWindow.setWindowTitle(_translate("ImportWindow", "Import document"))

