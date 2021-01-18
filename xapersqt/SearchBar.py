"""The search bar.
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


from xapersqt.ui_SearchBar import Ui_SearchBar
from PyQt5.QtWidgets import QWidget


class SearchBar(QWidget):
    """Contains the edit box for entering a search query, and the button to
    start a search.
    """
    def __init__(self, parent):
        super(SearchBar, self).__init__()
        self.parent = parent.parent()
        self.ui = Ui_SearchBar()
        self.ui.setupUi(self)
        self.ui.searchButton.clicked.connect(self.parent.startSearch)
        self.ui.searchLine.returnPressed.connect(self.parent.startSearch)

    def text(self):
        """Return the current search query term."""
        return self.ui.searchLine.text()

    @property
    def searchLine(self):
        """The actual LineEdit."""
        return self.ui.searchLine
