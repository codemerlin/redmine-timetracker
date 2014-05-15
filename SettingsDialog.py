import tkSimpleDialog
import Tkinter


class SettingsDialog(tkSimpleDialog.Dialog):
    def __init__(self, parent, title=None):
        self.const_pad_y = parent.const_pad_y
        self.const_pad_x = parent.const_pad_x
        self.const_sticky = parent.const_sticky
        self.img = parent.img
        tkSimpleDialog.Dialog.__init__(self, parent, title=None)

    def body(self, master):
        Tkinter.Label(master, text="Server Url: ").grid(row=0,
                                                        sticky=self.const_sticky,
                                                        padx=self.const_pad_x,
                                                        pady=self.const_pad_y)
        Tkinter.Label(master, text="Api Key : ").grid(row=1,
                                                      sticky=self.const_sticky,
                                                      padx=self.const_pad_x,
                                                      pady=self.const_pad_y)
        Tkinter.Label(master, text="Time in Minutes : ").grid(row=2,
                                                              sticky=self.const_sticky,
                                                              padx=self.const_pad_x,
                                                              pady=self.const_pad_y)
        self.resizable(False, False)
        # img = Tkinter.PhotoImage(file=resource_path('redmine_fluid_icon.gif'))
        if self.img is not None:
            self.tk.call('wm', 'iconphoto', self._w, self.img)

        self.server_url_entry = Tkinter.Entry(master)
        self.api_key_entry = Tkinter.Entry(master)
        self.time_in_minutes_entry = Tkinter.Entry(master)

        self.server_url_entry.grid(row=0, column=1,
                                   sticky=self.const_sticky,
                                   padx=self.const_pad_x,
                                   pady=self.const_pad_y)
        self.api_key_entry.grid(row=1, column=1,
                                sticky=self.const_sticky,
                                padx=self.const_pad_x,
                                pady=self.const_pad_y)
        self.time_in_minutes_entry.grid(row=2, column=1,
                                        sticky=self.const_sticky,
                                        padx=self.const_pad_x,
                                        pady=self.const_pad_y)
        return self.server_url_entry  # initial focus

    def apply(self):
        first = int(self.server_url_entry.get())
        second = int(self.api_key_entry.get())
        print first, second  # or something