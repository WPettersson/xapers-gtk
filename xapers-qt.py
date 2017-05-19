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
import os
import xapers
import gettext
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, QBoxLayout,
                             QPushButton, QTableView, QStackedWidget, QLabel,
                             QHeaderView, QAbstractItemView, QShortcut,
                             QMainWindow, QGridLayout, QDialogButtonBox,
                             QFileDialog, QMessageBox)
from PyQt5.QtCore import (Qt, QAbstractItemModel, QModelIndex, QSize, QUrl,
                          QSettings)
from PyQt5.QtGui import (QKeySequence, QFontMetrics, QFont, QDesktopServices,
                         QIcon)

gettext.bindtextdomain('xapers-qt', '/path/to/my/language/directory')
gettext.textdomain('xapers-qt')
_ = gettext.gettext


db = xapers.Database('~/.xapers/docs', writable=True)

CONSTS = {}
CONSTS['cols'] = 4

HEADINGS = [_("Title"), _("Author(s)"), _("Year"), _("PDF")]

KEYBINDS = [["Ctrl+L", "Search"], ["j", "Next"], ["k", "Prev"],
            ["Enter", "OpenPDF"], ["o", "OpenDoc"],
            ["Esc", "Exit"], ["Ctrl+q", "Exit"]]


class ResultsWidget(QStackedWidget):
    def __init__(self, settings):
        super(ResultsWidget, self).__init__()
        self.settings = settings
        self.children = []
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
        docs = db.search(searchString)
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
            return unicode(doc.get_title())
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


class PDFLabel(QLabel):
    def __init__(self, text, url):
        super(PDFLabel, self).__init__()
        markup = "<a href=\"%s\">%s</a>" % (url, text)
        self.setText(markup)
        self.setOpenExternalLinks(True)


class PDFList(QWidget):
    def __init__(self, parent, doc):
        super(PDFList, self).__init__()
        self.parent = parent
        self.doc = doc
        self.grid = QGridLayout()
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.addButton = QPushButton("&Add PDF")
        self.addButton.clicked.connect(self.parent.addPDF)
        self.refresh()

    def refresh(self):
        item = self.grid.takeAt(0)
        while item:
            del item
            item = self.grid.takeAt(0)
        item = self.layout.takeAt(0)
        while item:
            del item
            item = self.layout.takeAt(0)
        files = self.doc.get_files()
        paths = self.doc.get_fullpaths()
        for index in range(len(files)):
            l = PDFLabel(files[index], paths[index])
            d = QPushButton()
            d.setIcon(QIcon.fromTheme("edit-delete"))
            d.setText("")
            d.setEnabled(False)  # TODO Delete this PDF
            self.grid.addWidget(l, index, 0)
            self.grid.addWidget(d, index, 1)
        self.layout.addLayout(self.grid)
        self.layout.addWidget(self.addButton)
        self.setLayout(self.layout)


class DocWindow(QWidget):
    def __init__(self, doc):
        super(DocWindow, self).__init__()
        self.doc = doc
        self.shortcuts = []
        self.modified = False
        self.setupKeybinds(KEYBINDS)
        self.makeUI()

    def makeUI(self):
        self.resize(400, 300)
        self.setWindowTitle("xapers-qt: Document editor")
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.entries = QGridLayout()
        self.lines = {}
        self.addPair("Key", self.doc.get_key())
        self.addPair("Title", self.doc.get_title())
        self.addPair("Year", self.doc.get_year())
        self.pdfs = PDFList(self, self.doc)
        self.layout.addLayout(self.entries)
        self.layout.addWidget(self.pdfs)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Save |
                                          QDialogButtonBox.Discard)
        self.layout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.saveAndClose)
        discard = self.buttonBox.button(QDialogButtonBox.Discard)
        discard.clicked.connect(self.resetAndClose)
        self.setLayout(self.layout)
        self.show()

    def saveAndClose(self):
        self.saveChanges()
        self.close()

    def resetAndClose(self):
        self.lines["Key"].setText(self.doc.get_key())
        self.lines["Title"].setText(self.doc.get_title())
        self.lines["Year"].setText(self.doc.get_year())
        self.modified = False
        self.close()

    def addPair(self, text, value, PDF=False):
        r = self.entries.rowCount()
        self.entries.addWidget(QLabel(text), r, 0)
        if PDF:
            l = QBoxLayout(QBoxLayout.LeftToRight)
            openPDFButton = QPushButton("&Open PDF")
            if not value:
                openPDFButton.setEnabled(False)
            else:
                print(value)
            l.addWidget(openPDFButton)
            selectPDFButton = QPushButton("&Select PDF")
            l.addWidget(selectPDFButton)
            self.entries.addLayout(l, r, 1)
        else:
            self.lines[text] = QLineEdit(value)
            self.entries.addWidget(self.lines[text], r, 1)

    def addPDF(self):
        fileName, group = QFileDialog.getOpenFileName(self, _("Open PDF"),
                                                      str(), "PDFs (*.pdf)")
        if fileName:
            if os.path.exists(fileName):
                self.doc.add_file(fileName)
                self.modified = True
        self.pdfs.refresh()

    def setupKeybinds(self, binds):
        for s in self.shortcuts:
            pass  # TODO Delete shortcut?
        for keys, action in binds:
            if action == "Exit":
                func = self.close
            else:
                action = None
            if action:
                shortcut = QShortcut(QKeySequence(keys), self)
                shortcut.activated.connect(func)
                self.shortcuts.append(shortcut)

    def closeEvent(self, event):
        if self.lines["Key"].text() != self.doc.get_key():
            self.modified = True
        if self.lines["Title"].text() != self.doc.get_title():
            self.modified = True
        if self.lines["Year"].text() != self.doc.get_year():
            self.modified = True
        if self.modified:
            m = QMessageBox.question(self, "Save changes?",
                                     ("Do you want to save the changes you "
                                      "made to this document?"))
            if m == QMessageBox.Yes:
                self.saveChanges()

    def saveChanges(self):
        self.doc.sync()
        self.modified = False


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
    def __init__(self):
        super(MainWindow, self).__init__()
        self.settings = QSettings("xapers-qt", "xapers-qt")
        self.shortcuts = []
        self.makeUI()

    def startSearch(self):
        self.resultWidget.doSearch(self.searchBar.text())

    def makeUI(self):
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
        self.resultWidget = ResultsWidget(self.settings)

        mainLayout.addWidget(self.searchBar)
        mainLayout.addWidget(self.resultWidget)
        self.central = QWidget()
        self.central.setLayout(mainLayout)
        self.setCentralWidget(self.central)
        self.setupKeybinds(KEYBINDS)
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


def main():
    app = QApplication(sys.argv)
    m = MainWindow()
    assert m
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
