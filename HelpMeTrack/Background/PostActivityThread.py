from PySide import QtCore


class PostActivityThread(QtCore.QThread):
    activityPosted = QtCore.Signal()

    def __init__(self, screenShot,redmineClient, parent=None):
        super(PostActivityThread, self).__init__(parent)
        self.exiting = False
        self.screenShot = screenShot
        self.redmineClient = redmineClient

    def run(self):
        status = self.redmineClient.post_time_entry()
        # print(activities)
        self.activitiesRecd.emit(status)
