"""Various UI elements for PDFs"""

from PyQt5.QtWidgets import (QWidget, QBoxLayout, QPushButton, QLabel,
                             QGridLayout)
from PyQt5.QtGui import QIcon


class PDFLabel(QLabel):
    """A label for a PDF, including a link."""
    def __init__(self, text, url):
        super(PDFLabel, self).__init__()
        markup = "<a href=\"%s\">%s</a>" % (url, text)
        self.setText(markup)
        self.setOpenExternalLinks(True)


class PDFList(QWidget):
    """A list of PDFs for a document."""
    def __init__(self, parent):
        super(PDFList, self).__init__()
        self.doc = None
        self.doc_window = None
        self.parent = parent
        self.addButton = QPushButton("&Add PDF")
        self.grid = QGridLayout()
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)

    def set_doc_window(self, doc_window):
        """Set the doc_window of this list of PDFs."""
        self.doc_window = doc_window
        self.addButton.clicked.connect(self.doc_window.addPDF)

    def set_doc(self, doc):
        """Set document."""
        self.doc = doc
        self.refresh()

    def refresh(self):
        """Refresh list of PDF documents."""
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
        for index, (path, name) in enumerate(zip(paths, files)):
            label = PDFLabel(name, path)
            delete = QPushButton()
            delete.setIcon(QIcon.fromTheme("edit-delete"))
            delete.setText("")
            delete.setEnabled(False)  # TODO Delete this PDF
            self.grid.addWidget(label, index, 0)
            self.grid.addWidget(delete, index, 1)
        self.layout.addLayout(self.grid)
        self.layout.addWidget(self.addButton)
        self.setLayout(self.layout)
