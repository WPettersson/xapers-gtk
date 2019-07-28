"""Describes the window and widgets which show details about an individual
document in the database.
"""

import os
import gettext
from PyQt5.QtWidgets import (QWidget, QShortcut, QDialogButtonBox, QFileDialog,
                             QMessageBox)
from PyQt5.QtGui import QKeySequence

from xapersqt.ui_DocWindow import Ui_DocWindow


gettext.bindtextdomain('xapers-qt', '/path/to/my/language/directory')
gettext.textdomain('xapers-qt')
_ = gettext.gettext


class DocWindow(QWidget):
    """A window showing details (and allowing editing) of one document.
    """
    def __init__(self, doc, keybinds=None):
        super(DocWindow, self).__init__()
        self.doc = doc
        self.shortcuts = []
        self.modified = False
        self.ui = Ui_DocWindow()
        self.ui.setupUi(self)
        self.setup_doc()
        self.tag_list = self.ui.tag_list
        self.pdfs = self.ui.pdf_list
        self.pdfs.set_doc_window(self)
        self.pdfs.set_doc(self.doc)
        self.refresh_tags()
        self.ui.buttonBox.accepted.connect(self.saveAndClose)
        (self.ui.buttonBox.button(QDialogButtonBox.Discard)
         .clicked.connect(self.resetAndClose))
        if keybinds:
            self.setupKeybinds(keybinds)
        self.show()

    def setup_doc(self):
        """Setup the labels referring to the document."""
        self.ui.key.setText(self.doc.get_key())
        self.ui.title.setText(self.doc.get_title())
        self.ui.year.setText(self.doc.get_year())

    def saveAndClose(self):
        """Save changes and close."""
        self.saveChanges()
        self.close()

    def resetAndClose(self):
        """Reset any changes, and close."""
        self.ui.key.setText(self.doc.get_key())
        self.ui.title.setText(self.doc.get_title())
        self.ui.year.setText(self.doc.get_year())
        self.modified = False
        self.close()

    def refresh_tags(self):
        """Refresh the list of tags."""
        text = " ".join(chr(0x1F3F7 + tag) for tag in self.doc.get_tags())
        self.tag_list.setText(text)

    def addPDF(self):
        """Add a new PDF to this document."""
        fileName, group = QFileDialog.getOpenFileName(self, _("Open PDF"),
                                                      str(), "PDFs (*.pdf)")
        if fileName:
            if os.path.exists(fileName):
                self.doc.add_file(fileName)
                self.modified = True
        self.pdfs.refresh()

    def setupKeybinds(self, binds):
        """Setup any shortcuts."""
        for shortcut in self.shortcuts:
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
        """Window being closed. Save if changes are detected."""
        if self.ui.key.text() != self.doc.get_key():
            self.modified = True
        if self.ui.title.text() != self.doc.get_title():
            self.modified = True
        if self.ui.year.text() != self.doc.get_year():
            self.modified = True
        if self.modified:
            m = QMessageBox.question(self, "Save changes?",
                                     ("Do you want to save the changes you "
                                      "made to this document?"))
            if m == QMessageBox.Yes:
                self.saveChanges()

    def saveChanges(self):
        """Save any changes made to the document."""
        self.doc.sync()
        self.modified = False
