# File containing tests for the WHO Webscraper. 
# Github CI will not come up green if any test is unsuccessful.

################
# Initialisation
################

# Library imports
import pytest
import re
import json

# Import functions to be tested
from WebScraper import checkForMultiCountry, refreshAllJSONData, retrieveJSONData

# Filenames of test files
filename_empty = "BasicTesting/testOutput/scraperTestEmpty.json"
filename_basic = "BasicTesting/testOutput/scraperTestBasic.json"

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

# Test initialisation fixture
@pytest.fixture
def scraperTest_fixture(scope="function"):
    # Clear test output files.
    # Make sure your directory is set to inside the repo folder.
    f = open(filename_empty, "w")
    f.write("")
    f.close()

    f = open(filename_basic, "w")
    f.write("")
    f.close()

############################
# checkForMultiCountry tests
############################

# Confirm that the multi country check is negative for an empty list.
def test_checkForMultiCountry_empty(scraperTest_fixture):
    l = []
    assert(checkForMultiCountry(l)) == "None"

# Confirm that the multi country check returns a positive for 'Multi' if a list item
# contains the word.
def test_checkForMultiCountry_multi(scraperTest_fixture):
    l = ["Australia", "Bulgaria", "Chile", "Multi"]
    assert(checkForMultiCountry(l)) == "Multi"
    
    l = ["Here", "Comes", "A", "Multicountry"]
    assert(checkForMultiCountry(l)) == "Multi"

# Confirm that the multi country check returns a positive for 'Global' if a list item
# contains the word.
def test_checkForMultiCountry_global(scraperTest_fixture):
    l = ["One", "Two", "Three", "Global"]
    assert(checkForMultiCountry(l)) == "Global"
    
    l = ["Checking", "For", "Globalisation"]
    assert(checkForMultiCountry(l)) == "Global"

# Confirm that the multi country check returns a negative match if the list is non-empty but
# contains neither 'Multi' nor 'Global'.
def test_checkForMultiCountry_none(scraperTest_fixture):
    l = ["These", "Are", "Not", "Countries"]
    assert(checkForMultiCountry(l)) == "None"
    
########################
# retrieveJSONData Tests
########################

# Confirm that an empty JSON output is returned when argument is 0.
def test_retrieveJSONData_empty(scraperTest_fixture):
    assert(retrieveJSONData(0)) == []

# Confirm that an argument of 1 returns valid content.
def test_retrieveJSONData_basicContent(scraperTest_fixture):
    # Run the function 
    output = retrieveJSONData(1)
    
    # Assert that the returned JSON is non-empty
    assert(output != [])
    
    # Confirm that each record is valid.
    for record in output:
        # ASSERT: that all of the returned content has expected fields.
        assert(list(record.keys()) == ['date', 'disease', 'location'])
    
        # ASSERT: that each item in a date field is in date format using string matching.
        # The token checks for a day without leading zeroes, followed by a capitalised month name,
        # and a year consisting of 4 digits that begins with 1 or 2.
        date_token = "^[1-9][0-9]? (January|February|March|April|May|June|July|August|September|\
            October|November|December) [1-2][0-9]{3}$"
        
        # Confirm that each date matches the token.
        assert(re.search(date_token, record['date']))
    
        # ASSERT: that the disease field contains letters - no disease's name can be purely numbers/symbols.
        disease_token = "[A-z]+"
        assert(re.search(disease_token, record['disease']))
    
        # ASSERT: that the location field contains letters - no location's name can be purely numbers/symbols.
        location_token = "[A-z]+"
        assert(re.search(disease_token, record['location']))
        

# Confirm that an argument of 2 returns more content than an argument of 1.
def test_retrieveJSONData_contentIncreases(scraperTest_fixture):
    onePage = retrieveJSONData(1)
    twoPage = retrieveJSONData(2)
    
    assert(len(twoPage) > len(onePage))
    
#
# refreshAllJSONData Tests
#

# Confirm that a valid, empty JSON file is written when i argument is 0.
def test_refreshAllJSONData_empty(scraperTest_fixture):
    # Write to file
    refreshAllJSONData(0,filename_empty)
    
    # Access & read file
    f = open(filename_empty, "r")
    content = f.read()
    
    # Assert file contents are valid JSON
    assert(validateJSON(content))
    
    # Assert file contents are empty
    assert(content == '[]')
    

# Confirm that a valid, populated JSON file is written when i argument is 1.
def test_refreshAllJSONData_basic(scraperTest_fixture):
    
    # Write to file
    refreshAllJSONData(1,filename_basic)
    
    # Access & read file
    f = open(filename_basic, "r")
    content = f.read()
    
    # Assert file contents are valid JSON
    assert(validateJSON(content))
    
    # Assert file contents are non-empty
    assert(content != '[]')
