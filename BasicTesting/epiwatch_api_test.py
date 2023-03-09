#File containing tests for the Epiwatch API data

################
# Initialisation
################

#Library imports
import pytest
import re
import json

#Import functions to be tested
from EpiwatchAPI import GetEpiwatchData, WriteDataToFile

#Filenames for tests files
filename_empty = "BasicTesting/testOutput/epiwatchEmpty.json"
filename_basic = "BasicTesting/testOutput/epiwatchBasic.json"

#############################
# Helper Functions & Fixtures
#############################

# JSON Validation Helper Function
def validateJSON(content):
    try:
        json.loads(content)
    except:
        return False
    return True

@pytest.fixture
def epiwatchTest_fixture(scope="funtion"):
    #clear test files
    f = open(filename_basic, "w")
    f.write("")
    f.close()

    f = open(filename_empty, "w")
    f.write("")
    f.close()

#Confirm that the correct JSON output is provided
def test_getEpiwatchData_basicData(epiwatchTest_fixture):
    #Run the function
    output = GetEpiwatchData()
    
    #assert that the JSON returned is non empty
    assert(output != [])

    #for each record make sure they are valid
    for item in output:
        #make sure that all records have the correct keys
        assert(list(item.keys()) == ["date", "disease", "location"])

        #token that checks for a date of format 0000-00-00
        # this is used to assert that evey date is of the correect format
        date_token = "^[0,9][0-9][0-9][0-9]?-[0,9][0,9]-[0,9][0,9]{3}$"

        #assert that each date matches the format
        assert(re.search(date_token, item["date"]))

        #check that the disease feild is of type string (some entires can be empty strings)
        assert(type(item["disease"]) == str)

        #check that the location field is of type string 
        assert(type(item["location"]) == str)
    
#make sure that a valid JSON file is written when the funciton is called
def test_WriteDataToFile_basic(epiwatchTest_fixture):

    #write to file
    WriteDataToFile(filename_basic)

    #access and read file
    f = open(filename_basic, "r")
    content = f.read()

    #Assert file conent are valid JSON
    assert(validateJSON(content))