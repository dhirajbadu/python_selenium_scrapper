import time
from selenium import webdriver

def getChromeDriver():
    driver = webdriver.Chrome('/home/dhiraj/project/python/tracker/src/resorces/chromedriver_80/chromedriver')
    return driver

def getFirefoxDriver():
    driver = webdriver.Firefox(executable_path=r'/home/dhiraj/project/python/tracker/src/resorces/geckodriver')
    return driver