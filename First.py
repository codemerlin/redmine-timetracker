__author__ = 'Mohit_Thakral'

import Tkinter as Tk
# import Tkinter as Ttk
import ttk as ttk
# from ttk import


class Application(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.issue_subject = Tk.StringVar()
        self.issue_subject.set("Test Subject")
        self.issue_id = Tk.StringVar()
        self.issue_id.set("1")
        self.status_msg = Tk.StringVar()
        self.status_msg.set("Empty status Message")
        master.title("Feet To Meters")
        self.main_frame = ttk.Frame(master)
        self.main_frame.grid(column=0, row=0, sticky=(Tk.N, Tk.W, Tk.E, Tk.S))
        self.create_ui()

    def create_ui(self):
        ttk.Label(self.main_frame, textvariable=self.status_msg).grid(column=0, row=0)
        ttk.Entry(self.main_frame, textvariable=self.issue_id).grid(column=0, row=1)
        ttk.Button(self.main_frame, text="Find").grid(column=1, row=1)
        ttk.Button(self.main_frame, text="Settings").grid(column=2, row=1)
        ttk.Label(self.main_frame, textvariable=self.issue_subject).grid(column=0, row=2)
        ttk.Label(self.main_frame, text="Activity :").grid(column=0, row=3)
        var = Tk.StringVar()
        var.set("a")
        ttk.Combobox(self.main_frame).grid(column=1, row=3, columnspan=2)

# self.status_msg = "Empty Status Message"


root = Tk.Tk()

app = Application(master=root)

# root.title("Feet to Meters")

# mainframe = Ttk.Frame(root, padx=3, pady=5)

root.mainloop()
# root.destroy()