import sys
from util import link_format
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDesktopWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtWidgets import QStatusBar, QScrollArea
from PyQt5.QtWidgets import QLineEdit, QLabel, QTextEdit, QPushButton


class GetJobUI(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Get Job')
        self.setGeometry(0, 0, 980, 650)
        self.setMinimumWidth(800)
        self.setMinimumHeight(400)

        # Center main window
        qt_rectangle = self.frameGeometry()
        qt_rectangle.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qt_rectangle.topLeft())

        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        # Set central widget to be a scroll area
        self.mainScrollArea = QScrollArea(self)
        self.setCentralWidget(self.mainScrollArea)

        # Main job-add layout
        self.baseWidget = QWidget()
        self.generalLayout = QVBoxLayout()
        self.generalLayout.setContentsMargins(100, 20, 100, 20)
        self.baseWidget.setLayout(self.generalLayout)

        # Point baseWidget to the main scroll area
        self.mainScrollArea.setWidget(self.baseWidget)
        self.mainScrollArea.setWidgetResizable(True)

        # Create GUI components

        # List containing custom job add widgets
        self.addElements = []

        self._createLoadButton()
        self._createStatusBar()

    # Insert job add objects
    def addJobElement(self, jobAdd):
        element = _JobAddElement(jobAdd.add_heading,
                                 jobAdd.add_content,
                                 jobAdd.company,
                                 jobAdd.company_url,
                                 jobAdd.add_url,
                                 jobAdd.add_owner)

        # The first add element will have the index 2, with the current layout,
        # thus to insert new adds add the top of the list the insertWidget()
        # method is used insted of addWidget()
        self.generalLayout.insertWidget(2, element)

        self.addElements.append(element)

    def getIndices(self):
        for el in self.addElements:
            print(self.generalLayout.indexOf(el))

    def updateStatus(self, msg):
        self.status.showMessage(msg)
        self.update()

    def _createStatusBar(self):
        self.status = QStatusBar()
        self.status.showMessage("Welcome")
        self.setStatusBar(self.status)

    def _createLoadButton(self):
        self.loadButton = QPushButton("Load jobs")
        self.loadButton.setMaximumWidth(100)
        self.generalLayout.addWidget(self.loadButton)
        self.generalLayout.addStretch()


class _JobAddElement(QWidget):
    """ Class defining the job add GUI elements"""

    def __init__(self, heading, content, company, company_url, addurl,
                 add_owner):
        super(_JobAddElement, self).__init__()

        # Set background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#FAF4F4"))
        self.setPalette(palette)

        # Setup layout for the job adds
        self.setFixedHeight(200)
        self.setMinimumWidth(600)

        self.vertLayout = QVBoxLayout()
        self.setLayout(self.vertLayout)
        self.vertLayout.setContentsMargins(20, 10, 20, 15)

        self.horzLayout = QHBoxLayout()

        # Source icon
        logo = QLabel()
        pixmap = QtGui.QPixmap(add_owner + '.png')
        logo.setPixmap(pixmap.scaledToWidth(22))
        logo.setToolTip(add_owner.capitalize() + " add")

        # Add heading
        headingLabel = QLabel()

        # Truncate headings over 70 chars
        if len(heading) > 70:
            i = 70
            while heading[i] != " " or i == 1:
                i -= 1
            head_text = link_format(heading[0:i+1] + "...", addurl)
            headingLabel.setToolTip(heading)
        else:
            head_text = link_format(heading, addurl)

        headingLabel.setText(head_text)
        headingLabel.setOpenExternalLinks(True)
        headingLabel.setFont(QtGui.QFont("Helvetica", 14, QtGui.QFont.Bold))

        # Add company name
        companyLabel = QLabel()
        companyLabel.setFont(QtGui.QFont("Helvetica", 12, QtGui.QFont.Bold))
        companyLabel.setText(link_format(company, company_url))
        companyLabel.setOpenExternalLinks(True)

        # Make top row layout
        self.horzLayout.addWidget(logo)
        self.horzLayout.addWidget(headingLabel)
        self.horzLayout.addStretch()
        self.horzLayout.addWidget(companyLabel)
        self.vertLayout.addLayout(self.horzLayout)

        # Add content
        contentLabel = QTextEdit()
        contentLabel.setText(content)
        contentLabel.setReadOnly(True)
        contentLabel.setMaximumWidth(1000)
        # contentLabel.setFont(QtGui.QFont("Helvetica", 14))
        self.vertLayout.addWidget(contentLabel)


def initApp():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.png'))
    return app
