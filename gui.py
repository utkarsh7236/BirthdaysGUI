#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import font, messagebox
import engine
import re, os, sys


def main():
    birthdayList = engine.getBirthdays()
    window = ThemedTk(theme="equilux")
    window.title("Birthdays")
    w = window.winfo_reqwidth()
    h = window.winfo_reqheight()
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - 2 * (w / 2)
    y = (hs / 2) - 2.5 * (h / 2)
    window.geometry('+%d+%d' % (x, y))
    window.minsize(width=300, height=400)
    window.configure(bg='black')
    window.attributes('-notify', "true")
    listbox = tk.Listbox(window, width=32, background="Black", selectbackground="#86a6a3")

    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = ttk.Scrollbar(window)

    scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

    for item in birthdayList:
        listbox.insert(tk.END, "{:<25}  {:^10}  {:>10}".format(item[0], item[1], item[2]))

    listbox.config(yscrollcommand=scrollbar.set)
    listbox.config(font=font.Font(weight='bold'))
    listbox.configure(justify=tk.RIGHT)
    colors = ["red", "yellow", "lime", "grey"]

    for i in range(len(birthdayList)):
        listbox.itemconfig(i, foreground=colors[birthdayList[i][-1]])

    listbox.insert(0, "{:<25}  {:^10}  {:>10}".format("Name", "Days Left", "Age"))
    listbox.itemconfig(0, foreground="White")
    scrollbar.config(command=listbox.yview)

    def restart_program():
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def deleteBirthday():
        string = listbox.get(tk.ANCHOR)
        name = re.findall('([a-zA-Z ]*)\d*.*', string)[0]
        MsgBox = messagebox.askquestion('Confirm Delete Birthday', f"Are you sure you want to delete the birthday "
                                                                   f"information for {name.strip()}?",
                                        icon='warning')
        if MsgBox == 'yes':
            engine.deleteLine(name)
            listbox.delete(tk.ANCHOR)
        else:
            return None

    def calender(entryName):
        L2 = ttk.Label(window, text="Input Date Format: DDMMYYYY")
        L2.pack(side=tk.TOP)
        dateEntry = ttk.Entry(window)
        dateEntry.pack(side=tk.TOP, fill = tk.BOTH)

        def handleCalender():
            entryDate = dateEntry.get()

            with open(f'{os.getcwd()}/db.txt', "a", encoding='utf8') as f:
                f.write("\n" + entryName + ", " + entryDate)
                f.close()
            confirmDate.destroy()
            L2.destroy()
            dateEntry.destroy()

            restart_program()

        confirmDate = ttk.Button(window, text="Confirm Date", command=handleCalender)
        confirmDate.pack()

    def addBirthdayName():
        L1 = ttk.Label(window, text="Input Name")
        L1.pack(side=tk.TOP, fill=tk.BOTH)
        nameEntry = ttk.Entry(window)
        nameEntry.pack(side=tk.TOP, fill = tk.BOTH)
        addButton.destroy()

        def addBirthdayCalender():
            entryName = nameEntry.get()
            confirmButton.destroy()
            nameEntry.destroy()
            L1.destroy()
            calender(entryName)

        confirmButton = ttk.Button(window, text="Confirm Input", command=addBirthdayCalender)
        confirmButton.pack(fill=tk.BOTH)

    btn = ttk.Button(window, text="Remove Selected Birthday", command=deleteBirthday)
    btn.pack(fill=tk.BOTH)
    addButton = ttk.Button(window, text="Add Birthday", command=addBirthdayName)
    addButton.pack(side=tk.TOP, pady=3, fill=tk.BOTH)

    quit = ttk.Button(window, text="Quit", command=window.destroy)
    quit.pack(side=tk.BOTTOM, fill=tk.BOTH)
    window.mainloop()
