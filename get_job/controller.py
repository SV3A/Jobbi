import jobs as model


class Controller():
    def __init__(self, view):
        self._view = view
        self._model = model.JobDB()
        self._setupSignals()

    def loadAdds(self):
        print("Loading adds")
        self._model.fetchJobs("jobindex")

        for add in self._model.adds:
            self._view.addJobElement(add)

    def _setupSignals(self):
        self._view.loadButton.clicked.connect(self.loadAdds)
