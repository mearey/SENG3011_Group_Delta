import requests
import json
from datetime import datetime

def fromattingWHOData():
    
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    f = open("WHOdataTest.json", "r")
    allData = json.load(f)
    
    newDataEntry = {}
    newDataEntryList = []
    for data in allData:
       
        newDataEntry["timeobject"] = {
            "timestamp": data["date"],
            "duration" : 0,
            "duration_unit": "day",
            "timezone": "GMT+11"
        }
        

        newDataEntry["event_type"] = "article"
        newDataEntry["attribute"] = {
            "country" : data['location'],
            "disease" : data["disease"]
        }

        newDataEntryList.append(newDataEntry)


    formattedData = {
        "data_source": "WHO.int",
        "dataset_type": "Disease Info",
        "dataset_id": "https://www.who.int/emergencies/disease-outbreak-news/",
        "time_object": {
            "timestamp": dt_string,
            "timezone": "GMT+11"
        },
        "events": newDataEntryList
    }

    return formattedData

def fromattingEpiwatchData():

    formattedData = {}
    return formattedData

def combiningDataSets(epiwatchData, WHOdata):
    


if __name__ == "__main__":
    fromattingWHOData(); 