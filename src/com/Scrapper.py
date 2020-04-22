__author__ = "Dhiraj Badu"

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time

import driverSetUp as driverSetUp

browser = driverSetUp.getChromeDriver()
#subjectListSize = 0

subjectIndex = 0
subjectListSize = 0
def main():
    global subjectListSize
    browser.get('https://schedule.msu.edu/')
    subjectList = browser.find_elements_by_xpath("//select[@name='ctl00$MainContent$ddlTerm']/option")
    subjectListSize = len(subjectList)
    print ("subjectListSize")
    print (subjectListSize)

    indexPage()

def indexPage():
    time.sleep(2)
    global subjectIndex
    #browser.get('https://schedule.msu.edu/')
    subjectIndex = subjectIndex +1
    print (subjectIndex )
    if(subjectIndex <= subjectListSize):
        mainForm()



def mainForm():
    # Term dropdown select Spring 2020
    browser.find_element_by_xpath("//select[@name='ctl00$MainContent$ddlTerm']/option[text()='Spring 2020']").click()

    # subject dropdown select first
    my_select = Select(browser.find_element_by_name("ctl00$MainContent$ddlSubject"))
    my_select.select_by_index(subjectIndex)
    #find_element_by_xpath("//select[@name='ctl00$MainContent$ddlSubject']/option[text()='"+sujectText+"']").click()

    # click View all results on one page
    browser.find_element_by_name("ctl00$MainContent$chkAllonePg").click()

    # submit the form
    browser.find_element_by_name("ctl00$MainContent$btnSubmit").click()

    indexPage()

#browser.quit()

if __name__ == '__main__':
    try:
        main()
        browser.quit()
    except:
        print("Something else went wrong")
        browser.quit()
    #browser.quit()