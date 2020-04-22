import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import datetime

import mysql.connector
from mysql.connector import errorcode

import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


parser = argparse.ArgumentParser(description='App Store')
parser.add_argument('-q', dest='query', help='provide query')
args = parser.parse_args()

query = args.query

path = '/home/dhiraj/client/'

browser = webdriver.Chrome('/home/dhiraj/project/python/tracker/src/resorces/chromedriver_80/chromedriver')

#127.0.0.1
config = {
    'user': 'dhiraj',
    'password': 'dhiraj',
    'host': '127.0.0.1',
    'database': 'scrapping',
    'raise_on_warnings': True
}

#create database scrapping;

def getMysqlConnection():
    try:
        conn = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        sys.exit(0)
    else:
     return conn

def createTable():
    tableQuery = "create table if not exists google_play_store_search ( "
    tableQuery += "id bigint auto_increment primary key,"
    tableQuery += "created_date DATETIME,"
    tableQuery += "keyword varchar(500),"
    tableQuery += "resultJson varchar(255) "
    tableQuery += ");"

    print(tableQuery)
    conn = getMysqlConnection()
    dbcursor = conn.cursor()
    dbcursor.execute(tableQuery)
    conn.commit()
    conn.close()
    print(dbcursor.rowcount, "record(s) affected")


def main():
    rawData = []
    browser.get('https://play.google.com/store/movies?hl=en')
    elem = browser.find_element_by_name('q')  # Find the search box
    elem.clear()
    elem.send_keys(query + Keys.RETURN)
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='qZxJ9']/div")))
    elemResultList = browser.find_elements_by_xpath("//div[@class='qZxJ9']/div")
    print (len(elemResultList))
    for elemResult in elemResultList:

        #print (str(elemResult.text))
        rawData.append(str(elemResult.text))

    insertReultIntoDb(rawData)

def writeFile(dataList):
    print (dataList)
    fileName = path + query + "_" + str(time.time() * 1000) + ".csv"
    file = open(fileName, "a")
    for data in dataList:
        file.write(data)
        file.write("\n")
    file.close()

def insertReultIntoDb(dataList):

    #createTable()
    insertQuery = "INSERT INTO google_play_store_search (created_date , keyword , resultJson)"
    insertQuery += "VALUES(%s, %s, %s)"
    current_time = datetime.datetime.now()
    resultJson = json.dumps(dataList)
    #print(current_time)
    #print(resultJson)
    conn = getMysqlConnection()
    dbcursor = conn.cursor()
    dbcursor.execute(insertQuery , (current_time , query,resultJson ))
    conn.commit()
    conn.close()
    print(dbcursor.rowcount, "record(s) affected")

if __name__ == '__main__':
    try:
        main()
        browser.quit()
    except:
        print("Something else went wrong")
        browser.quit()
        raise

# go to here and install selenium and Chrome https://pypi.org/project/selenium/
#pip install selenium

#pip install mysql-connector-python
#pip install --user mysql-connector-python