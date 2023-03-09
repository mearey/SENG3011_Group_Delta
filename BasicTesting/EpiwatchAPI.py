import requests
import json

URL = "https://epiwatch-api.azurewebsites.net/api/grid"
page = requests.post(URL)
data = page.json()
dataList = []

def GetEpiwatchData():
    print(data["results"])
    for item in data["results"]:
        date = item["publication_date"]
        try:
            disease = item["diseases"]
        except KeyError:
            disease = item["disease"]

        location = item["country_name"]
        dataFormatted = {"date":date, "disease":disease, "location" : location}
        dataList.append(dataFormatted)
    return dataList

def WriteDataToFile(filename):
    f = open(filename, "a")
    f.write(json.dumps(GetEpiwatchData()))
    f.close()