import sys
import settings
import addslogic as al
from util import link_format
from main import img_path
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDesktopWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QToolBar, QAction, QStatusBar, QScrollArea
from PyQt5.QtWidgets import QLabel, QTextEdit


class JobbiUI(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Init window
        self._setupWindow()

        # List containing custom job add widgets
        self.addElements = []

        # Init UI and create GUI components
        self._createToolBar()
        self._setupUI()
        self._createStatusBar()

    def insertJobs(self, adds):
        if adds is not None:
            adds = al.shuffle_adds(adds)
            adds.reverse()

            for add in adds:
                self.insertJobElement(add)

    # Insert job add objects
    def insertJobElement(self, jobAdd):
        element = _JobAddElement(jobAdd.add_heading,
                                 jobAdd.add_content,
                                 jobAdd.company,
                                 jobAdd.company_url,
                                 jobAdd.add_url,
                                 jobAdd.add_owner)

        # The first add element will have the index 0, with the current layout,
        # thus to insert new adds add the top of the list the insertWidget()
        # method is used insted of addWidget()
        self.generalLayout.insertWidget(0, element)

        self.addElements.append(element)

    def getIndices(self):
        for el in self.addElements:
            print(self.generalLayout.indexOf(el))

    def updateStatus(self, msg):
        self.status.showMessage(msg)
        self.update()

    def _setupUI(self):
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

    def _createToolBar(self):
        # Define main toolbar
        self.toolbar = QToolBar("Main toolbar")
        self.addToolBar(self.toolbar)
        self.toolbar.setIconSize(QSize(22, 22))
        self.toolbar.setFixedHeight(36)

        # Define action to be included in the toolbar and add them to it
        self.settingsAction = QAction(QIcon(str(img_path/"build-24px.svg")),
                                      "Settings", self)
        self.updateAction = QAction(QIcon(
            str(img_path/"cloud_download-24px.svg")), "Load adds", self)

        self.toolbar.addAction(self.settingsAction)
        self.toolbar.addAction(self.updateAction)

    def _createStatusBar(self):
        self.status = QStatusBar()
        self.status.showMessage("Welcome")
        self.setStatusBar(self.status)

    def _setupWindow(self):
        self.setWindowTitle('Jobbi')
        self.setGeometry(0, 0, 990, 660)
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


class _JobAddElement(QWidget):
    """ Class defining the job add GUI elements"""

    def __init__(self, heading, content, company, company_url, addurl,
                 add_owner):
        super(_JobAddElement, self).__init__()

        # Set background color
        if add_owner == "jobindex":
            bcColor = "#FAF4F4"
        elif add_owner == "jobfinder":
            bcColor = "#F7FBFD"
        else:
            bcColor = "#F4F4F4"

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(bcColor))
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
        pixmap = QtGui.QPixmap(str(img_path / (add_owner+'.png')))
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
    app.setWindowIcon(QIcon(str(img_path/"icon.png")))
    return app
