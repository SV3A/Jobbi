#!/bin/python3
# import json
# import scraper
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDesktopWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QStatusBar, QScrollArea
from PyQt5.QtWidgets import QLineEdit, QLabel, QTextEdit


class getJobUI(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Get Job')
        self.setGeometry(0, 0, 980, 650)

        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        # Center main window
        qt_rectangle = self.frameGeometry()
        qt_rectangle.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qt_rectangle.topLeft())

        # Set central widget and general layout
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)

        self.generalLayout = QVBoxLayout()
        self._centralWidget.setLayout(self.generalLayout)

        self.generalLayout.setContentsMargins(100, 20, 100, 20)

        # Insert job add objects
        testhead = "Global Key Account Manager for responsible business growth"
        testtext = "Elma Instruments A/S, " +\
                   "Farum\nVi har forrygende travlt og søg er derfor " +\
                   "hurtigst muligt en maskinmester med el erfaring eller " +\
                   "el-installatør til vores salgs- & support afdeling i " +\
                   "Farum. Du kommer til at arbejde i en dynamisk afdeling " +\
                   "med otte gode kollegaer, hvor alle hjælper alle og " +\
                   "hvor du samtidigt bliver du fagligt udfordret."

        for i in range(10):
            self.generalLayout.addWidget(JobAdd(testhead, testtext))

        # Create GUI components
        self._createStatusBar()

    # def _createCenterPane(self):
        # self.centerPaneLayout = QVBoxLayout()
        # self.generalLayout.addLayout(self.centerPaneLayout)

    # def _addPane(self):
        # p1 = QLineEdit()
        # p1.setAlignment(Qt.AlignRight)
        # p1.setReadOnly(True)

        # self.centerPaneLayout.addWidget(p1)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Loading job adds...")
        self.setStatusBar(status)


class JobAdd(QWidget):
    def __init__(self, heading, content, *args, **kwargs):
        super(JobAdd, self).__init__(*args, **kwargs)

        # Set background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#E5E5E5"))
        self.setPalette(palette)

        # Setup layout for job add
        self.setFixedHeight(200)
        self.setMinimumWidth(600)
        self.subLayout      = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self._centralWidget.setLayout(self.subLayout)
        self.subLayout.setContentsMargins(10, 10, 10, 10)

        # Add heading
        headingLabel = QLabel()
        headingLabel.setText(heading)
        headingLabel.setFont(QtGui.QFont("Helvetica", 18, QtGui.QFont.Bold))
        self.subLayout.addWidget(headingLabel)

        # Add content
        contentLabel = QTextEdit()
        contentLabel.setFixedHeight(100)
        contentLabel.setText(content)
        contentLabel.setReadOnly(True)
        contentLabel.setFont(QtGui.QFont("Helvetica", 14))
        self.subLayout.addWidget(contentLabel)


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
