# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_SearchBar.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SearchBar(object):
    def setupUi(self, SearchBar):
        SearchBar.setObjectName("SearchBar")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(SearchBar)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.searchLine = QtWidgets.QLineEdit(SearchBar)
        self.searchLine.setObjectName("searchLine")
        self.horizontalLayout_2.addWidget(self.searchLine)
        self.searchButton = QtWidgets.QPushButton(SearchBar)
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout_2.addWidget(self.searchButton)

        self.retranslateUi(SearchBar)
        QtCore.QMetaObject.connectSlotsByName(SearchBar)

    def retranslateUi(self, SearchBar):
        _translate = QtCore.QCoreApplication.translate
        SearchBar.setWindowTitle(_translate("SearchBar", "Form"))
        self.searchButton.setText(_translate("SearchBar", "Search"))


