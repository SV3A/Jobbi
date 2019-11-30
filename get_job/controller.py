import jobs as model
from datetime import datetime


class Controller():
    def __init__(self, view):
        target_urls = [
                "https://www.jobindex.dk/jobsoegning/ingenioer/" +
                "maskiningenioer/storkoebenhavn",
                "https://www.jobfinder.dk/jobs/category/maskin-produktion"]

        self.clock = datetime.now().time()

        # Initiate view- and model objects for the controller
        self._view  = view
        self._model = model.JobDB(target_urls)

        # Load stored data
        self.loadAdds(self._model.readData())

        # Setup signals and slots
        self._setupSignals()

    def loadAdds(self, adds):
        if adds is not None:
            adds.reverse()

            for add in adds:
                self._view.addJobElement(add)

    def refreshAdds(self):
        adds = self._model.fetchData()

        if adds is not None:
            self.loadAdds(adds)
            self._view.updateStatus("Updated at "+self.clock.strftime("%H:%M"))
        else:
            self._view.updateStatus("No new adds were found")

    def _setupSignals(self):
        self._view.loadButton.clicked.connect(self.refreshAdds)
