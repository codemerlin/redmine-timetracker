from PySide import QtCore, QtGui


class ScreenShotTimer(QtCore.QTimer):

    def __init__(self, parent=None):
        super(ScreenShotTimer, self).__init__(parent)

    def registerScreenShotCallback(self, callback):
        self.currentCallback = callback
        self.stop()
        self.timeout.connect(self.captureScreenShot)
        # self.setSingleShot(True)
        # TODO:: change this to calculate random time
        randomMin = 1
        self.start(randomMin*6000)

    def captureScreenShot(self):
        if self.currentCallback is not None:
            self.currentCallback(
                QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId()))
