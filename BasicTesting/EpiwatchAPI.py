import requests

URL = "https://epiwatch-api.azurewebsites.net/api/grid"

page = requests.post(URL)

data = page.json()

def GetDataType(datatype):
    l = []
    if datatype == "all":
        for item in data["results"]:
            l.append(item)
    else:
        for item in data["results"]:
            l.append(item[datatype])
    return l