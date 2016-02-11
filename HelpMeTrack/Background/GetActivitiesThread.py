from PySide import QtCore


class GetActivitiesThread(QtCore.QThread):
    activitiesRecd = QtCore.Signal(list)

    def __init__(self, redmineClient, parent=None):
        super(GetActivitiesThread, self).__init__(parent)
        self.exiting = False
        self.redmineClient = redmineClient

    def run(self):
        activities = self.redmineClient.getActivities()
        # print(activities)
        self.activitiesRecd.emit(activities)
