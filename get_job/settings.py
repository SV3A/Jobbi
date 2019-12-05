from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QDialogButtonBox, QPushButton
from PyQt5.QtWidgets import QLineEdit, QListWidget, QLabel, QListWidgetItem


class SettingsDialog(QDialog):

    def __init__(self, providerURLs, *args, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)

        self.urlItems = []
        self.providerURLs = providerURLs

        self._setupDialog()
        self._createUrlList()

        if len(providerURLs) > 0:
            self._initiateProviderList()

        # Add or remove buttons
        self.horzLayout.addStretch()
        self.horzLayout.addWidget(QLabel("Add or remove: "))

        self.addButton = QPushButton("+")
        self.addButton.setMaximumWidth(60)

        self.rmButton = QPushButton("-")
        self.rmButton.setMaximumWidth(60)

        self.horzLayout.addWidget(self.addButton)
        self.horzLayout.addWidget(self.rmButton)
        self.vertLayout.addLayout(self.horzLayout)

        # Save and cancel buttons
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Save |
                                          QDialogButtonBox.Cancel)
        self.vertLayout.addWidget(self.buttonBox)

        # Signal to slot setup
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.addButton.clicked.connect(self.addItem)
        self.rmButton.clicked.connect(self.removeItem)

    def _setupDialog(self):
        """ Sets up the window and layouts """
        self.setWindowTitle("Settings")

        self.vertLayout = QVBoxLayout()
        self.horzLayout = QHBoxLayout()

        self.setLayout(self.vertLayout)

    def _initiateProviderList(self):

        for url in self.providerURLs:
            newItem = QListWidgetItem(str(url), self.providerList)
            self.urlItems.append(newItem)

    def addItem(self):
        newItem = QListWidgetItem("https://", self.providerList)
        self.providerList.openPersistentEditor(newItem)
        self.urlItems.append(newItem)

    def removeItem(self):
        if len(self.urlItems) > 0:
            self.providerList.takeItem(len(self.urlItems)-1)
            self.urlItems.pop()

    def _createUrlList(self):
        self.vertLayout.addWidget(QLabel("URLs to scrape:"))
        self.providerList = QListWidget()
        self.providerList.setMinimumWidth(600)
        self.vertLayout.addWidget(self.providerList)


# Entry point for debugging purposes
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    target_urls = [
            "https://www.jobindex.dk/",
            "https://www.jobfinder.dk/"]

    app = QApplication(sys.argv)
    window = SettingsDialog(target_urls)
    window.show()
    sys.exit(app.exec_())
