from Tkinter import *
import Tkinter as Ttk


def calculate(*args):
    try:
        value = float(feet.get())
        meters.set((0.3048 * value * 10000.0 + 0.5) / 10000.0)
    except ValueError:
        pass


root = Tk()

root.title("Feet to Meters")

mainframe = Ttk.Frame(root, padx=3, pady=5)

mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

feet = StringVar()
meters = StringVar()

feet_entry = Ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

Ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
Ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

Ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
Ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
Ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind('<Return>', calculate)

root.mainloop()
