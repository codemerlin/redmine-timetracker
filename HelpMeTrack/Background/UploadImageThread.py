from PySide import QtCore
import tempfile
from time import gmtime, strftime
import os
import paramiko


class UploadImageThread(QtCore.QThread):
    imageUploaded = QtCore.Signal(bool)

    def __init__(self, fileNameOnly, completeFileName, currentUser, partialFileName, parent=None):
        super(UploadImageThread, self).__init__(parent)
        self.exiting = False
        self.currentUser = currentUser
        self.partialFileName = partialFileName
        self.fileNameOnly = fileNameOnly
        self.completeFileName = completeFileName

    def run(self):
        # print(activities)
       try :
           self.sftpClient = paramiko.SSHClient()
           self.sftpClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
           self.sftpClient.connect("ti-images.cloudapp.net", 22, username='mthakral', password=')wl12345', timeout=4)
           sftp = self.sftpClient.open_sftp()
           basedirPath = '/home/mthakral/upload/' # + self.currentUser + '/' + strftime("%Y%m%d", gmtime())
           # self.mkdir_p(sftp,basedirPath, True)
           sftp.put(self.completeFileName, basedirPath + self.fileNameOnly)
           os.remove(self.completeFileName)
           print(self.completeFileName)
           self.imageUploaded.emit(True)
       finally:
           if self.sftpClient:
               self.sftpClient.close()

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
