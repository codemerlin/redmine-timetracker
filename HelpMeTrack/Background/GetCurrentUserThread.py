from PySide import QtCore
import tempfile
from time import gmtime, strftime


class GetCurrentUserThread(QtCore.QThread):
    currentUserRecd = QtCore.Signal(str)

    def __init__(self, redMineClient, parent=None):
        super(GetCurrentUserThread, self).__init__(parent)
        self.exiting = False
        self.redMineClient = redMineClient

    def run(self):
        self.currentUserRecd.emit(self.redMineClient.getCurrentUser())