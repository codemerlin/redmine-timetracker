from PySide import QtCore
import tempfile
from time import gmtime, strftime
import os
import paramiko


class UploadImageThread(QtCore.QThread):
    imageUploaded = QtCore.Signal(bool)

    def __init__(self, screenShotPixMap, currentUser, partialFileName, parent=None):
        super(UploadImageThread, self).__init__(parent)
        self.exiting = False
        self.screenShotPixMap = screenShotPixMap
        self.currentUser = currentUser
        self.partialFileName = partialFileName

    def run(self):
        # print(activities)
        dirname = tempfile.gettempdir()
        filenameOnly = self.currentUser + self.partialFileName + ".png"
        completeFileName = dirname + os.path.sep + filenameOnly
        self.screenShotPixMap.toImage().save(completeFileName)
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect("ti-images.cloudapp.net", 22, username='mthakral', password=')wl12345', timeout=4)
        sftp = s.open_sftp()
        basedirPath = '/home/mthakral/upload/' # + self.currentUser + '/' + strftime("%Y%m%d", gmtime())
        # self.mkdir_p(sftp,basedirPath, True)
        sftp.put(completeFileName, basedirPath + filenameOnly)
        os.remove(completeFileName)
        print(completeFileName)
        self.imageUploaded.emit(True)

    def mkdir_p(self, sftp, remote, is_dir=False):
        """
        emulates mkdir_p if required.
        sftp - is a valid sftp object
        remote - remote path to create.
        """
        dirs_ = []
        if is_dir:
            dir_ = remote
        else:
            dir_, basename = remote.split('/')

        while len(dir_) > 1:
            dirs_.append(dir_)
            dir_, _ = os.path.split(dir_)

        if len(dir_) == 1 and not dir_.startswith("/"):
            dirs_.append(dir_)  # For a remote path like y/x.txt

        while len(dirs_):
            dir_ = dirs_.pop()
        try:
            sftp.stat(dir_)
        except:
            print "making ... dir", dir_
            sftp.mkdir(dir_)
