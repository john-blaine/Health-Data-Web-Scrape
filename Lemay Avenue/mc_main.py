"""
This module is intended to be the main loop for a program will
run when a therapy record is being created in the Columbine
Health Systems electornic therapy system. The program will pull
data from MatrixCare.com that will auto-populate into the
relevant patient record fields once the user has selected the
patient from a generated list.

Postcondition: User enters their username and password, and the
program pulls the relevant report from MatrixCare.com and
auto-populates the data for the given patient.

Subgoal 1: User enters their MatrixCare username and password
to be used when the program pulls data from MatrixCare.

Subgoal 2: Using username's username/password, program webscrapes
MatrixCare.com for patient information to be loaded into patient
record during the creation phase.

"""

import tkinter
from tkinter import *
from mc_login import *
from mc_webscrape import *
import sys

class MainApplication():
    def __init__(self, parent, *args, **kwargs):

        global username
        global password
        
        username = ""
        password = ""
        
        # Subgoal 1: Entering user's MatrixCare login information
        login_portal = Login_Portal(parent)

class ContinueWebscrape:
    def __init__(self, username, password):
        
        time.sleep(10)

        # Subgoal 2: Webscraping patient information
        webscrape(username, password)

    
            
if __name__ == "__main__":
    root = tkinter.Tk()
    MainApplication(root)
    root.mainloop()
