import jobs as model


class Controller():
    def __init__(self, view):
        self._view = view
        self._model = model.JobDB()
        self.loadAdds()
        self._setupSignals()

    def loadAdds(self):
        self._model.readData()

        for add in self._model.adds:
            self._view.addJobElement(add)

    def fetchAdds(self):
        self._model.fetchData()

    def _setupSignals(self):
        self._view.loadButton.clicked.connect(self.loadAdds)
