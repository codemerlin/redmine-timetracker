import os
import sys
import json
from PySide import QtCore, QtGui
import re
import RedMineClient as rm
import SettingsDialogModule as SettingsDialogModule
qt_app = QtGui.QApplication(sys.argv)


class HelpMeTrack(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        # Set Window properties and create controls
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
        comments_label = QtGui.QLabel("Activity :")
        self.comments_box = QtGui.QTextEdit("Comments :")
        self.configureLayout(activity_label, comments_label,
                             time_in_min_label)
        self.setFixedSize(410, 510)
        self.attach_events()
        # self.activity_thread = threading.Thread()
        settings = self.read_settings(show_error=False)
        if settings is None:
            QtGui.QMessageBox.Warning(self, "Settings Missing",
                                      "Please use \
                                      settings button to provide settings")
        else:
            self.reset_from()

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
        grid_layout = QtGui.QGridLayout()
        grid_layout.addWidget(self.status_label, 0, 0, 1, 3)
        grid_layout.addWidget(self.issueIdBox, 1, 0)
        grid_layout.addWidget(self.issue_btn, 1, 1)
        grid_layout.addWidget(self.settings_btn, 1, 2)
        grid_layout.addWidget(self.issue_subject_label, 2, 0, 1, 3)
        grid_layout.addWidget(activity_label, 3, 0)
        grid_layout.addWidget(self.activity_combobox, 3, 1, 1, 2)
        grid_layout.addWidget(time_in_min_label, 4, 0)
        grid_layout.addWidget(self.time_in_min_box, 4, 1, 1, 2)
        grid_layout.addWidget(comments_label, 5, 0, 1, 3)
        grid_layout.addWidget(self.comments_box, 6, 0, 1, 3)
        self.setLayout(grid_layout)

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

    def issue_btn_click(self):

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

    def run(self):
        # Show the Form
        self.show()
        # Run the Qt application
        qt_app.exec_()

    def reset_from(self):
        settings = self.read_settings(show_error=False)
        if settings is not None:
            self.timerInMilliSecond = settings['time_in_minutes'] * 60000

            self.redmineClient = rm.RedMineClient(settings['server_url'],
                                                  settings['api_key'])
            self.getActivities()
            self.issue = None
            self.issue_btn.setText("Find")
            self.issueIdBox.setEnabled(True)
            # self.issue_id.set("")
            # self.issue_subject.set("")

    # class ClearLabel(QtCore.QObject):
        # clearMsg = QtCore.Signal()

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


class GetIssueThread(QtCore.QThread):
    issueRecd = QtCore.Signal(list)

    def __init__(self, redmineClient, parent=None):
        super(GetIssueThread, self).__init__(parent)
        self.exiting = False
        self.redmineClient = redmineClient

    def run(self, issueId):
        issue = self.redmineClient.get_issue(issueId)
        # print(activities)
        self.issueRecd.emit(issue)


class GetActivitiesThread(QtCore.QThread):
    activitiesRecd = QtCore.Signal(list)

    def __init__(self, redmineClient, parent=None):
        super(GetActivitiesThread, self).__init__(parent)
        self.exiting = False
        self.redmineClient = redmineClient

    def run(self):
        activities = self.redmineClient.getActivities()
        # print(activities)
        self.activitiesRecd.emit(activities)

app = HelpMeTrack()
app.run()
