#!/bin/python3
# import json
# import scraper
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QVBoxLayout


class getJobUI(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Get Job')
        self.setGeometry(100, 100, 980, 650)
        self.move(250, 100)
        # Set central widget and general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # Create GUI components
        self._createStatusBar()

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("I'm the Status Bar")
        self.setStatusBar(status)


def main():
    app = QApplication([])
    app.setWindowIcon(QIcon('icon.png'))
    view = getJobUI()
    view.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

# Initiate scraper
# scraper = scraper.Jobindex()

# Parse
# scraper.parse_adds()

# Write adds to json file
# for add in scraper.adds:
#    with open("data.json", "a", encoding="utf8") as write_file:
#       json.dump(add.get_dict(), write_file, indent=4, separators=(',', ': '),
#                  ensure_ascii=False)
