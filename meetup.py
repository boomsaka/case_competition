import csv 
import time
import requests
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

SCROLL_PAUSE_TIME = 0.5

clubs = []  # create an empty list to store reviews
#the url you want crawl

URL = 'https://www.meetup.com/find/?allMeetups=false&keywords=VR&radius=Infinity&userFreeform=us&gcResults=United+States%3AUS%3Anull%3Anull%3Anull%3Anull%3Anull%3A37.09024%3A-95.71289100000001&change=yes&sort=recommended&eventFilter=mysugg'
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(URL)

driver.find_element_by_xpath('//*[@id="simple-view"]/div[1]/div[2]/div/span').click()

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


soup = BeautifulSoup(driver.page_source,'html.parser')

#print(soup.prettify())
counter = 0

#list to store url for each club
url_list = []
clubs = []

for i in soup.find_all('li',{'class':'groupCard tileGrid-tile noRatings'}):
    #print(i)
    counter +=1
    club = {}

    #data cleaning
    name = str(i.find('h3').text[2:]).replace(' ','').replace('\n','')
    count_members = str(i.find('p').text[:]).replace(' ','')
    count_members = re.sub("\D", "", count_members)
    club_url = str(i.find('a'))[30:-(len(str(i.find('a'))[30:])-str(i.find('a'))[30:].find('">'))]
    url_list.append(club_url)


    #assign keys and values to the club dictionary
    club['Name'] = name
    club['Member counts'] = count_members
    club['URL'] = club_url

    clubs.append(club)
    #print(club_url)
    
#print(clubs)
#print(url_list)
print(str(counter)+' groups are crawled') #==1201


count = 0
locations = []
for i in url_list:

    ourUrl=urllib.request.urlopen(i)
    soup = BeautifulSoup(ourUrl,'html.parser')
    
    
    for i in soup.find_all('a',{'class':'groupHomeHeaderInfo-cityLink'}):
        count += 1
        location = {}

        location['Location'] = str(i.find('span')).replace('<span>','').replace('</span>','')
        locations.append(location)
    
print(locations)
print(count)

csv_columns = ['Name','Member counts','URL']
csv_file = "clubs.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in clubs:
            writer.writerow(data)
except IOError:
    print("I/O error") 

csv_columns1 = ['Location']
csv_file = "locations.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns1)
        writer.writeheader()
        for data in locations:
            writer.writerow(data)
except IOError:
    print("I/O error") 
