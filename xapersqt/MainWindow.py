# This file is a part of XapersQt - a Qt interface to the Xapers article
# database system. Copyright (C) 2017 William Pettersson
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
from PyQt5.QtWidgets import (QWidget, QLineEdit, QBoxLayout,
                             QPushButton, QTableView, QStackedWidget, QLabel,
                             QHeaderView, QAbstractItemView, QShortcut,
                             QMainWindow)
from PyQt5.QtCore import (Qt, QAbstractItemModel, QModelIndex, QSize, QUrl,
                          QSettings)
from PyQt5.QtGui import (QKeySequence, QFontMetrics, QFont, QDesktopServices)
from xapersqt.DocWindow import DocWindow

gettext.bindtextdomain('xapers-qt', '/path/to/my/language/directory')
gettext.textdomain('xapers-qt')
_ = gettext.gettext

CONSTS = {}
CONSTS['cols'] = 4

HEADINGS = [_("Title"), _("Author(s)"), _("Year"), _("PDF")]


class ResultsWidget(QStackedWidget):
    def __init__(self, settings, db):
        super(ResultsWidget, self).__init__()
        self.settings = settings
        self.children = []
        self.db = db
        noResults = QWidget()
        noResultsLayout = QBoxLayout(QBoxLayout.TopToBottom)
        noResultsLabel = QLabel()
        noResultsLabel.setText("No results found")
        noResultsLayout.addWidget(noResultsLabel)
        noResults.setLayout(noResultsLayout)
        self.addWidget(noResults)

        self.results = PapersTable(self.settings)
        self.addWidget(self.results)

    def doSearch(self, searchString=""):
        docs = self.db.search(searchString)
        if len(docs) == 0:
            self.setCurrentIndex(0)
        else:
            self.results.addResults(docs)
            self.setCurrentIndex(1)

    def saveSettings(self):
        self.results.saveSettings()

    def selectNext(self):
        self.results.selectNext()

    def selectPrev(self):
        self.results.selectPrev()

    def openPDF(self):
        self.results.openPDF()

    def openDoc(self):
        self.children.append(self.results.openDoc())


class PDFButton(QPushButton):
    def __init__(self, url):
        super(PDFButton, self).__init__()
        self.url = url
        self.setText("Open PDF")
        self.setStyleSheet("margin: 5px;")
        self.clicked.connect(self.openUrl)

    def openUrl(self):
        path = "file://" + self.url
        QDesktopServices.openUrl(QUrl(path))


class PapersTable(QTableView):
    def __init__(self, settings):
        super(PapersTable, self).__init__()
        self.settings = settings
        self.model = PapersModel()
        self.setModel(self.model)
        self.activated.connect(self.openPDF)
        self.setSortingEnabled(True)
        try:
            setting = self.settings.value("table/titleProportion", 0.6)
            self.titleProportion = float(setting)
        except ValueError:
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
        self.horizontalHeader().sectionResized.connect(self.columnResize)

    def columnResize(self, col, old, new):
        if col == 0:
            self.titleProportion = float(new) / self.width()

    def addResults(self, docs=[]):
        listed = list(docs)
        self.model.setDoc(listed)
        count = 0
        for d in listed:
            try:
                button = PDFButton(d.get_fullpaths()[0])
                # Third column is PDF
                self.setIndexWidget(self.model.index(count, 3, 0), button)
            except IndexError:  # No PDF file found
                pass
            count += 1
        self.selectRow(0)
        self.setFocus()

    def selectNext(self):
        try:
            index = self.selectionModel().selectedRows()[0]
            self.selectRow(index.row()+1)
        except:
            pass

    def selectPrev(self):
        try:
            index = self.selectionModel().selectedRows()[0]
            self.selectRow(index.row()-1)
        except:
            pass

    def openDoc(self):
        try:
            index = self.selectionModel().selectedRows()[0]
            doc = self.model.docs[index.row()]
            return DocWindow(doc)
        except:
            pass

    def openPDF(self):
        try:
            index = self.selectionModel().selectedRows()[0]
            doc = self.model.docs[index.row()]
            url = doc.get_fullpaths()[0]
            path = "file://" + url
            QDesktopServices.openUrl(QUrl(path))
        except:
            pass

    def saveSettings(self):
        self.settings.setValue("table/titleProportion", self.titleProportion)

    def refresh(self):
        self.setColumnWidth(0, self.titleProportion * self.width())


class PapersModel(QAbstractItemModel):
    def __init__(self):
        super(PapersModel, self).__init__()
        metric = QFontMetrics(QFont())
        # TODO Could probably be done better
        self.yearWidth = metric.width("8888") + 10
        self.PDFwidth = metric.width("Open PDF") + 30
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
            return doc.get_title()
        elif index.column() == 1:
            auth = doc.get_authors()
            if not auth:
                return ""
            if len(auth) > 3:
                return ", ".join(auth[0:2]) + " et al."
            else:
                return ", ".join(auth)
        elif index.column() == 2:
            return doc.get_year()
        elif index.column() == 3:
            f = doc.get_files()
            # If len(f) > 0 we will insert a button instead
            if len(f) == 0:
                return "No PDF found"
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


class MainWindow(QMainWindow):
    def __init__(self, db, keybinds):
        super(MainWindow, self).__init__()
        self.settings = QSettings("xapers-qt", "xapers-qt")
        self.shortcuts = []
        self.db = db
        self.makeUI(keybinds)

    def startSearch(self):
        self.resultWidget.doSearch(self.searchBar.text())

    def makeUI(self, keybinds):
        self.resize(800, 300)
        try:
            width = int(self.settings.value("main/width", 800))
        except ValueError:
            width = 800
        try:
            height = int(self.settings.value("main/height", 300))
        except ValueError:
            height = 300
        self.resize(width, height)
        self.setWindowTitle("xapers-qt")
        mainLayout = QBoxLayout(QBoxLayout.TopToBottom)
        self.searchBar = SearchBar(self)
        self.resultWidget = ResultsWidget(self.settings, self.db)

        mainLayout.addWidget(self.searchBar)
        mainLayout.addWidget(self.resultWidget)
        self.central = QWidget()
        self.central.setLayout(mainLayout)
        self.setCentralWidget(self.central)
        self.setupKeybinds(keybinds)
        self.show()

    def setupKeybinds(self, binds):
        for s in self.shortcuts:
            pass  # TODO Delete shortcut?
        for keys, action in binds:
            if action == "Search":
                func = self.focusSearchBar
            elif action == "Next":
                func = self.resultWidget.selectNext
            elif action == "Prev":
                func = self.resultWidget.selectPrev
            elif action == "OpenPDF":
                func = self.resultWidget.openPDF
            elif action == "OpenDoc":
                func = self.resultWidget.openDoc
            elif action == "Exit":
                func = self.close
            else:
                action = None
            if action:
                shortcut = QShortcut(QKeySequence(keys), self)
                shortcut.activated.connect(func)
                self.shortcuts.append(shortcut)

    def focusSearchBar(self):
        self.searchBar.searchLine.setFocus(Qt.ShortcutFocusReason)

    def saveSettings(self):
        self.settings.setValue("main/width", self.width())
        self.settings.setValue("main/height", self.height())
        self.resultWidget.saveSettings()

    def closeEvent(self, event):
        self.saveSettings()

    def resizeEvent(self, resizeEvent):
        self.resultWidget.results.refresh()
