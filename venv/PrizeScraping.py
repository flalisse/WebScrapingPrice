
import unicodedata
import selenium as se
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime
import urllib.request

import re
import requests

import json
from DataBase import create_table, create_connection


def ScrapData ():
    options = se.webdriver.ChromeOptions()
    options.add_argument("headless")

    time.sleep(1)
    driver = se.webdriver.Chrome("/Users/francois/PycharmProjects/WebScrapingPrice/venv/lib/python3.7/site-packages/chromedriver",options=options)

    time.sleep(1)
    driver.get("https://www.google.com/shopping")

    input = driver.find_element_by_class_name("lst")
    time.sleep(1)

    brand = "samsung"
    input.send_keys(brand)

    GotoPagetoScrap = driver.find_element_by_name("btnG")
    GotoPagetoScrap.submit()


    page_to_scrap = driver.page_source

#must precise the headers agent to avoid error 403
#page = urllib.request.Request(page_to_scrap, headers={'User-Agent': 'Mozilla/5.0'})
#html = urllib.request.urlopen(page).read()


    soup = BeautifulSoup(page_to_scrap, 'html.parser')

#scrap all data span with class define in attrs
    result = soup.find_all("span",attrs= {'O8U6h'})

#occurence of scrap
    numberOfOccurence = len(result)
    numberOfOccurence = int(numberOfOccurence)
    i=0
    price_contains = []

    time.sleep(1)
    while i < numberOfOccurence:
    #retrive the text without html balise

        time.sleep(0.3)
        PriceScraped = soup.find_all("span",attrs= {'O8U6h'})[i].text

    #with unicode package -> normalize the data to have a good format
        PriceScraped_goodformat = unicodedata.normalize("NFKD", PriceScraped)
    #add to our list
        price_contains.append(PriceScraped_goodformat)
        i+=1

    print(price_contains)
    date = datetime.date.today()
    date = str(date)
    return WhichFormat(price_contains,brand,date)


#function who just redirect the programm to the right format data extraction
def WhichFormat(priceValue,brand,date):


    Choice = input("Quel type de format ? Uniquement sqlite ou json")
    while Choice is not "sqlite" and "json":
        if Choice == "sqlite":
            return AddToDB(priceValue,brand,date)

        elif Choice == "json":
            return AddToJson(priceValue,brand,date)


#add the datas to a sqlite database
def AddToDB(valueToAdd,brand,Date):

    #setup the connexion to the DataBase created by DataBase.py just before
    try :
        db = "WebScraping_DB.sqlite"
        connection = create_connection(db)

    except Error as e:
        print(e)


    #insert all price in database
    for elt in valueToAdd:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO products(price,project_brand,date) VALUES (?,?,?)',(elt,brand,Date))
        connection.commit()
    print("record OK")




def AddToJson(valueToAdd,brand,date):
    
    
    data = {brand:[{

        "price":valueToAdd,
        "Date":date
    }]}

    with open("data.json","w") as outfile:

        json.dump(data,outfile,ensure_ascii=False)


    fileJson = "data.txt"
    return fileJson




ScrapData()





