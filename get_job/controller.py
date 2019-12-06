import settings
import jobs as model
from datetime import datetime


class Controller():
    def __init__(self, view):
        self.clock = datetime.now().time()

        # Read settings
        self._settings_model = settings.ProviderDB()
        provider_urls = self._settings_model.readData()

        # Initiate main model object
        self._model = model.JobDB(provider_urls)

        # Initiate main view and settings view
        self._view = view
        self._view.settingsDlg = settings.SettingsDialog(provider_urls)

        # Load stored data
        self.loadAdds(self._model.readData())

        # Setup signals and slots
        self._setupSignals()

    def loadAdds(self, adds):
        """ Insert adds into view """
        self._view.insertJobs(adds)

    def refreshAdds(self):
        """
        Slot for update button in toolbar: Calls DB to fetch adds add sends
        them to the view.
        """
        adds = self._model.fetchData()

        if adds is not None:
            self.loadAdds(adds)
            self._view.updateStatus("Updated at "+self.clock.strftime("%H:%M"))
        else:
            self._view.updateStatus("No new adds were found")

    def getSettings(self, s):
        """
        Slot for settings button in toolbar: Reads the gui list object con-
        taining the provider urls and writes them to disk.
        """
        new_providerlist = []

        if self._view.settingsDlg.exec_():
            # If save
            for url in self._view.settingsDlg.urlItems:
                new_providerlist.append(url.text().lower().strip())

            self._model.target_urls = new_providerlist
            self._settings_model.writeData(new_providerlist)
        else:
            # If cancel
            pass

    def _setupSignals(self):
        # Load adds toolbar button
        self._view.updateAction.triggered.connect(self.refreshAdds)

        # Settings toolbar button
        self._view.settingsAction.triggered.connect(self.getSettings)
