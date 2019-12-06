import os
import json
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


class ProviderDB:
    def __init__(self):
        self.dbFile = "settings.json"

    def writeData(self, provider_list):
        """ Write provider list to settings file """

        # Write data to json file
        with open(self.dbFile, "w", encoding="utf8") as write_file:
            json.dump(provider_list, write_file, indent=4,
                      separators=(',', ': '), ensure_ascii=False)

    def readData(self):
        """ Read provider list from settings file """

        if not os.path.isfile("./"+self.dbFile):
            return []

        with open(self.dbFile) as json_file:
            provider_list = json.load(json_file)

        return provider_list


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
