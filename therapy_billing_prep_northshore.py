
"""This program is designed to webscrape MatrixCare.com for
information related to Columbine Health Systems' facilities
and patient population. This informaton is intended to be
used by Columbine Health Systems' electronic therapy record
system when performing tasks such as creating therapy billing
records.

Postcondition: Reports are automatically pulled from MatrixCare
to be used by the therapy record system and billing interfaces.

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
import pyautogui
import time
import subprocess
import glob
import os
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from shutil import copyfile
import win32com.client

browser = webdriver.Firefox()
browser.get('https://columbine.achievematrix.com/')


# Subgoal 1: Getting the information to login to MatrixCare
emailElem = browser.find_element_by_id('j_username')
emailElem.send_keys('john.blaine')

passwordElem = browser.find_element_by_id('j_password')
passwordElem.send_keys('Fallen1989!')

linkElem = browser.find_element_by_class_name('loginbtn')

linkElem.click() # Attempts to login to MatrixCare

# Subgoal 2: Navigating and to report on MatrixCare.

facility_elem = browser.find_element_by_name('facility_name')
facility_elem.send_keys('North Shore')

search_elem = browser.find_element_by_name('search')
search_elem.click() # Executes the search

facility_elem = browser.find_element_by_link_text('NORTH SHORE HEALTH & REHAB - Loveland, CO')
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

reports_elem_value = reports_elem_value

reports_elem_value = reports_elem_value.strftime('%m/%d/%Y')

reports_elem.clear()

reports_elem.send_keys(reports_elem_value)

reports_elem = browser.find_element_by_name('Submit')
reports_elem.click()

time.sleep(10)

#pyautogui.press('down')

# Subgoal 3: Downloading report and importing into therapy record system

pyautogui.press('enter')

time.sleep(5)

browser.quit()

#path = os.path.normpath('G:/Z_John B/Python Programs/test_folder/Centre Avenue Therapy Record Interface (BETA).xlsm')

#os.startfile(path)

xl=win32com.client.Dispatch('Excel.Application')
xl.Workbooks.Open(Filename="G:/Therapy Record Interfaces/North Shore/North Shore Therapy Record Interface.xlsm")
xl.Run('Import_Worksheet')

