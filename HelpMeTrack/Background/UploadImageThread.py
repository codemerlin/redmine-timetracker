from PySide import QtCore
import tempfile
from time import gmtime, strftime
import os
import paramiko


class UploadImageThread(QtCore.QThread):
    imageUploaded = QtCore.Signal(bool)

    def __init__(self, screenShotPixMap, currentUser, parent=None):
        super(UploadImageThread, self).__init__(parent)
        self.exiting = False
        self.screenShotPixMap = screenShotPixMap
        self.currentUser = currentUser

    def run(self):
        # print(activities)
        filenameSuffix = strftime("_%Y%m%d_%H-%M-%S.png", gmtime())
        dirname = tempfile.gettempdir()
        filenameOnly = self.currentUser + filenameSuffix
        completeFileName = dirname + os.path.sep + filenameOnly
        self.screenShotPixMap.toImage().save(completeFileName)
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect("ti-images.cloudapp.net", 22, username='mthakral', password=')wl12345', timeout=4)
        sftp = s.open_sftp()
        sftp.put(completeFileName, '/home/mthakral/upload/'+filenameOnly)
        print(completeFileName)
        self.imageUploaded.emit(True)
