import os
import sys

__author__ = 'Mohit_Thakral'

import Tkinter as Tkinter
# import Tkinter as Ttk
import ttk as ttk
import ScrolledText
import RedMineClient as rm
import threading as threading
# from ttk import
import mbox

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Application(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
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
        self.main_frame.grid(column=0, row=0, sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S), padx=0, pady=5)
        self.cmb_activity = ttk.Combobox(self.main_frame, textvariable=self.select_activity)
        self.box_comments = ScrolledText.ScrolledText(self.main_frame, width=47, height=8)
        self.btn_find_issue = ttk.Button(self.main_frame, text="Find", command=self.find_issue_click)
        self.entry_issue = ttk.Entry(self.main_frame, textvariable=self.issue_id)
        self.redmine_client = rm.RedMineClient("https://support.targetintegration.com",
                                               "c3a7f2f4562ed90ff5bc9b6d9e0574f4d434d54e")
        self.label_status = ttk.Label(self.main_frame)

        self.create_ui()
        self.get_activities()

    def create_ui(self):
        constpadx = 10
        constpady = 5
        constSticky = (Tkinter.W,)
        self.box = mbox.tbox(self)
        # standard_font = label_status['font']
        # new_font = tkFont.Font(font=standard_font)
        # new_font['weight'] = tkFont.BOLD
        # label_status['font'] = new_font
        self.label_status.grid(column=0, row=0, columnspan=3,
                               sticky=constSticky, padx=constpadx,
                               pady=constpady)
        self.entry_issue.grid(column=0, row=1, columnspan=1, sticky=constSticky,
                              padx=constpadx, pady=constpady)
        self.btn_find_issue.grid(column=1, row=1, columnspan=1, sticky=constSticky, padx=constpadx, pady=constpady)

        ttk.Button(self.main_frame, text="Settings", command=lambda: self.box("Name ?")).grid(column=2, row=1, columnspan=1, sticky=constSticky,
                                                          padx=constpadx,
                                                          pady=constpady)
        ttk.Label(self.main_frame, textvariable=self.issue_subject, wraplength=370).grid(column=0, row=2, columnspan=3,
                                                                                         sticky=constSticky,
                                                                                         padx=constpadx,
                                                                                         pady=constpady)
        ttk.Label(self.main_frame, text="Activity :").grid(column=0, row=3, columnspan=1, sticky=constSticky,
                                                           padx=constpadx,
                                                           pady=constpady)
        self.cmb_activity.grid(column=1, row=3, columnspan=2, sticky=constSticky, padx=constpadx, pady=constpady)
        self.cmb_activity.state(statespec=('readonly',))

        ttk.Label(self.main_frame, text="Time In Minutes :").grid(column=0, row=4, columnspan=1, sticky=constSticky,
                                                                  padx=constpadx, pady=constpady)
        ttk.Entry(self.main_frame, textvariable=self.time_in_minutes).grid(column=1, row=4, columnspan=2,
                                                                           sticky=constSticky, padx=constpadx,
                                                                           pady=constpady)
        ttk.Label(self.main_frame, text="Comments :").grid(column=0, row=5, columnspan=3, sticky=constSticky,
                                                           padx=constpadx,
                                                           pady=constpady)
        self.box_comments.grid(column=0, row=6, columnspan=3, sticky=constSticky, padx=constpadx, pady=constpady)
        ttk.Button(self.main_frame, text="Save", command=self.save_time_entry_click).grid(column=2, row=7,
                                                                                          sticky=constSticky,
                                                                                          padx=constpadx,
                                                                                          pady=constpady)


    def save_time_entry_click(self):
        if not self.validate_form():
            return
        selected_activity = self.cmb_activity.get()
        selected_activity_id = list(filter(lambda x: x["name"] == selected_activity, self.activities))[0]["id"]
        user_comments = self.box_comments.get('1.0', Tkinter.END)
        self.time_entry = rm.TimeEntry(activity_id=selected_activity_id, issue_id=int(self.issue_id.get()),
                                       comments=user_comments, time_in_minutes=self.time_in_minutes.get())

        self.after(2, self.process_time_entry)

    def process_time_entry(self):
        status = self.redmine_client.post_time_entry(self.time_entry)
        if status:
            self.set_success_msg("Time Entry Saved SuccessFully")


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
        self.issue = self.redmine_client.get_issue(int(self.issue_id.get()))
        self.issue_subject.set(self.issue["subject"])
        self.entry_issue.state(statespec=('disabled',))
        self.btn_find_issue['text'] = "Edit"


    def get_activities(self):
        self.activity_thread.__init__(target=self.req_get_activity_process, args=())
        self.set_msg("Loading Activities .. ")
        self.activity_thread.start()
        self.after(5, self.req_get_activity_end)


    def req_get_activity_process(self):
        self.activities = self.redmine_client.get_activities()


    def req_get_activity_end(self):
        if self.activity_thread.is_alive():
            self.after(5, self.req_get_activity_end)
            return
        else:
            default_item = list(filter(lambda x: 'is_default' in x, self.activities))[0]["name"]
            self.cmb_activity['values'] = list(map(lambda x: x["name"].encode('ascii', 'ignore'), self.activities))
            self.cmb_activity.set(default_item)
            self.set_msg("")
            self.activity_thread.join()


try:
    root = Tkinter.Tk()
    root.resizable(False, False)
    root.wm_iconbitmap(resource_path('appicon.ico'))
    app = Application(master=root)
    root.mainloop()
except Exception, e:
    open("logfile.log", "a").write(e.__str__())