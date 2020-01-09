import os
import json
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QDialogButtonBox, QPushButton
from PyQt5.QtWidgets import QLineEdit, QListWidget, QLabel, QListWidgetItem
from PyQt5.QtWidgets import QAbstractItemView


class SettingsDialog(QDialog):
    """ Definition of the settings dialog view """

    def __init__(self, providerURLs, *args, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)

        self.urlItems = []  # Reference list of url-entry objects
        self.providerURLs = providerURLs

        self._setupDialog()
        self._createUrlList()

        # If the class is initiated with urls add them to the list object
        if len(providerURLs) > 0:
            self._initiateProviderList()

        # Add and remove buttons
        self.horzLayout.addStretch()
        self.horzLayout.addWidget(QLabel("Add or remove: "))

        self.addButton = QPushButton("+")
        self.addButton.setMaximumWidth(60)

        self.rmButton = QPushButton("-")
        self.rmButton.setEnabled(False)
        self.rmButton.setMaximumWidth(60)

        self.horzLayout.addWidget(self.addButton)
        self.horzLayout.addWidget(self.rmButton)
        self.vertLayout.addLayout(self.horzLayout)

        # Save and cancel buttons
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Save |
                                          QDialogButtonBox.Cancel)
        self.vertLayout.addWidget(self.buttonBox)

        # Signal to slot setup
        self._setupSignals()

    def _setupDialog(self):
        """ Sets up the window and layouts """
        self.setWindowTitle("Settings")

        self.vertLayout = QVBoxLayout()
        self.horzLayout = QHBoxLayout()

        self.setLayout(self.vertLayout)

    def _createUrlList(self):
        """ Sets up the url list containing the jobadd providers """
        self.vertLayout.addWidget(QLabel("URLs to scrape:"))
        self.providerList = QListWidget()
        self.providerList.setMinimumWidth(600)

        # Enable multi-line selection
        self.providerList.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.vertLayout.addWidget(self.providerList)

    def _setupSignals(self):
        """ Sets up the signals to slots"""
        # Save/cancel buttons
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Url add/remove button
        self.addButton.clicked.connect(self.addItem)
        self.rmButton.clicked.connect(self.removeItem)

        # Double click and selection of list items
        self.providerList.itemDoubleClicked.connect(self._handleDoubleClick)
        self.providerList.itemSelectionChanged.connect(self._handleSelChange)

    def _initiateProviderList(self):
        """ If the class is initiated with urls add them to the list object """
        for url in self.providerURLs:
            newItem = QListWidgetItem(str(url), self.providerList)
            self.urlItems.append(newItem)

    def addItem(self):
        """ Add new provider (url) """
        newItem = QListWidgetItem("https://", self.providerList)
        self.providerList.openPersistentEditor(newItem)
        # Add to reference list
        self.urlItems.append(newItem)

    def removeItem(self):
        """ Removed selected urls """
        for selected in self.providerList.selectedItems():
            # Find index in reference list
            rmIdx = self.urlItems.index(selected)
            # Remove from GUI
            self.providerList.takeItem(rmIdx)
            # Remove from reference list
            self.urlItems.pop(rmIdx)

    def _handleDoubleClick(self, item):
        """ Opens line for editing """
        self.providerList.openPersistentEditor(item)

    def _handleSelChange(self):
        """ Slot responsible for handling selection dependent states """
        if len(self.providerList.selectedItems()) > 0:
            self.rmButton.setEnabled(True)
        else:
            self.rmButton.setEnabled(False)

            # Close open line edits
            for item in self.urlItems:
                if self.providerList.isPersistentEditorOpen(item):
                    self.providerList.closePersistentEditor(item)


class ProviderDB:
    """ Model for the jobadd providers """

    def __init__(self):
        # Specification of the database file to be used
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
