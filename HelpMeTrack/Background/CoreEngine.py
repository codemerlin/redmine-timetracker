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
from pprint import pprint
from random import randint


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
        self.currentUser = None
        print('Core engine created')

    def start(self):
        self.timeinMilliSeconds = self.timerIntervalCallback()
        print('Time after which entry would be posted : ' + str(self.timeinMilliSeconds/self.conversationToMinFactor) + " minutes" )
        self.screenShotTimer = ScreenShotTimer()
        self.screenShotTimer.start(self.postScreenShotTimer, self.timeinMilliSeconds)

    def cancel(self):
        self.screenShotTimer.stop()

    def setScreenShotLabel(self):
        self.screenShotLabel.setPixmap(self.screenShotPixMap.scaled(
            self.screenShotLabel.size(), QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation))

    def postScreenShotTimer(self, screenShotPixMap):
        self.screenShotPixMap = screenShotPixMap
        self.setScreenShotLabel()
        self.startPostActivityThread()
        if (self.currentUser is None):
            self.startGetCurrentUserThread()
        else:
            self.startUploadImageThread()
        self.start()

    def startPostActivityThread(self):
        timeEntry = TimeEntry(
            activity_id=self.activityIdCallback(),
            issue_id=self.issueId,
            comments=self.commentTextCallback(),
            time_in_minutes=self.timeinMilliSeconds / self.conversationToMinFactor )
        # pprint(vars(timeEntry))
        postActivityThread = PostActivityThread(self.redMineClient, timeEntry)
        postActivityThread.activityPosted.connect(
            self.postActivitiesPosted)
        if not postActivityThread.isRunning():
            postActivityThread.start()

    def postActivitiesPosted(self, status):
        if status:
            self.successHandler("Activity posted successfully")

    def startGetCurrentUserThread(self):
        currentUserThread = GetCurrentUserThread(self.redMineClient)
        currentUserThread.currentUserRecd.connect(self.postGetCurrentUser)
        if not currentUserThread.isRunning():
            currentUserThread.start()

    def postGetCurrentUser(self, user):
        self.currentUser = user
        self.startUploadImageThread()

    def startUploadImageThread(self):
        uploadImageThread = UploadImageThread(self.screenShotPixMap, self.currentUser)
        uploadImageThread.imageUploaded.connect(self.postImageUploaded)
        if not uploadImageThread.isRunning():
            uploadImageThread.start()

    def postImageUploaded(self, status):
        print(status)