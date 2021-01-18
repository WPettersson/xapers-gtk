#!/usr/bin/env python3


import sys
from xapersqt import XapersQt


dbpath = '~/.xapers/docs'

KEYBINDS = [["Ctrl+L", "Search"], ["j", "Next"], ["k", "Prev"],
            ["Enter", "OpenPDF"], ["o", "OpenDoc"],
            ["Esc", "Exit"], ["Ctrl+q", "Exit"]]


def main(args):
    app = XapersQt.XapersQt(sys.argv, dbpath, KEYBINDS)
    assert app
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)
