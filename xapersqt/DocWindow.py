import os
import gettext
from PyQt5.QtWidgets import (QWidget, QLineEdit, QBoxLayout,
                             QPushButton, QLabel,
                             QShortcut,
                             QGridLayout, QDialogButtonBox,
                             QFileDialog, QMessageBox)
from PyQt5.QtGui import (QKeySequence, QIcon)

gettext.bindtextdomain('xapers-qt', '/path/to/my/language/directory')
gettext.textdomain('xapers-qt')
_ = gettext.gettext


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
    def __init__(self, doc, keybinds):
        super(DocWindow, self).__init__()
        self.doc = doc
        self.shortcuts = []
        self.modified = False
        self.setupKeybinds(keybinds)
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
