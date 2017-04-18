#!/usr/bin/env python2

# Load config


# Searching
# tag:string
# show only things with "string" inside tag
# support and/or keywords, and brackets?


# Layout
#
# Searchbox
# ---------
# Entry
# Entry

# Entry = Title, Authors, Year, PDF-link

import sys
import xapers
import gettext
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, QBoxLayout,
                             QPushButton, QTableView, QStackedWidget, QLabel,
                             QHeaderView, QAbstractItemView, QShortcut)
from PyQt5.QtCore import (Qt, QCoreApplication, QAbstractItemModel,
                          QModelIndex, QSize, QUrl)
from PyQt5.QtGui import QKeySequence, QFontMetrics, QFont, QDesktopServices

gettext.bindtextdomain('xapers-qt', '/path/to/my/language/directory')
gettext.textdomain('xapers-qt')
_ = gettext.gettext


db = xapers.Database('~/.xapers/docs')

CONSTS = {}
CONSTS['cols'] = 4

HEADINGS = [_("Title"), _("Author(s)"), _("Year"), _("PDF")]


class ResultsWidget(QStackedWidget):
    def __init__(self):
        super(ResultsWidget, self).__init__()
        noResults = QWidget()
        noResultsLayout = QBoxLayout(QBoxLayout.TopToBottom)
        noResultsLabel = QLabel()
        noResultsLabel.setText("No results found")
        noResultsLayout.addWidget(noResultsLabel)
        noResults.setLayout(noResultsLayout)
        self.addWidget(noResults)

        self.results = PapersTable()
        self.addWidget(self.results)

    def doSearch(self, searchString=""):
        docs = db.search(searchString)
        if len(docs) == 0:
            self.setCurrentIndex(0)
        else:
            self.results.addResults(docs)
            self.setCurrentIndex(1)


class PapersTable(QTableView):
    def __init__(self):
        super(PapersTable, self).__init__()
        self.model = PapersModel()
        self.setModel(self.model)
        self.setSortingEnabled(True)
        self.titleProportion = 0.6
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
        self.clicked.connect(self.onTableClicked)
        self.horizontalHeader().sectionResized.connect(self.columnResize)

    def columnResize(self, col, old, new):
        if col == 0:
            self.titleProportion = float(new) / self.width()

    def addResults(self, docs=[]):
        self.model.setDoc(docs)

    def refresh(self):
        self.setColumnWidth(0, self.titleProportion * self.width())

    def onTableClicked(self, index):
        if (index.isValid()):
            if index.column() == 3:
                doc = self.model.getDoc(index.row())
                try:
                    path = "file://" + doc.get_fullpaths()[0]
                    QDesktopServices.openUrl(QUrl(path))
                except:
                    pass


class PapersModel(QAbstractItemModel):
    def __init__(self):
        super(PapersModel, self).__init__()
        metric = QFontMetrics(QFont())
        # TODO Could probably be done better
        self.yearWidth = metric.width("8888") + 10
        self.PDFwidth = metric.width("Open") + 10
        self.docs = []

    def setDoc(self, docs):
        self.beginResetModel()
        self.docs = list(docs)
        self.endResetModel()

    def getDoc(self, index):
        try:
            return self.docs[index]
        except:
            return []

    def index(self, row, column, parent):
        return QAbstractItemModel.createIndex(self, row, column,
                                              CONSTS['cols'] * row + column)

    def parent(self, index):
        return QModelIndex()

    def columnCount(self, unused):
        return CONSTS['cols']

    def rowCount(self, unused):
        return len(self.docs)

    def data(self, index, role):
        doc = self.docs[index.row()]
        if role != Qt.DisplayRole:
            return None
        if index.column() == 0:
            return str(doc.get_title())
        elif index.column() == 1:
            auth = doc.get_authors()
            if len(auth) > 3:
                return ", ".join(auth[0:2]) + " et al."
            else:
                return ", ".join(auth)
        elif index.column() == 2:
            return doc.get_year()
        elif index.column() == 3:
            f = doc.get_files()
            if len(f) > 0:
                # s = "%s" % (f[0])
                return "Open"
            return None
        return None

    def sort(self, which, order):
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


class DocWindow(QWidget):
    def __init__(self):
        super(DocWindow, self).__init__()
        self.makeUI()

    def makeUI(self):
        self.resize(400, 300)
        self.setWindowTitle("xapers-qt: Document editor")


class SearchBar(QWidget):
    def __init__(self, parent):
        super(SearchBar, self).__init__()
        self.parent = parent
        self.makeUI()

    def makeUI(self):
        searchLayout = QBoxLayout(QBoxLayout.LeftToRight)
        self.searchLine = QLineEdit()
        searchButton = QPushButton("Search")
        searchButton.clicked.connect(self.parent.startSearch)
        self.searchLine.returnPressed.connect(self.parent.startSearch)
        searchLayout.addWidget(self.searchLine)
        searchLayout.addWidget(searchButton)
        self.setLayout(searchLayout)

    def text(self):
        return self.searchLine.text()


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.makeUI()

    def startSearch(self):
        self.resultWidget.doSearch(self.searchBar.text())

    def makeUI(self):
        self.resize(800, 300)
        self.setWindowTitle("xapers-qt")
        mainLayout = QBoxLayout(QBoxLayout.TopToBottom)
        self.searchBar = SearchBar(self)
        self.resultWidget = ResultsWidget()

        mainLayout.addWidget(self.searchBar)
        mainLayout.addWidget(self.resultWidget)
        self.setLayout(mainLayout)
        esc = QShortcut(QKeySequence("Esc"), self)
        ctrlq = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q), self)
        esc.activated.connect(QCoreApplication.instance().quit)
        ctrlq.activated.connect(QCoreApplication.instance().quit)
        self.show()

    def resizeEvent(self, resizeEvent):
        self.resultWidget.results.refresh()


def main():
    app = QApplication(sys.argv)
    m = MainWindow()
    assert m
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
