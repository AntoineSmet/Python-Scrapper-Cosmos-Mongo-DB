import requests
from bs4 import BeautifulSoup as bs
import pymongo
import json

myclient = pymongo.MongoClient("mongodb://******************************")
#Your DataBase Name
mydb = myclient["MyDataBase"]
#Your Collection Name
mycol = mydb["MyCollection"]


#change the url to the one you want to scrape
URL = 'WebSiteURL'
number = 0
#change the number to begin where you want to start
page_begin = 1
#change the number to the number of pages you want to scrape
page_end = 230 + 1
#open the file name where you want to save the data
file_txt = open("data.txt", "w", encoding="UTF-8")

#if you want to scrape only one page, change the page_end to page_begin or delete the loop
for page in range(page_begin, page_end):
    #check the url for all pages you want to scrapp and add if there other thing that just the number of the page in url
    req = requests.get(URL + str(page))
    #filter the data by div like a funnel
    soup = bs(req.text, 'html.parser')
    #find the div with the class name and replace card it with the div you want to scrape
    mother = soup.find('div', attrs={'class', 'card'})
    sons = mother.find_all('div', attrs={'class', 'p-2'})
    for son in sons:
        number = number+1
        #change the final name of the div you want to scrape
        elements = son.find_all('a', attrs={'class', 'text-dark'})
        #extract the text from the div
        title = elements[0].text
        #replace characters that you don't want in the text
        title = title.replace('"', "'")
        data_json = '''
                {
                    "id": %s,
                    "title": "%s"
                } 
                ''' % (number, title)
        #transform the data in json
        alpha = json.loads(data_json)
        #insert the data in the database
        mycol.insert_one(alpha)
        #write like you want the data in the file
        data_txt = "%s - %s\n" % (number, title)
        file_txt.write(data_txt)
        #print the result in the terminal just to check if it is working
        print(data_txt)
#close the file name where you want to save the data
file_txt.close()