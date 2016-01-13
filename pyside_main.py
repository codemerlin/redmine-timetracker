import os
import sys

from PySide import QtCore
from PySide.QtCore import SIGNAL

from PySide.QtGui import *


qt_app = QApplication(sys.argv)


class HelpMeTrack(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # Set Window properties and create controls
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowTitle("Redmine Time Tracker")
        self.setWindowIcon(QIcon(self.resource_path('redmine_fluid_icon.gif')))
        self.status_label = QLabel()
        self.issue_id_box = QLineEdit()
        self.issue_btn = QPushButton("Find")
        self.settings_btn = QPushButton("Settings")
        self.settings_btn
        self.issue_subject_label = QLabel()
        activity_label = QLabel("Activity :")
        self.activity_combobox = QComboBox()
        time_in_min_label = QLabel("Time in Min :")
        self.time_in_min_box = QLineEdit()
        comments_label = QLabel("Comment :")
        self.comments_box = QTextEdit()

        self.configure_layout(activity_label, comments_label, time_in_min_label)
        self.attach_events()


    #region UI Functions
    def configure_layout(self, activity_label, comments_label, time_in_min_label):
        # Prepare and configure GridLayout
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.status_label, 0, 0, 1, 3)
        grid_layout.addWidget(self.issue_id_box, 1, 0)
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

    def attach_events(self):
        # Attach the events
        self.connect(self.issue_btn, SIGNAL("clicked()"), self.issue_btn_click)
        pass

    #endregion

    #region Click Events
    def issue_btn_click(self):
        pass
    #endregion


    #region Utility Functions
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    #endregion

    def run(self):
        # Show the Form
        self.show()
        # Run the Qt application
        qt_app.exec_()


app = HelpMeTrack()
app.run()
