import requests
import json
from datetime import datetime
from WebScraper import retrieveJSONData
from EpiwatchAPI import GetEpiwatchData

def formattingWHOData():
    
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    
    allData = retrieveJSONData(1)
    
    newDataEntry = {}
    newDataEntryList = []
    for data in allData:
       
        newDataEntry["time_object"] = {
            "timestamp": data["date"],
            "duration" : 0,
            "duration_unit": "day",
            "timezone": "GMT+11"
        }
        
        newDataEntry["event_type"] = "article"
        newDataEntry["attribute"] = {
            "disease" : data["disease"],
            "syndrome" : [],
            "location" : data["location"],
            "event_date" : data["date"],
            "date_of_publication" : " "
            
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

def formattingEpiwatchData():

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    allData = GetEpiwatchData()

    newDataEntry = {}
    newDataEntryList = []
    for data in allData:
       
        newDataEntry["time_object"] = {
            "timestamp": data["date"],
            "duration" : 0,
            "duration_unit": "day",
            "timezone": "GMT+11"
        }     

        newDataEntry["event_type"] = "article"
        newDataEntry["attribute"] = {
            "disease" : data["disease"],
            "syndrome" : [],
            "location" : data["location"],
            "event_date" : data["date"],
            "date_of_publication" : " "
        }

        newDataEntryList.append(newDataEntry)

    formattedData = {
        "data_source": "epiwatch.org",
        "dataset_type": "Disease Info",
        "dataset_id": "https://www.epiwatch.org/reports",
        "time_object": {
            "timestamp": dt_string,
            "timezone": "GMT+11"
        },
        "events": newDataEntryList
    }

    return formattedData
    

def combiningDataSets(epiwatchData, WHOdata):

    data = []
    data.append(epiwatchData)
    data.append(WHOdata)
    return data

def uploadToS3():
        
    # getting token
    UploadSignUpURL = "https://afzpve4n13.execute-api.ap-southeast-2.amazonaws.com/sign_up"
    UploadLoginUpURL = "https://afzpve4n13.execute-api.ap-southeast-2.amazonaws.com/login"
    jsonDataForSignup = {
        "username": "H14B_DELTA",
        "password": "deltapasswordidklmao127?$%",
        "group": "H14B_DELTA"
    }

    requests.post(UploadSignUpURL, json = jsonDataForSignup)  
    data = requests.post(UploadLoginUpURL, json = jsonDataForSignup)  
    token = json.loads(data.text)["token"] 

    # uploading datasets
    UploadToS3 = "https://afzpve4n13.execute-api.ap-southeast-2.amazonaws.com/F14A_SIERRA/upload"


    jsonDataForUploadList = combiningDataSets(formattingEpiwatchData(), formattingWHOData())
    tokenHeaderDict = {"Authorization" : token}
    
    for dataSet in jsonDataForUploadList:
        requests.post(UploadToS3, json=dataSet, headers=tokenHeaderDict)
        
  
if __name__ == "__main__":
    uploadToS3()
   

    