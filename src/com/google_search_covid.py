import argparse
import sys

from selenium import webdriver
import time


import json


parser = argparse.ArgumentParser(description='App Store')
parser.add_argument('-q', dest='query', help='provide query')
args = parser.parse_args()

query = args.query

path = '/home/dhiraj/client/'

browser = webdriver.Chrome('/home/dhiraj/project/python/tracker/src/resorces/chromedriver_80/chromedriver')

def prepareQuery(v , delemieter):
    str = v.split()
    new_string = delemieter.join(str)
    #print(new_string)
    return new_string

def scrapPage():
    rawData = []
    newsEleList = browser.find_elements_by_xpath("//div[@id='rso']/div")
    counter = 0
    for newEle in newsEleList:
        tempData = []
        tempData.append(newEle.find_elements_by_xpath("//div/div/h3/a")[counter].text)
        tempData.append(newEle.find_elements_by_xpath("//div/div/h3/a")[counter].get_attribute('href'))
        tempData.append(newEle.find_elements_by_xpath("//div/div[@class='st']")[counter].text)
        rawData.append(tempData)
        counter = counter + 1

    return rawData



def main():
    finalData = []
    tempQuery = str(prepareQuery(query , "+"))
    browser.get('https://www.google.com/search?q='+tempQuery+'&amp;rlz=1C1CHBF_enUS880US880&amp;source=lnms&amp;tbm=nws&amp;sa=X&amp;ved=2ahUKEwiaweHXyufoAhVNzjgGHb00C28Q_AUoBHoECAsQBg')

    # language
    browser.find_elements_by_xpath("//div[@id='Rzn5id']/div/a")[1].click()
    # news
    browser.find_elements_by_xpath("//div[@id='hdtb-msb-vis']/div/a[contains(text(),'News')]")[0].click()

    finalData.append(scrapPage())
    nextElm = browser.find_elements_by_xpath("//a[@id='pnnext']")
    print(len(nextElm))
    loopCounter = 10
    while(len(nextElm) == 1 and loopCounter > 0):
        nextElm[0].click()
        finalData.append(scrapPage())
        nextElm = browser.find_elements_by_xpath("//a[@id='pnnext']")
        loopCounter = loopCounter - 1
        #pass

    writeFile(finalData)


def writeFile(dataList):
    #print (dataList)
    fileName = path + str(prepareQuery(query , "_")) + "_" + str(time.time() * 1000) + ".csv"
    file = open(fileName, "a")
    file.write(json.dumps(dataList))
    file.close()

if __name__ == '__main__':
    try:
        if(query is None or query == ""):
            print("Please provide query, eg: -q COVIt")
            sys.exit(0)
        else:
            main()
            browser.quit()
    except:
        print("Something else went wrong")
        browser.quit()
        raise

# go to here and install selenium and Chrome https://pypi.org/project/selenium/
#pip install selenium
#https://www.upwork.com/ab/find-work/details/~017eaf8570491424b3