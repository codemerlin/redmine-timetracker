import string
import json
import Tkinter
from PySide import QtCore, QtGui


class SettingsDialog(QtGui.QDialog):

    def __init__(self, parent):
        super(SettingsDialog, self).__init__(parent)
        self.is_valid_url = parent.is_valid_url
        self.settings = parent.read_settings(show_error=False)
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
        grid_layout.addWidget(self.serverUrlBox, 1, 1)
        grid_layout.addWidget(QtGui.QLabel("Api Key : "), 2, 0)
        grid_layout.addWidget(self.apiKeyBox, 2, 1)
        grid_layout.addWidget(QtGui.QLabel("Time in Min : "), 3, 0)
        grid_layout.addWidget(self.timeInMinBox, 3, 1)
        self.setLayout(grid_layout)

    def readSettings(self):
        if(self.settings):
            # print(self.settings['server_url'])
            self.serverUrlBox.setText(self.settings['server_url'])
            self.apiKeyBox.setText(self.settings['api_key'])
            self.timeInMinBox.setText(str(self.settings['time_in_minutes']))

    # def body(self, master):

    #     self.label_status = Tkinter.Label(master)
    #     self.label_status.grid(row=0, columnspan=2,
    #                            sticky=self.const_sticky,
    #                            padx=self.const_pad_x,
    #                            pady=self.const_pad_y)
    #     Tkinter.Label(master, text="Server Url: ").grid(row=1,
    #                                                     sticky=self.const_sticky,
    #                                                     padx=self.const_pad_x,
    #                                                     pady=self.const_pad_y)
    #     Tkinter.Label(master, text="Api Key : ").grid(row=2,
    #                                                   sticky=self.const_sticky,
    #                                                   padx=self.const_pad_x,
    #                                                   pady=self.const_pad_y)
    #     Tkinter.Label(master, text="Time in Minutes : ").grid(row=3,
    #                                                           sticky=self.const_sticky,
    #                                                           padx=self.const_pad_x,
    #                                                           pady=self.const_pad_y)
    #     self.resizable(False, False)
    #     # img = Tkinter.PhotoImage(file=resource_path('redmine_fluid_icon.gif'))
    #     if self.img is not None:
    #         self.tk.call('wm', 'iconphoto', self._w, self.img)

    #     self.server_url_entry = Tkinter.Entry(master, width=50)
    #     self.api_key_entry = Tkinter.Entry(master, width=50)
    #     self.time_in_minutes_entry = Tkinter.Entry(master, width=50)

    #     if self.settings is not None:
    #         self.server_url_entry.delete(0, END)
    #         self.server_url_entry.insert(0, self.settings['server_url'])

    #         self.api_key_entry.delete(0, END)
    #         self.api_key_entry.insert(0, self.settings['api_key'])

    #         self.time_in_minutes_entry.delete(0, END)
    #         self.time_in_minutes_entry.insert(0, self.settings['time_in_minutes'])

    #     self.server_url_entry.grid(row=1, column=1,
    #                                sticky=self.const_sticky,
    #                                padx=self.const_pad_x,
    #                                pady=self.const_pad_y)
    #     self.api_key_entry.grid(row=2, column=1,
    #                             sticky=self.const_sticky,
    #                             padx=self.const_pad_x,
    #                             pady=self.const_pad_y)
    #     self.time_in_minutes_entry.grid(row=3, column=1,
    #                                     sticky=self.const_sticky,
    #                                     padx=self.const_pad_x,
    #                                     pady=self.const_pad_y)
    #     return self.server_url_entry  # initial focus

    # def validate(self):
    #     if not self.is_valid_url(self.server_url_entry.get()):
    #         self.label_status['foreground'] = 'RED'
    #         self.label_status['text'] = "Please provide a valid Url"
    #         self.server_url_entry.focus()
    #         return False
    #     if not self.api_key_entry.get().strip():
    #         self.label_status['foreground'] = 'RED'
    #         self.label_status['text'] = "Please provide a value of api key"
    #         self.api_key_entry.focus()
    #         return False
    #     if not all(c in string.hexdigits for c in self.api_key_entry.get().strip()):
    #         self.label_status['foreground'] = 'RED'
    #         self.label_status['text'] = "Please  make sure api key, is a correct hexadecimal value"
    #         self.api_key_entry.focus()
    #         return False
    #     if not self.time_in_minutes_entry.get().isdigit():
    #         self.label_status['foreground'] = 'RED'
    #         self.label_status['text'] = "Please make sure that time in minutes is an integral value"
    #         self.time_in_minutes_entry.focus()
    #         return False

    #     return True

    # def apply(self):
    #     # first = int(self.server_url_entry.get())
    #     # second = int(self.api_key_entry.get())
    #     settings = {'server_url': self.server_url_entry.get().strip(), 'api_key': self.api_key_entry.get().strip(),
    #                 'time_in_minutes': int(self.time_in_minutes_entry.get().strip())}
    #     with open('settings.json', 'w') as outfile:
    #         json.dump(settings, outfile)
    #         # print first, second  # or something
