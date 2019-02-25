"""Runs the program if called as a module."""

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

import sys
import xapers
from xapersqt.XapersQt import XapersQt


def __main__():
    db = '~/.xapers/docs'

    keybinds = [["Ctrl+L", "Search"], ["j", "Next"], ["k", "Prev"],
                ["Enter", "OpenPDF"], ["o", "OpenDoc"],
                ["Esc", "Exit"], ["Ctrl+q", "Exit"]]
    app = XapersQt(sys.argv, db, keybinds)
    sys.exit(app.exec_())


if __name__ == "__main__":
    __main__()
