import requests
import json

URL = "https://epiwatch-api.azurewebsites.net/api/grid"
page = requests.post(URL)
data = page.json()
dataList = []

def GetEpiwatchData():
    for item in data["results"]:
        print(item)
        date = item["publication_date"]
        disease = item["diseases"]
        location = item["country_name"]
        dataFormatted = {"date":date, "disease":disease, "location" : location}
        dataList.append(dataFormatted)
    return json.dumps(dataList)

def WriteDataToFile(filename):
    f = open(filename, "a")
    f.write(GetEpiwatchData())
    f.close()