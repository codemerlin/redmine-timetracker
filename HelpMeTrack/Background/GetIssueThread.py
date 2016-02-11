from PySide import QtCore


class GetIssueThread(QtCore.QThread):
    issueFound = QtCore.Signal(list)

    def __init__(self, redmineClient, issueId, parent=None):
        super(GetIssueThread, self).__init__(parent)
        self.exiting = False
        self.redmineClient = redmineClient
        self.issueId = issueId

    def run(self):
        issue = self.redmineClient.get_issue(self.issueId)
        # print(activities)
        self.issueFound.emit(issue)
