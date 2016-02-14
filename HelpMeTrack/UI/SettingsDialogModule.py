import string
import json
from PySide import QtCore, QtGui


class SettingsDialog(QtGui.QDialog):
    def __init__(self, parent):
        super(SettingsDialog, self).__init__(parent)
        self.is_valid_url = parent.is_valid_url
        self.settings = parent.read_settings(show_error=False)
        self.resetParent = parent.reset_form
        # self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setFixedSize(400, 110)
        self.createControls()

    def createControls(self):
        self.status_label = QtGui.QLabel()
        self.serverUrlBox = QtGui.QLineEdit()
        self.apiKeyBox = QtGui.QLineEdit()
        self.timeInMinBox = QtGui.QLineEdit()
        self.readSettings()
        self.configureLayout()

        # region UI Functions

    def configureLayout(self):
        # Prepare and configure GridLayout
        grid_layout = QtGui.QGridLayout()
        grid_layout.addWidget(self.status_label, 0, 0, 1, 2)
        grid_layout.addWidget(QtGui.QLabel("Server Url : "), 1, 0)
        grid_layout.addWidget(self.serverUrlBox, 1, 1, 1, 2)
        grid_layout.addWidget(QtGui.QLabel("Api Key : "), 2, 0, 1, 2)
        grid_layout.addWidget(self.apiKeyBox, 2, 1, 1, 2)
        # grid_layout.addWidget(QtGui.QLabel("Time in Min : "), 3, 0)
        # grid_layout.addWidget(self.timeInMinBox, 3, 1)
        save_button = QtGui.QPushButton("Save")
        save_button.clicked.connect(self.saveClicked)
        grid_layout.addWidget(save_button, 3, 1)
        cancel_button = QtGui.QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancelClicked)
        grid_layout.addWidget(cancel_button, 3, 2)
        self.setLayout(grid_layout)

    def saveClicked(self):
        if not self.validate():
            return
        settings = {'server_url': self.serverUrlBox.text().strip(), 'api_key': self.apiKeyBox.text().strip()}
        with open('settings.json', 'w') as outfile:
            json.dump(settings, outfile)
        self.resetParent()
        self.close()

    def cancelClicked(self):
        self.close()
        pass

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

    def validate(self):
        if not self.is_valid_url(self.serverUrlBox.text()):
            self.set_error_msg("Please provide a valid Url")
            self.serverUrlBox.focus()
            return False
        if not self.apiKeyBox.text().strip():
            self.set_error_msg("Please provide a value of api key")
            self.apiKeyBox.focus()
            return False
        if not all(c in string.hexdigits for c in self.apiKeyBox.text().strip()):
            self.set_error_msg("Please  make sure api key, is a correct hexadecimal value")
            self.apiKeyBox.focus()
            return False
        return True

    def readSettings(self):
        if (self.settings):
            # print(self.settings['server_url'])
            self.serverUrlBox.setText(self.settings['server_url'])
            self.apiKeyBox.setText(self.settings['api_key'])
