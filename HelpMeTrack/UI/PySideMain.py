import os
import sys
import json
from PySide import QtCore, QtGui
import re
from HelpMeTrack.Shared.RedMineClient import RedMineClient
import SettingsDialogModule as SettingsDialogModule
from HelpMeTrack.Background.GetIssueThread import GetIssueThread
from HelpMeTrack.Background.GetActivitiesThread \
    import GetActivitiesThread
from HelpMeTrack.Background.ScreenShotTimer \
    import ScreenShotTimer


class HelpMeTrack(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        # # Set Window properties and create controls
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowTitle("Redmine Time Tracker")
        self.setWindowIcon(QtGui.QIcon(
            self.resource_path('redmine_fluid_icon.gif')))
        self.status_label = QtGui.QLabel()
        self.issueIdBox = QtGui.QLineEdit()
        self.issue_btn = QtGui.QPushButton("Find")
        self.settings_btn = QtGui.QPushButton("Settings")
        self.issue_subject_label = QtGui.QLabel()
        activity_label = QtGui.QLabel("Activity :")
        self.activity_combobox = QtGui.QComboBox()
        time_in_min_label = QtGui.QLabel("Time in Min :")
        self.time_in_min_box = QtGui.QLineEdit()
        comments_label = QtGui.QLabel("Comments :")
        self.comments_box = QtGui.QTextEdit()
        self.screenShotLabel = QtGui.QLabel()
        self.screenShotPixMap = QtGui.QPixmap(400, 300)
        self.screenShotPixMap.fill(QtCore.Qt.white)
        self.screenShotLabel.setPixmap(self.screenShotPixMap.scaled(
            self.screenShotLabel.size(), QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation))
        self.configureLayout(activity_label, comments_label,
                             time_in_min_label)
        self.attach_events()
        self.createTimers()
        self.setFixedSize(410, 510)
        # self.activity_thread = threading.Thread()
        settings = self.read_settings(show_error=False)
        if settings is None:
            QtGui.QMessageBox.warning(self, "Settings Missing",
                                      "Please use \
                                      settings button to provide settings")
        else:
            self.reset_from()

    def createTimers(self):
        self.postTimer = QtCore.QTimer(self)
        self.postTimer.timeout.connect(self.postEntry)
        self.postTimer.start(1000)
        self.screenShotTimer = ScreenShotTimer()
        self.screenShotTimer.stop()
        self.screenShotTimer.registerScreenShotCallback(
            self.setScreenShotLabel)

    def read_settings(self, show_error=True):
        settings = None
        try:
            with open('settings.json', 'r') as json_file:
                settings = json.load(json_file)
        except Exception:
            if show_error:
                self.settings_file_error()
            return settings
        if settings is None:
            if show_error:
                self.settings_file_error()
            return settings
        if (settings['api_key'] == '' or
                settings['server_url'] == '' or
                settings['time_in_minutes'] == ''):
            if show_error:
                self.settings_file_error()
            return settings
        if not self.is_valid_url(settings['server_url']):
            if show_error:
                self.settings_file_error()
            return settings
        return settings

    def is_valid_url(self, url):
        regex = re.compile(
            r'^https?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url is not None and regex.search(url)

    # region UI Functions
    def configureLayout(self, activity_label, comments_label,
                        time_in_min_label):
        # Prepare and configure GridLayout
        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(self.status_label, 0, 0, 1, 3)
        gridLayout.addWidget(self.issueIdBox, 1, 0)
        gridLayout.addWidget(self.issue_btn, 1, 1)
        gridLayout.addWidget(self.settings_btn, 1, 2)
        gridLayout.addWidget(self.issue_subject_label, 2, 0, 1, 3)
        gridLayout.addWidget(activity_label, 3, 0)
        gridLayout.addWidget(self.activity_combobox, 3, 1, 1, 2)
        # gridLayout.addWidget(time_in_min_label, 4, 0)
        # gridLayout.addWidget(self.time_in_min_box, 4, 1, 1, 2)
        gridLayout.addWidget(comments_label, 4, 0, 1, 3)
        # gridLayout.addWidget(comments_label, 5, 0, 1, 3)
        gridLayout.addWidget(self.comments_box, 5, 0, 1, 3)
        # gridLayout.addWidget(self.comments_box, 6, 0, 1, 3)
        gridLayout.addWidget(self.screenShotLabel, 6, 0, 1, 3)
        self.setLayout(gridLayout)

    def set_error_msg(self, message):
        self.status_label.setStyleSheet(
            "QLabel { color : Red; }")
        self.status_label.setText(message)

    def setMessage(self, message):
        self.status_label.setStyleSheet(
            "QLabel { color : black; }")
        self.status_label.setText(message)

    def set_success_msg(self, message):
        self.status_label.setStyleSheet(
            "QLabel { color : Green; }")
        self.status_label.setText(message)

    # region Click Events
    def show_settings(self):
        print "Setting clicked"
        SettingsDialogModule.SettingsDialog(self).show()
        pass
    # endregion

    def attach_events(self):
        # Attach the events
        self.settings_btn.clicked.connect(self.show_settings)
        self.issue_btn.clicked.connect(self.issue_btn_click)
        pass

    # endregion

    # region Utility Functions
    def resource_path(self, relative_path):
        # Get absolute path to resource, works for dev and for PyInstaller
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    # endregion

    def run(self, qt_app):
        # Show the Form
        self.show()
        # Run the Qt application
        qt_app.exec_()

    def reset_from(self):
        settings = self.read_settings(show_error=False)
        if settings is not None:
            self.timerInMilliSecond = settings['time_in_minutes'] * 60000

            self.redmineClient = RedMineClient(settings['server_url'],
                                               settings['api_key'])
            self.getActivities()
            self.issue = None
            self.issue_btn.setText("Find")
            self.issueIdBox.setEnabled(True)
            # self.issue_id.set("")
            # self.issue_subject.set("")

    # class ClearLabel(QtCore.QObject):
        # clearMsg = QtCore.Signal()

    def issue_btn_click(self):
        try:
            is_valid = self.validate_issue_id(self.issueIdBox.text())
            if not is_valid:
                return
            self.issueId = int(self.issueIdBox.text())
            self.getIssueThread = GetIssueThread(
                redmineClient=self.redmineClient, issueId=self.issueId)
            self.getIssueThread.issueFound.connect(
                self.postIssueFound)
            if not self.getIssueThread.isRunning():
                self.getIssueThread.start()
        except Exception, e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)

    def validate_issue_id(self, issue_id):
        is_issue_id_valid = issue_id.isdigit()
        if not is_issue_id_valid:
            self.set_error_msg("Issue ID has to be integer")
        return is_issue_id_valid

    def postIssueFound(self, issue):
        try:
            if(type(issue) is bool):
                self.set_error_msg("Issue not found")
                # self.getIssueThread.
            else:
                self.setMessage("")
                self.issue = issue
                self.issue_subject_label.setText(issue["subject"])
                self.issue_btn.setText("Edit")
                self.issueIdBox.setEnabled(False)

        except Exception, e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)

    def setScreenShotLabel(self, screenShotPixMap):
        self.screenShotLabel.setPixmap(screenShotPixMap.scaled(
            self.screenShotLabel.size(), QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation))

    def getActivities(self):
        # self.activity_thread.__init__(
            # target=self.postActivitiesRecd, args=())
        self.setMessage("Loading Activities ...... ")
        self.getActivityThread = GetActivitiesThread(
            redmineClient=self.redmineClient)
        self.getActivityThread.activitiesRecd.connect(
            self.postActivitiesRecd)
        if not self.getActivityThread.isRunning():
            self.getActivityThread.start()

    def postActivitiesRecd(self, actvities):
        self.activities = actvities
        defaultActivity = list(
            filter(
                lambda x: 'is_default' in x, self.activities))[0]["name"]
        dictActivities = {k["id"]: k['name'].encode(
            'ascii', 'ignre') for k in self.activities}
        self.activity_combobox.addItems(dictActivities.values())
        self.activity_combobox.setCurrentIndex(
            dictActivities.values().index(defaultActivity))
        self.setMessage("")

    def postEntry(self):
        pass
