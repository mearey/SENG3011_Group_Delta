import requests
import json
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
from bs4 import BeautifulSoup

def checkForMultiCountry(l):
    for item in l:
        if "Multi" in item:
            return "Multi"
        if "Global" in item:
            return "Global"
    return "None"

def retrieveJsonData(i):
    
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
            locationAndDisease = strings[2].text.split(" - ")

            disease = nltk.pos_tag(nltk.word_tokenize(locationAndDisease[0]))
            if disease == "Multi":
                disease = nltk.pos_tag(nltk.word_tokenize(locationAndDisease[1]))

            for item in disease:
                if item[1] == "NNP" or "NN" or "NNS":
                    disease = item[0]
                    break

            location = "N/A"
            multiCountry = checkForMultiCountry(locationAndDisease)
            if multiCountry != "None":
                location = multiCountry
            elif len(locationAndDisease) >= 2:
                location = locationAndDisease[len(locationAndDisease)-1]
            
            jsonData = {"date":date, "disease":disease, "location" : location}

            dataFormatted.append(jsonData)
    
    return dataFormatted

# default filename: "WHOdataTest.json"
def refreshAllJsonData(i, filename):
    f = open(filename, "w")
    
    jsonData = retrieveJsonData(i)
            
    f.write(json.dumps(jsonData))
    f.close()