import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDesktopWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QStatusBar, QScrollArea
from PyQt5.QtWidgets import QLineEdit, QLabel, QTextEdit, QPushButton


class getJobUI(QMainWindow):
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
        self._createLoadButton()
        self._createStatusBar()

    # Insert job add objects
    def addJobElement(self, adds):
        for add in adds:
            self.generalLayout.addWidget(_JobAddElement(add.add_heading,
                                                        add.add_content))

    def updateStatus(self, msg):
        self.status.showMessage(msg)

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

    def __init__(self, heading, content, *args, **kwargs):
        super(_JobAddElement, self).__init__(*args, **kwargs)

        # Set background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#E5E5E5"))
        self.setPalette(palette)

        # Setup layout for job add
        self.setFixedHeight(200)
        self.setMinimumWidth(600)
        self.subLayout = QVBoxLayout()
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


def initApp():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.png'))
    return app
