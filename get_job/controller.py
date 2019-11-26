import jobs as model
# from functools import partial
# from PyQt5.QtCore import QObject, pyqtSlot


class Test():
    def __init__(self):
        testhead = "Global Key Account Manager for responsible business growth"
        testtext = "Elma Instruments A/S, " +\
                   "Farum\nVi har forrygende travlt og søg er derfor " +\
                   "hurtigst muligt en maskinmester med el erfaring eller " +\
                   "el-installatør til vores salgs- & support afdeling i " +\
                   "Farum. Du kommer til at arbejde i en dynamisk afdeling " +\
                   "med otte gode kollegaer, hvor alle hjælper alle og " +\
                   "hvor du samtidigt bliver du fagligt udfordret."

        self.add_heading = testhead
        self.add_content = testtext


class Ctrlr():
    def __init__(self, view):
        self._view = view
        self._setupSignals()

    def loadAdds(self):
        print("Loading adds")
        return
        adds = model.fetchJobs()

        for add in adds:
            self._view.addJobElement(add)

    def _setupSignals(self):
        # lolz = [Test()]
        # self._view.loadButton.clicked.connect(partial(self._view.addJobElement,
        #                                     # lolz))
        self._view.loadButton.clicked.connect(self.loadAdds)
