"""Classes relating to looking at papers.
"""
# This file is a part of XapersQt - a Qt interface to the Xapers article
# database system. Copyright (C) 2019 William Pettersson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# The author can be contacted at william@ewpettersson.se and issues can
# be raised at https://github.com/WPettersson/xapers-qt/

import gettext
from PyQt5.QtWidgets import (QTableView, QHeaderView, QAbstractItemView,
                             QPushButton)
from PyQt5.QtGui import QDesktopServices, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex, QSize, QUrl

from xapersqt.DocWindow import DocWindow


gettext.bindtextdomain('xapers-qt', '/path/to/my/language/directory')
gettext.textdomain('xapers-qt')
_ = gettext.gettext

CONSTS = {}
CONSTS['cols'] = 4

HEADINGS = [_("Title"), _("Author(s)"), _("Year"), _("PDF")]


class PDFButton(QPushButton):
    """A button which opens a PDF."""
    def __init__(self, url):
        super(PDFButton, self).__init__()
        self.url = url
        self.setText("Open PDF")
        self.setStyleSheet("margin: 5px;")
        self.clicked.connect(self.openUrl)

    def openUrl(self):
        """Open the PDF associated with this button."""
        path = "file://" + self.url
        QDesktopServices.openUrl(QUrl(path))


class PapersTable(QTableView):
    """The table which will contain all documents found by a search."""
    def __init__(self, parent):
        super(PapersTable, self).__init__()
        self.model = PapersModel()
        self.parent = parent
        self.settings = None
        self.titleProportion = 0.6
        self.setModel(self.model)
        self.activated.connect(self.openPDF)
        self.setSortingEnabled(True)
        self.horizontalHeader().show()
        self.horizontalHeader().setSectionsMovable(True)
        self.horizontalHeader().setMinimumSectionSize(self.model.yearWidth)
        self.setColumnWidth(0, self.titleProportion * self.width())
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.setColumnWidth(2, self.model.yearWidth)
        self.setColumnWidth(3, self.model.PDFwidth)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.horizontalHeader().sectionResized.connect(self.columnResize)

    def set_settings(self, settings):
        """Set the settings."""
        self.settings = settings
        try:
            setting = self.settings.value("table/titleProportion", 0.6)
            self.titleProportion = float(setting)
        except ValueError:
            self.titleProportion = 0.6
        self.setColumnWidth(0, self.titleProportion * self.width())

    def columnResize(self, col, old, new):
        """Inherited from QTableView. Record how wide the title is.
        """
        if col == 0:
            self.titleProportion = float(new) / self.width()

    def add_results(self, docs):
        """Set a list of documents as the results to be showin in this table.
        """
        listed = list(docs)
        count = 0
        self.model.setDoc(listed)
        for document in listed:
            try:
                button = PDFButton(document.get_fullpaths()[0])
                # Third column is PDF
                self.setIndexWidget(self.model.index(count, 3, 0), button)
            except IndexError:  # No PDF file found
                pass
            count += 1
        self.selectRow(0)
        self.setFocus()

    def selectNext(self):
        """Select the next document."""
        try:
            index = self.selectionModel().selectedRows()[0]
            self.selectRow(index.row()+1)
        except IndexError:
            # No more documents, or possibly no selected document
            pass

    def selectPrev(self):
        """Select the previous document."""
        try:
            index = self.selectionModel().selectedRows()[0]
            self.selectRow(index.row()-1)
        except IndexError:
            # No previous document, or possible no selected document
            pass

    def openDoc(self):
        """Open a window showing the details of a document."""
        try:
            index = self.selectionModel().selectedRows()[0]
            doc = self.model.docs[index.row()]
            return DocWindow(doc)
        except IndexError:
            # Possibly no selected document
            pass

    def openPDF(self):
        """Open a PDF of the highlighted document."""
        try:
            index = self.selectionModel().selectedRows()[0]
            doc = self.model.docs[index.row()]
            url = doc.get_fullpaths()[0]
            path = "file://" + url
            QDesktopServices.openUrl(QUrl(path))
        except IndexError:
            # Possibly no selected document, or no PDF associated with it
            pass

    def saveSettings(self):
        """Save the proportion of the total width that the title takes up.."""
        self.settings.setValue("table/titleProportion", self.titleProportion)

    def refresh(self):
        """Set the proportions of the columns."""
        self.setColumnWidth(0, self.titleProportion * self.width())


class PapersModel(QAbstractItemModel):
    """Represents an individual paper/document in the table."""
    def __init__(self):
        super(PapersModel, self).__init__()
        metric = QFontMetrics(QFont())
        # TODO Could probably be done better
        self.yearWidth = metric.width("8888") + 10
        self.PDFwidth = metric.width("Open PDF") + 33
        self.docs = []

    def setDoc(self, docs):
        """Set the (xapian) documents which occurs here."""
        self.beginResetModel()
        self.docs = list(docs)  # Create a copy of the list
        self.endResetModel()

    def getDoc(self, index):
        """Return a given document."""
        return self.docs[index]

    def index(self, row, column, parent):
        """Inheritied from QAbstractItemModel
        """
        return QAbstractItemModel.createIndex(self, row, column,
                                              CONSTS['cols'] * row + column)

    def parent(self, index):
        """Inheritied from QAbstractItemModel
        """
        return QModelIndex()

    def columnCount(self, unused):
        """Inheritied from QAbstractItemModel
        """
        return CONSTS['cols']

    def rowCount(self, unused):
        """Inheritied from QAbstractItemModel
        """
        return len(self.docs)

    def data(self, index, role):
        """Inheritied from QAbstractItemModel
        """
        doc = self.docs[index.row()]
        if role != Qt.DisplayRole:
            return None
        if index.column() == 0:
            return doc.get_title()
        elif index.column() == 1:
            auth = doc.get_authors()
            if len(auth) > 3:
                return ", ".join(auth[0:2]) + " et al."
            elif auth:
                return ", ".join(auth)
            return ""
        elif index.column() == 2:
            return doc.get_year()
        elif index.column() == 3:
            f = doc.get_files()
            # If len(f) > 0 we will insert a button instead
            if not f:
                return "No PDF found"
            return None
        return None

    def sort(self, which, order):
        """Inheritied from QAbstractItemModel.
        Sort by the appropriate column.
        """
        reverse = (order == Qt.DescendingOrder)
        if which == 0:  # Title
            self.layoutAboutToBeChanged.emit()
            self.docs.sort(key=lambda d: d.get_title(), reverse=reverse)
            self.layoutChanged.emit()
        elif which == 1:  # Authors
            self.layoutAboutToBeChanged.emit()
            self.docs.sort(key=lambda d: d.get_authors(), reverse=reverse)
            self.layoutChanged.emit()
        elif which == 2:  # Years
            self.layoutAboutToBeChanged.emit()
            self.docs.sort(key=lambda d: d.get_year(), reverse=reverse)
            self.layoutChanged.emit()

    def headerData(self, section, orientation, role):
        """Inherited from QAbstractItemModel."""
        if orientation != Qt.Horizontal:
            return None
        if role == Qt.SizeHintRole:
            if section == 0:  # Title
                return QSize(500, 15)
            if section == 2:
                return QSize(self.yearWidth, 15)
            if section == 3:
                return QSize(self.PDFwidth, 15)
        if role != Qt.DisplayRole:
            return None
        if section < len(HEADINGS):
            return HEADINGS[section]
        return None

