import requests
import json
from bs4 import BeautifulSoup

WHOURL = "https://www.who.int/emergencies/disease-outbreak-news"

i = 140

f = open("WHOdataTest.json", "a")
dataFormatted = json.loads("[]")
while i > 0:
    WHOURL = "https://www.who.int/emergencies/disease-outbreak-news/" + str(i)
    i = i - 1

    who = requests.get(WHOURL)
    soup = BeautifulSoup(who.content, "html.parser")
    content = soup.find(id="PageContent_C010_Col00")
    list = content.find_all(class_="sf-list-vertical__item")

    for item in list:
        title = item.find(class_="sf-list-vertical__title") 
        strings = title.find_all()

        date = strings[1].text
        locationAndDisease = strings[2].text.split("-")
        disease = locationAndDisease[0]
        location = "N/A"
        
        if len(location) == 2:
            location = locationAndDisease[1]
        
        jsonData = {"date":date, "disease":disease, "location" : location}

        dataFormatted.append(jsonData)
        
f.write(json.dumps(dataFormatted))
f.close()