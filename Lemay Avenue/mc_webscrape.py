"""This program is designed to webscrape MatrixCare.com for
information related to Columbine Health Systems' facilities
and patient population. This informaton is intended to be
used by Columbine Health Systems' electronic therapy record
system when performing tasks such as creating therapy billing
records.

Postcondition: Reports are automatically pulled from MatrixCare
and imported to the therapy record system.

Subgoal 1: Provide a prompt for users to input username and
password that will then be used to log into MatrixCare.

Subgoal 2: Select the correct facility and access the
appropriate menu items to navigate to the screen on which
admission/discharge reports are produced.

Subgoal 3: Download the report to be used by the therapy
record system when creating a grid.
"""

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
import pyautogui
import time
import subprocess
import glob
import os
import sys
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from shutil import copyfile
import win32com.client
import win32clipboard
from tkinter import messagebox
import tkinter
from tkinter import *

global username
global password


def webscrape(username, password):

    parent = Tk()
    parent.withdraw()
    
    # This initializes the selenium gecko webdriver and prevents it from creating logs
    browser = webdriver.Firefox(log_path='')
    browser.get('https://columbine.achievematrix.com/')
    
    # Subgoal 1: Getting the information to login to MatrixCare
    
    emailElem = browser.find_element_by_id('j_username')
    emailElem.send_keys(username)
    
    passwordElem = browser.find_element_by_id('j_password')
    passwordElem.send_keys(password)
    
    linkElem = browser.find_element_by_class_name('loginbtn')
    
    linkElem.click() # Attempts to login to MatrixCare
    
    # Subgoal 2: Navigating to report on MatrixCare.

    try:
        facility_elem = browser.find_element_by_name('facility_name')
    except:
        facility_elem = False
    
    if facility_elem:
        pass
    else:
        
        messagebox.showinfo('Error', 'There was a problem with the ' \
                            'MatrixCare login information that was ' \
                            'entered. Please restart the program.')
        sys.exit() 
    
    facility_elem.send_keys('Lemay')

    search_elem = browser.find_element_by_name('search')
    search_elem.click() # Executes the search

    facility_elem = browser.find_element_by_link_text('LEMAY AVENUE HEALTH & REHAB - Fort Collins, CO')
    facility_elem.click()

    reports_elem = browser.find_element_by_xpath('/html/body/nav[1]')

    action = ActionChains(browser)
    action.move_to_element(reports_elem)
    action.move_by_offset(-90, 0)
    action.click().perform()

    time.sleep(.5)

    reports_elem = browser.find_element_by_link_text('Census Reports')
    reports_elem.click()

    reports_elem = browser.find_element_by_id('ReportRadio202')
    reports_elem.click()

    reports_elem = browser.find_element_by_name('Submit')
    reports_elem.click()

    reports_elem = browser.find_element_by_name('REPORTOUTPUTTYPE')
    reports_elem.click()

    for option in reports_elem.find_elements_by_tag_name('option'):
        if option.text == "MS EXCEL":
            option.click()
            pyautogui.press('enter')

    reports_elem = browser.find_element_by_name('StartDateOpenPeriod')
    reports_elem_value = reports_elem.get_attribute("value")

    reports_elem_value = datetime.strptime(reports_elem_value, '%m/%d/%Y')

    reports_elem_value = reports_elem_value - relativedelta(months=3)

    reports_elem_value = reports_elem_value.strftime('%m/%d/%Y')

    reports_elem.clear()

    reports_elem.send_keys(reports_elem_value)

    reports_elem = browser.find_element_by_name('EndDateOpenPeriod')
    reports_elem_value = reports_elem.get_attribute("value")

    reports_elem_value = datetime.strptime(reports_elem_value, '%m/%d/%Y')

    now_month = datetime.now().month
    now_day = datetime.now().day
    now_year= datetime.now().year

    reports_elem_value = reports_elem_value.replace(month=now_month, day=now_day, year=now_year)
        
    reports_elem_value = reports_elem_value.strftime('%m/%d/%Y')
     
    reports_elem.clear()

    reports_elem.send_keys(reports_elem_value)

    reports_elem = browser.find_element_by_name('Submit')
    reports_elem.click()

    time.sleep(10)

    #pyautogui.press('down')
    
    # Subgoal 3: Downloading report and importing into therapy record system
    # Data is pulled from the cliboard, which was sent by the Excel
    # VBA in order to find the therapy record file
    
    pyautogui.press('enter')

    time.sleep(5)

    browser.quit()

    xl=win32com.client.Dispatch('Excel.Application')
    xl.Workbooks.Open(Filename="G:/Therapy Record Interfaces/Lemay Avenue/Lemay Avenue Therapy Record Interface.xlsm")
    xl.Run('Import_Worksheet')


