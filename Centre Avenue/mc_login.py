"""
This module is intended to create a dialogue box that will
allow for entry and capture of a username and password for MatrixCare.

Postcondition: User enters their username and password, which
is captured by the program and placed into self-documenting
variables.

Subgoal 1: A dialogue box appears on-screen which prompts the
user for their username and password.

Subgoal 2: The username and password are saved to variables and
these variables are passed back to the calling function.
"""

import tkinter
from tkinter import *
import time
from mc_main import *

class Login_Portal(tkinter.Frame):
    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        print("Login Initialized!")
        print("Please wait...")

        global username
        global password

        username = ""
        password = ""
        
        username_label = Label(parent, text="MatrixCare Username")
        password_label = Label(parent, text="MatrixCare Password")
        username_entry = Entry(parent, width=25)
        password_entry = Entry(parent, show="*", width=25)

        username_label.config(font=("Arial", 12))
        password_label.config(font=("Arial", 12))
        username_entry.config(font=("Arial", 12))
        password_entry.config(font=("Arial", 12))
        
        username_label.pack()
        username_entry.pack()
        password_label.pack()
        password_entry.pack()

        username_entry.focus_set()

        def store_username_password():
            username = username_entry.get()
            password = password_entry.get()
            parent.destroy()
            continue_test = ContinueWebscrape(username, password)
            

        submit_button = Button(parent, text="Submit", width=10, command=store_username_password)
        submit_button.config(font=("Arial", 12))
        submit_button.pack()

        def center(toplevel):
            toplevel.update_idletasks()
            w = toplevel.winfo_screenwidth()
            h = toplevel.winfo_screenheight()
            size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
            x = w/2 - size[0]/2
            y = h/2 - size[1]/2
            toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

        parent.geometry('{}x{}'.format(200, 125))
        
        center(parent)
        
if __name__ == "__main__":
    root = tkinter.Tk()
    Login_Portal(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

