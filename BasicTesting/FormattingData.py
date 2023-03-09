import requests
import json
from datetime import datetime
import boto3
import os
import logging 

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

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

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    f = open("EpiwatchdataTest.json", "r")
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
    with open("finalData.json","w") as f:
        json.dump(data, f)
        f.close()

def trial():
    # s3 = boto3.client('s3')
    # contents = s3.list_objects(Bucket=os.getenv("GLOBAL_S3_NAME"))
    # print(contents)
    # keys = [item['Key'] for item in contents['Contents']]

   
    LOGGER.info(f"Received event: LMAP")
    return {
        "statusCode": 200,
        "body": "json.dumps(event",
        "headers": {
            "Content-Type": "application/json",
        },
    }
  
if __name__ == "__main__":
    
    