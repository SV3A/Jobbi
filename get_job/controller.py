import jobs
import view


def startGUI():
    view.startView()
    readJobs()


def readJobs():
    jobs.fetchJobs()
