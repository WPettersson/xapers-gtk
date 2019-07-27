# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_ResultsWidget.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ResultsWidget(object):
    def setupUi(self, ResultsWidget):
        ResultsWidget.setObjectName("ResultsWidget")
        ResultsWidget.resize(280, 210)
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.formLayout = QtWidgets.QFormLayout(self.page)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(255)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        ResultsWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.page_2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.papersTable = PapersTable(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(255)
        sizePolicy.setHeightForWidth(self.papersTable.sizePolicy().hasHeightForWidth())
        self.papersTable.setSizePolicy(sizePolicy)
        self.papersTable.setObjectName("papersTable")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.papersTable)
        ResultsWidget.addWidget(self.page_2)

        self.retranslateUi(ResultsWidget)
        ResultsWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ResultsWidget)

    def retranslateUi(self, ResultsWidget):
        _translate = QtCore.QCoreApplication.translate
        ResultsWidget.setWindowTitle(_translate("ResultsWidget", "StackedWidget"))
        self.label.setText(_translate("ResultsWidget", "No results found"))


from xapersqt.PapersDetails import PapersTable
