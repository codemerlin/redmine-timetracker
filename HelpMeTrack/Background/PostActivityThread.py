from PySide import QtCore


class PostActivityThread(QtCore.QThread):
    activityPosted = QtCore.Signal(bool)

    def __init__(self, redmineClient, time_entry,
                 parent=None):
        super(PostActivityThread, self).__init__(parent)
        self.time_entry = time_entry
        self.exiting = False
        self.redmineClient = redmineClient

    def run(self):
        status = self.redmineClient.post_time_entry(self.time_entry)
        # print(activities)
        self.activityPosted.emit(status)
