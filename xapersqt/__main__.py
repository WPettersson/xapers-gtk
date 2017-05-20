#!/usr/bin/env python2

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

from xapersqt.XapersQt import XapersQt
import sys
import xapers


def __main__():
    db = xapers.Database('~/.xapers/docs', writable=True)

    keybinds = [["Ctrl+L", "Search"], ["j", "Next"], ["k", "Prev"],
                ["Enter", "OpenPDF"], ["o", "OpenDoc"],
                ["Esc", "Exit"], ["Ctrl+q", "Exit"]]
    app = XapersQt(sys.argv, db, keybinds)
    sys.exit(app.exec_())

if __name__ == "__main__":
    __main__()