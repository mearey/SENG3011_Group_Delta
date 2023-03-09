import requests
import json
import nltk
import spacy
nltk.download('averaged_perceptron_tagger')
from bs4 import BeautifulSoup
nlp = spacy.load("en_core_med7_lg")

def checkForMultiCountry(l):
    for item in l:
        if "Multi" in item:
            return "Multi"
        if "Global" in item:
            return "Global"
    return "None"

def findDiseaseName(s):
    disease = nltk.pos_tag(nltk.word_tokenize(s))
    for item in disease:
        if (item[1] == "NNP" or "NNS" or "NN") and not item[0].isdigit():
            disease = item[0]
            return disease
    return "N/A"

def findDiseaseEntity(s):
    result = nlp(s)
    # print(result)
    # print(result.ents)
    for ent in result.ents:
        # print(ent.label_)
        if ent.label_ == "DISEASE":
            return ent.text
    return "N/A"

def retrieveJSONData(i):
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
            date = strings[1].text.strip("| ")
            locationAndDisease = strings[2].text.split(" - ")

            disease = locationAndDisease[0]
            #findDiseaseName(locationAndDisease[0])
            if disease == "Multi":
                disease = locationAndDisease[1]
                #findDiseaseName(locationAndDisease[1])
            
            #if disease == "N/A":
                #URL = item["href"]
                #pageContent = requests.get(URL)
                #soup = BeautifulSoup(pageContent.content, "html.parser")
                #article = soup.find(class_="sf-detail-body-wrapper")
                #disease = str(findDiseaseEntity(article.text))

            location = "N/A"
            multiCountry = checkForMultiCountry(locationAndDisease)
            if multiCountry != "None":
                location = multiCountry
            elif len(locationAndDisease) >= 2:
                location = locationAndDisease[len(locationAndDisease)-1]
            jsonData = {"date":date, "disease":disease, "location" : location}

            dataFormatted.append(jsonData)
            
    return dataFormatted

def refreshAllJSONData(i, filename):
    f = open(filename, "w")
    
    data = retrieveJSONData(i)
            
    f.write(json.dumps(data))
