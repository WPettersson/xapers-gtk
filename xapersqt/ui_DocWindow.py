# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_DocWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DocWindow(object):
    def setupUi(self, Ui_DocWindow):
        Ui_DocWindow.setObjectName("Ui_DocWindow")
        Ui_DocWindow.setGeometry(QtCore.QRect(0, 0, 400, 300))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Ui_DocWindow)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(Ui_DocWindow)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Ui_DocWindow)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(Ui_DocWindow)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.key = QtWidgets.QLineEdit(Ui_DocWindow)
        self.key.setObjectName("key")
        self.gridLayout.addWidget(self.key, 0, 1, 1, 1)
        self.title = QtWidgets.QLineEdit(Ui_DocWindow)
        self.title.setObjectName("title")
        self.gridLayout.addWidget(self.title, 1, 1, 1, 1)
        self.year = QtWidgets.QLineEdit(Ui_DocWindow)
        self.year.setObjectName("year")
        self.gridLayout.addWidget(self.year, 2, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.tag_list = QtWidgets.QLabel(Ui_DocWindow)
        self.tag_list.setObjectName("tag_list")
        self.verticalLayout_2.addWidget(self.tag_list)
        self.pdf_list = PDFList(Ui_DocWindow)
        self.pdf_list.setObjectName("pdf_list")
        self.verticalLayout_2.addWidget(self.pdf_list)
        self.buttonBox = QtWidgets.QDialogButtonBox(Ui_DocWindow)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Discard|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Ui_DocWindow)
        QtCore.QMetaObject.connectSlotsByName(Ui_DocWindow)

    def retranslateUi(self, Ui_DocWindow):
        _translate = QtCore.QCoreApplication.translate
        Ui_DocWindow.setWindowTitle(_translate("DocWindow", "xapers-qt: Document editor"))
        self.label_3.setText(_translate("DocWindow", "Year"))
        self.label_2.setText(_translate("DocWindow", "Title"))
        self.label.setText(_translate("DocWindow", "Key"))
        self.tag_list.setText(_translate("DocWindow", "TextLabel"))


from xapersqt.PDFDetails import PDFList
