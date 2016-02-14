from PySide import QtCore, QtGui


class ScreenShotTimer():

    def __init__(self):
        pass

    def start(self, callback, timeInMilliSeconds):
        self.currentCallback = callback
        self.timer = QtCore.QTimer()
        self.timer.setInterval(timeInMilliSeconds)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.captureScreenShot)
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def captureScreenShot(self):
        if self.currentCallback is not None:
            self.currentCallback(
                QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId()))
