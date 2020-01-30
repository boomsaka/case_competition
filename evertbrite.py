import csv 
import requests
from bs4 import BeautifulSoup
import urllib.request

locations = []  # create an empty list to store reviews
#the url you want crawl
for i in range(1,50):
    print(i)
    URL = 'https://www.eventbrite.com/d/united-states/virtual-reality/?page='+str(i)
    ourUrl=urllib.request.urlopen(URL)
    soup = BeautifulSoup(ourUrl,'html.parser')
 #<div class="card-text--truncated__one">Verlocal, New Orleans, LA</div>
    for i in soup.find_all('div',{'class':'card-text--truncated__one'}):  
        location = {}

        location['location'] = i.text
        locations.append(location)
        print(location)
        
    
csv_columns = ['location']
csv_file = "eventbrite.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in locations:
            writer.writerow(data)
except IOError:
    print("I/O error") 