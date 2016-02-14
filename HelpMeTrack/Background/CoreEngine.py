from PySide import QtCore
from HelpMeTrack.Background.ScreenShotTimer \
    import ScreenShotTimer
from HelpMeTrack.Background.PostActivityThread \
    import PostActivityThread
from HelpMeTrack.Shared.RedMineClient \
    import TimeEntry
from HelpMeTrack.Background.UploadImageThread \
    import UploadImageThread
from HelpMeTrack.Background.GetCurrentUserThread \
    import GetCurrentUserThread
from time import gmtime, strftime, localtime
import uuid
import tempfile
from time import gmtime, strftime
import os


class CoreEngine(object):
    def __init__(self, labelToShowSS, redMineClient,
                 errorHandler, successHandler,
                 issueId, activityIdCallback, commentTextCallback,
                 timerIntervalCallback, conversationToMinFactor,
                 parent=None):
        super(CoreEngine, self).__init__()
        self.screenShotLabel = labelToShowSS
        self.redMineClient = redMineClient
        self.errorHandler = errorHandler
        self.successHandler = successHandler
        self.issueId = issueId
        self.activityIdCallback = activityIdCallback
        self.commentTextCallback = commentTextCallback
        self.timerIntervalCallback = timerIntervalCallback
        self.conversationToMinFactor = conversationToMinFactor
        self.uploadImageThreadList = []
        self.postActivityThreadList = []
        self.currentUser = None
        print('Core engine created')

    def start(self):
        self.timeinMilliSeconds = self.timerIntervalCallback()
        # print('Time after which, next entry would be posted : ' + str(
        #     self.timeinMilliSeconds / self.conversationToMinFactor) + " minutes")
        self.trackerId = uuid.uuid4()
        print(' Current time is :: ' + strftime("%Y-%m-%d %H:%M:%S", localtime()))
        print(" look for :: " + str(self.trackerId) + " To track the entry ")
        self.screenShotTimer = ScreenShotTimer()
        self.screenShotTimer.start(self.postScreenShotTimer, self.timeinMilliSeconds)

    def stop(self):
        if (self.screenShotTimer is not None):
            self.screenShotTimer.stop()
        QtCore.QTimer().singleShot(6000,self.postStopCleanup)
        self.cleanPostActivityThreadList()
        self.cleanUploadImageThreadList()

    def postStopCleanup(self):
        self.cleanPostActivityThreadList()
        self.cleanUploadImageThreadList()

    def setScreenShotLabel(self):
        self.screenShotLabel.setPixmap(self.screenShotPixMap.scaled(
            self.screenShotLabel.size(), QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation))

    def postScreenShotTimer(self, screenShotPixMap):
        self.screenShotPixMap = screenShotPixMap
        self.partialFileName = "_" + str(self.issueId) + strftime("_%Y%m%d_%H-%M-%S", gmtime())
        # print(" kicking of threads for : "+ self.partialFileName )
        print(" threads are starting for tracking id :: " + str(self.trackerId))
        if (self.currentUser is None):
            self.startGetCurrentUserThread()
        else:
            self.startUploadImageThread()
        self.startPostActivityThread()
        self.setScreenShotLabel()
        self.start()

    def startPostActivityThread(self):
        self.timeEntry = TimeEntry(
            activity_id=self.activityIdCallback(),
            issue_id=self.issueId,
            comments=self.commentTextCallback() + " -- " + self.partialFileName,
            time_in_minutes=self.timeinMilliSeconds / self.conversationToMinFactor)
        self.cleanPostActivityThreadList()
        # if (self.postActivityThread is not None and self.postActivityThread.isRunning()):
        #     while (self.postActivityThread.isRunning()):
        #         print('postActivity thread is running')

        # pprint(vars(timeEntry))
        postActivityThread = PostActivityThread(self.redMineClient, self.timeEntry)
        postActivityThread.activityPosted.connect(
            self.postActivitiesPosted)
        if not postActivityThread.isRunning():
            postActivityThread.start()
        self.postActivityThreadList.append(postActivityThread)

    def postActivitiesPosted(self, status):
        if status:
            self.successHandler("Activity posted successfully")

    def startGetCurrentUserThread(self):
        self.currentUserThread = GetCurrentUserThread(self.redMineClient)
        self.currentUserThread.currentUserRecd.connect(self.postGetCurrentUser)
        if not self.currentUserThread.isRunning():
            self.currentUserThread.start()

    def postGetCurrentUser(self, user):
        self.currentUser = user
        self.startUploadImageThread()

    def startUploadImageThread(self):
        self.serializeImage()
        # if (self.uploadImageThread is not None and self.uploadImageThread.isRunning()):
        #     while (self.uploadImageThread.isRunning()):
        #         print('uplaodImageThread is running')
        self.cleanUploadImageThreadList()
        uploadImageThread = UploadImageThread(self.filenameOnly, self.completeFileName, self.currentUser,
                                                   self.partialFileName)
        uploadImageThread.imageUploaded.connect(self.postImageUploaded)
        if not uploadImageThread.isRunning():
            uploadImageThread.start()
        self.uploadImageThreadList.append(uploadImageThread)

    def cleanPostActivityThreadList(self):
        newList = []
        for thread in self.postActivityThreadList:
            if(thread.isRunning()):
                newList.append(thread)
        self.postActivityThreadList = newList

    def cleanUploadImageThreadList(self):
        newList = []
        for thread in self.uploadImageThreadList:
            if(thread.isRunning()):
                newList.append(thread)
        self.uploadImageThreadList = newList


    def serializeImage(self):
        dirname = tempfile.gettempdir()
        self.filenameOnly = self.currentUser + self.partialFileName + ".png"
        self.completeFileName = dirname + os.path.sep + self.filenameOnly
        self.screenShotPixMap.toImage().save(self.completeFileName)

    def postImageUploaded(self, status):
        print(status)
