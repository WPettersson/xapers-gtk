"""Contains the code for the main window of XapersQt, as well as all widgets
contained within it.
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

from xapersqt.ui_MainWindow import Ui_MainWindow

from PyQt5.QtWidgets import QShortcut, QMainWindow
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QKeySequence


class MainWindow(QMainWindow):
    """The main window, containing the search bar and results table."""
    def __init__(self, db, keybinds):
        super(MainWindow, self).__init__()
        self.settings = QSettings("xapers-qt", "xapers-qt")
        self.shortcuts = []
        self.db = db
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.results = self.ui.resultsWidget
        self.searchBar = self.ui.searchBar
        self.results.setDb(self.db)
        self.results.setSettings(self.settings)
        self.setupKeybinds(keybinds)
        self.restore_size()
        self.show()

    def restore_size(self):
        """Resize to size stored in settings.
        """
        try:
            width = int(self.settings.value("main/width", 800))
        except ValueError:
            width = 800
        try:
            height = int(self.settings.value("main/height", 300))
        except ValueError:
            height = 300
        self.resize(width, height)

    def startSearch(self):
        """Launches a search."""
        self.results.doSearch(self.searchBar.text())

    def setupKeybinds(self, binds):
        """Setup the keyboard shortcuts.
        """
        for shortcut in self.shortcuts:
            pass  # TODO Delete shortcut?
        for keys, action in binds:
            if action == "Search":
                func = self.focusSearchBar
            elif action == "Next":
                func = self.results.selectNext
            elif action == "Prev":
                func = self.results.selectPrev
            elif action == "OpenPDF":
                func = self.results.openPDF
            elif action == "OpenDoc":
                func = self.results.openDoc
            elif action == "Exit":
                func = self.close
            else:
                action = None
            if action:
                shortcut = QShortcut(QKeySequence(keys), self)
                shortcut.activated.connect(func)
                self.shortcuts.append(shortcut)

    def focusSearchBar(self):
        """Set focus to the search bar."""
        self.searchBar.searchLine.setFocus(Qt.ShortcutFocusReason)

    def saveSettings(self):
        """Save any settings we may have changed."""
        self.settings.setValue("main/width", self.width())
        self.settings.setValue("main/height", self.height())
        self.results.saveSettings()

    def closeEvent(self, event):
        """Things to do when closing the window.
        """
        self.saveSettings()

    def resizeEvent(self, resizeEvent):
        """Things to do when resizing the window.
        """
        self.results.refresh()
