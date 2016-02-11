import os
import sys
from time import strftime
import Tkinter as Tkinter
# import Tkinter as Ttk
import ttk as ttk
import ScrolledText
import RedMineClient as rm
import threading as threading
# from ttk import
import json
import tkMessageBox
import re

from TKInterSettingsDialog_module import TKInterSettingsDialog


__author__ = 'Mohit_Thakral'


class Application(ttk.Frame):

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
        if (settings['api_key'] == '' or settings['server_url'] == '' or settings['time_in_minutes'] == ''):
            if show_error:
                self.settings_file_error()
            return settings
        if not self.is_valid_url(settings['server_url']):
            if show_error:
                self.settings_file_error()
            return settings
        return settings

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.const_pad_y = 5
        self.const_pad_x = 10
        self.const_sticky = (Tkinter.W,)

        self.log_timer_duration = None
        self.redmine_client = None

        self.img = Tkinter.PhotoImage(
            file=self.resource_path('redmine_fluid_icon.gif'))
        master.tk.call('wm', 'iconphoto', master._w, self.img)
        self.activity_thread = threading.Thread()
        self.activities = None
        self.time_in_minutes = Tkinter.StringVar()
        self.issue_subject = Tkinter.StringVar()
        self.issue_subject.set("")
        self.issue_id = Tkinter.StringVar()
        self.issue_id.set("")
        self.issue = None
        self.select_activity = Tkinter.StringVar()
        master.title("Redmine Time Tracker")
        self.main_frame = ttk.Frame(master)
        self.main_frame.grid(column=0, row=0, sticky=(
            Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S), padx=0, pady=5)
        self.cmb_activity = ttk.Combobox(
            self.main_frame, textvariable=self.select_activity)
        self.box_comments = ScrolledText.ScrolledText(
            self.main_frame, width=47, height=8)
        self.btn_find_issue = ttk.Button(
            self.main_frame, text="Find", command=self.find_issue_click)
        self.entry_issue = ttk.Entry(
            self.main_frame, textvariable=self.issue_id)
        self.label_status = ttk.Label(self.main_frame)

        self.create_ui()
        settings = self.read_settings(show_error=False)
        if settings is None:
            tkMessageBox.showwarning("Settings Missing", "Please use settings \
                button to provide settings")
        else:
            self.reset_from()

    def resource_path(self, relative_path):
        # Get absolute path to resource, works for dev and for PyInstaller
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

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

    def settings_file_error(self):
        tkMessageBox.showerror("Error", "Error Reading Settings File, \
         Make sure it exists with correct Values")

    def create_ui(self):
        # standard_font = label_status['font']
        # new_font = tkFont.Font(font=standard_font)
        # new_font['weight'] = tkFont.BOLD
        # label_status['font'] = new_font
        self.label_status.grid(column=0, row=0, columnspan=3,
                               sticky=self.const_sticky, padx=self.const_pad_x,
                               pady=self.const_pad_y)
        self.entry_issue.grid(column=0, row=1, columnspan=1, sticky=self.const_sticky,
                              padx=self.const_pad_x, pady=self.const_pad_y)
        self.btn_find_issue.grid(column=1, row=1, columnspan=1, sticky=self.const_sticky, padx=self.const_pad_x,
                                 pady=self.const_pad_y)

        ttk.Button(self.main_frame, text="Settings", command=self.settings_btn_click).grid(column=2, row=1,
                                                                                           columnspan=1,
                                                                                           sticky=self.const_sticky,
                                                                                           padx=self.const_pad_x,
                                                                                           pady=self.const_pad_y)
        ttk.Label(self.main_frame, textvariable=self.issue_subject, wraplength=370).grid(column=0, row=2, columnspan=3,
                                                                                         sticky=self.const_sticky,
                                                                                         padx=self.const_pad_x,
                                                                                         pady=self.const_pad_y)
        ttk.Label(self.main_frame, text="Activity :").grid(column=0, row=3, columnspan=1, sticky=self.const_sticky,
                                                           padx=self.const_pad_x,
                                                           pady=self.const_pad_y)
        self.cmb_activity.grid(column=1, row=3, columnspan=2, sticky=self.const_sticky, padx=self.const_pad_x,
                               pady=self.const_pad_y)
        self.cmb_activity.state(statespec=('readonly',))

        ttk.Label(self.main_frame,
                  text="Time In Minutes :").grid(column=0, row=4, columnspan=1,
                                                                  sticky=self.const_sticky,
                                                                  padx=self.const_pad_x, pady=self.const_pad_y)
        entry_time = ttk.Entry(
            self.main_frame, textvariable=self.time_in_minutes)
        entry_time.grid(column=1, row=4, columnspan=2,
                        sticky=self.const_sticky, padx=self.const_pad_x,
                        pady=self.const_pad_y)
        ttk.Label(self.main_frame, text="Comments :").grid(column=0, row=5, columnspan=3, sticky=self.const_sticky,
                                                           padx=self.const_pad_x,
                                                           pady=self.const_pad_y)
        self.box_comments.grid(column=0, row=6, columnspan=3, sticky=self.const_sticky, padx=self.const_pad_x,
                               pady=self.const_pad_y)
        save_button = ttk.Button(
            self.main_frame, text="Save", command=self.save_time_entry_click)
        save_button.grid(column=2, row=7,
                         sticky=self.const_sticky,
                         padx=self.const_pad_x,
                         pady=self.const_pad_y)
        tab_order = (
            self.entry_issue, self.btn_find_issue, self.cmb_activity, entry_time, self.box_comments, save_button, )

        for w in tab_order:
            w.lift()

    def settings_btn_click(self):
        TKInterSettingsDialog(self)
        self.reset_from()

    def save_time_entry_click(self):
        if not self.validate_form():
            return
        self.save_time_entry_server(self.time_in_minutes.get())

    def save_time_entry_server(self, time_in_minute):
        selected_activity = self.cmb_activity.get()
        selected_activity_id = list(
            filter(lambda x: x["name"] == selected_activity, self.activities))[0]["id"]
        user_comments = self.box_comments.get('1.0', Tkinter.END)
        self.time_entry = rm.TimeEntry(activity_id=selected_activity_id, issue_id=int(self.issue_id.get()),
                                       comments=user_comments, time_in_minutes=time_in_minute.__str__())

        self.after(2, self.process_time_entry)

    def process_time_entry(self):
        status = self.redmine_client.post_time_entry(self.time_entry)
        if status:
            self.set_success_msg(
                "Time Entry Saved Successfully " + strftime("%Y-%m-%d %H:%M:%S"))

    def find_issue_click(self):
        is_valid = self.validate_issue_id()
        if not is_valid:
            return
        if self.issue is None:
            self.after(2, self.req_find_issue)
        else:
            self.issue = None
            self.btn_find_issue['text'] = "Find"
            self.entry_issue.state(statespec=('!disabled',))
            self.issue_id.set("")
            self.issue_subject.set("")

    def set_error_msg(self, message):
        self.label_status['foreground'] = 'RED'
        self.label_status['text'] = message

    def set_msg(self, message):
        self.label_status['foreground'] = 'BLACK'
        self.label_status['text'] = message
        pass

    def set_success_msg(self, message):
        self.label_status['foreground'] = 'GREEN'
        self.label_status['text'] = message
        pass

    def validate_issue_id(self):
        is_issue_id_valid = self.issue_id.get().isdigit()
        if not is_issue_id_valid:
            self.set_error_msg("Issue ID has to be integer")
        return is_issue_id_valid

    def validate_form(self):
        if self.issue is None:
            self.set_error_msg("Please find an issue first")
            return False
        if not self.time_in_minutes.get().isdigit():
            self.set_error_msg("Provide time in minutes")
            return False
        return True

    def req_find_issue(self):
        if self.redmine_client is not None:
            self.issue = self.redmine_client.get_issue(
                int(self.issue_id.get()))
            self.issue_subject.set(self.issue["subject"])
            self.entry_issue.state(statespec=('disabled',))
            self.btn_find_issue['text'] = "Edit"
            self.after(self.log_timer_duration, self.start_logging)
        else:
            tkMessageBox.showerror(
                "Settings Missing", "Please provide settings, using settings button")

    def start_logging(self):
        self.save_time_entry_server(self.log_timer_duration / 60000)
        self.after(self.log_timer_duration, self.start_logging)

    def get_activities(self):
        self.activity_thread.__init__(
            target=self.req_get_activity_process, args=())
        self.set_msg("Loading Activities .. ")
        self.activity_thread.start()
        self.after(5, self.req_get_activity_end)

    def req_get_activity_process(self):
        self.activities = self.redmine_client.getActivities()

    def req_get_activity_end(self):
        if self.activity_thread.is_alive():
            self.after(5, self.req_get_activity_end)
            return
        else:
            default_item = list(
                filter(lambda x: 'is_default' in x, self.activities))[0]["name"]
            self.cmb_activity['values'] = list(
                map(lambda x: x["name"].encode('ascii', 'ignore'), self.activities))
            self.cmb_activity.set(default_item)
            self.set_msg("")
            self.activity_thread.join()

    def reset_from(self):
        settings = self.read_settings(show_error=False)
        if settings is not None:
            self.log_timer_duration = settings['time_in_minutes'] * 60000

            self.redmine_client = rm.RedMineClient(settings['server_url'],
                                                   settings['api_key'])
            self.get_activities()
            self.issue = None
            self.btn_find_issue['text'] = "Find"
            self.entry_issue.state(statespec=('!disabled',))
            self.issue_id.set("")
            self.issue_subject.set("")


try:
    root = Tkinter.Tk()
    root.resizable(False, False)
    # root.wm_iconbitmap(resource_path('appicon.ico'))
    app = Application(master=root)
    root.mainloop()
except Exception, e:
    open("logfile.log", "a").write(e.__str__())
