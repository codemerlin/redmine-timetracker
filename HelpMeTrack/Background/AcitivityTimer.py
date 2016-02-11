from PySide import QtCore, QtGui


class ActivityTimer(QtCore.QTimer):

    def __init__(self, parent=None):
        super(ActivityTimer, self).__init__(parent)

    def registerActivityCallBack(self, callback, collectComment):
        self.collectComment = collectComment
        self.currentCallback = callback
        self.stop()
        self.timeout.connect(self.postActivicty)
        # self.setSingleShot(True)
        # TODO:: change this to calculate random time
        randomMin = 10
        self.start(randomMin*6000)

    def postActivicty(self):

        if self.currentCallback is not None:
            self.currentCallback(
                QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId()))
