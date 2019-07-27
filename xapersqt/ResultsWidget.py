"""The list of search results
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


from PyQt5.QtWidgets import QStackedWidget

from xapersqt.ui_ResultsWidget import Ui_ResultsWidget


class ResultsWidget(QStackedWidget):
    """The widget in the results window which lists all the results."""
    def __init__(self, parent):
        super(ResultsWidget, self).__init__()
        self.settings = None
        self.parent = parent
        self.db = None
        self.children = []
        self.ui = Ui_ResultsWidget()
        self.ui.setupUi(self)
        self.setCurrentIndex(0)
        self.papers = self.ui.papersTable

    def setDb(self, db):
        """Set the database object."""
        self.db = db

    def setSettings(self, settings):
        """Set the settings object."""
        if settings:
            self.settings = settings
            self.papers.set_settings(self.settings)

    def doSearch(self, searchString=""):
        """Run a search with the given string. No results are directly
        returned, instead they are displayed in the table inside this widget.
        """
        docs = self.db.search(searchString)
        if not docs:
            self.setCurrentIndex(0)
        else:
            self.papers.add_results(docs)
            self.setCurrentIndex(1)

    def saveSettings(self):
        """Save the settings of the table of results.
        """
        self.papers.saveSettings()

    def selectNext(self):
        """Select the next document."""
        self.papers.selectNext()

    def selectPrev(self):
        """Select the previous document."""
        self.papers.selectPrev()

    def openPDF(self):
        """Open the associated PDF. If there is none, takes no actions."""
        self.papers.openPDF()

    def openDoc(self):
        """Open the highlighted document. This creates a new window allowing
        the user to edit the data relating to said document.
        """
        self.children.append(self.papers.openDoc())

    def refresh(self):
        """Refresh the view."""
        self.papers.refresh()
