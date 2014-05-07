import os
import sys

__author__ = 'Mohit_Thakral'

import Tkinter as Tkinter
# import Tkinter as Ttk
import ttk as ttk
import ScrolledText
# from ttk import


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
        self.time_in_minutes = Tkinter.StringVar()
        self.issue_subject = Tkinter.StringVar()
        self.issue_subject.set("<<Test Subject>>")
        self.issue_id = Tkinter.StringVar()
        self.issue_id.set("1")
        self.status_msg = Tkinter.StringVar()
        self.status_msg.set("<<Test status Message>>")
        master.title("Redmine Time Tracker")
        self.main_frame = ttk.Frame(master)
        self.main_frame.grid(column=0, row=0, sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S), padx=0, pady=5)
        self.create_ui()

    def create_ui(self):
        constpadx = 10
        constpady = 5
        constSticky = (Tkinter.W,)
        ttk.Label(self.main_frame, textvariable=self.status_msg).grid(column=0, row=0, columnspan=3,
                                                                      sticky=constSticky, padx=constpadx,
                                                                      pady=constpady)
        ttk.Entry(self.main_frame, textvariable=self.issue_id).grid(column=0, row=1, columnspan=1, sticky=constSticky,
                                                                    padx=constpadx, pady=constpady)
        ttk.Button(self.main_frame, text="Find").grid(column=1, row=1, columnspan=1, sticky=constSticky, padx=constpadx,
                                                      pady=constpady)
        ttk.Button(self.main_frame, text="Settings").grid(column=2, row=1, columnspan=1, sticky=constSticky,
                                                          padx=constpadx,
                                                          pady=constpady)
        ttk.Label(self.main_frame, textvariable=self.issue_subject).grid(column=0, row=2, columnspan=3,
                                                                         sticky=constSticky, padx=constpadx,
                                                                         pady=constpady)
        ttk.Label(self.main_frame, text="Activity :").grid(column=0, row=3, columnspan=1, sticky=constSticky,
                                                           padx=constpadx,
                                                           pady=constpady)
        self.cmbActivity = ttk.Combobox(self.main_frame)
        self.cmbActivity.grid(column=1, row=3, columnspan=2, sticky=constSticky, padx=constpadx, pady=constpady)
        self.cmbActivity.state(statespec=('readonly',))

        ttk.Label(self.main_frame, text="Time In Minutes :").grid(column=0, row=4, columnspan=1, sticky=constSticky,
                                                                  padx=constpadx, pady=constpady)
        ttk.Entry(self.main_frame, textvariable=self.time_in_minutes).grid(column=1, row=4, columnspan=2,
                                                                           sticky=constSticky, padx=constpadx,
                                                                           pady=constpady)
        ttk.Label(self.main_frame, text="Comments :").grid(column=0, row=5, columnspan=3, sticky=constSticky,
                                                           padx=constpadx,
                                                           pady=constpady)
        ScrolledText.ScrolledText(self.main_frame, width=47, height=8).grid(column=0, row=6, columnspan=3,
                                                                                    sticky=constSticky,
                                                                                    padx=constpadx,
                                                                                    pady=constpady)
        # Tkinter.Text()

# self.status_msg = "Empty Status Message"


root = Tkinter.Tk()

root.resizable(False, False)

root.wm_iconbitmap(resource_path('appicon.ico'))

app = Application(master=root)


# root.title("Feet to Meters")

# mainframe = Ttk.Frame(root, padx=3, pady=5)

root.mainloop()
# root.destroy()