"""Functions for import new documents.
"""

from xapers.documents import Document
from xapers.source import Sources

from xapersqt.ui_ImportWindow import Ui_ImportWindow

from PyQt5.QtWidgets import QWidget, QMessageBox

class ImportWindow(QWidget):
    """A window where a user can enter a URL, and optionally drop a PDF.
    """
    def __init__(self, parent, db):
        super(ImportWindow, self).__init__()
        self._sources = Sources()
        self._parent = parent
        self._db = db
        self._ui = Ui_ImportWindow()
        self._ui.setupUi(self)
        self._ui.buttonBox.accepted.connect(self.try_add)
        self._ui.buttonBox.rejected.connect(self.close)
        self.show()

    def try_add(self):
        """Try to add a document based on a source."""
        source_string = self._ui.source_string.text()
        source = self._sources.match_source(source_string)
        if not source:
            box = QMessageBox()
            box.setText(f"Could not find \"{source_string}\" as a document.")
            box.exec_()
            return
        # Check to see if it already exists
        in_db = self._db.doc_for_source(source.sid)
        if in_db:
            # Already found this thing in the database
            doc = in_db
        else:
            bibtex = source.fetch_bibtex()
            doc = Document(self._db)
            if bibtex:
                doc.add_bibtex(bibtex)
            doc.add_sid(source.sid)
            doc.sync()
        self._parent.openDoc(doc)
        self.close()
