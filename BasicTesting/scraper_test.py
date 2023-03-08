# File containing general pytests. Keep in mind that Github CI will not come up green if any test is unsuccessful.

from WebScraper import checkForMultiCountry

# Confirm that the multi country check is negative for an empty list.
def test_checkForMultiCountry_empty():
    l = []
    assert(checkForMultiCountry(l)) == "None"

# Confirm that the multi country check returns a positive for 'Multi' if a list item
# contains the word.
def test_checkForMultiCountry_multi():
    l = ["Australia", "Bulgaria", "Chile", "Multi"]
    assert(checkForMultiCountry(l)) == "Multi"
    
    l = ["Here", "Comes", "A", "Multicountry"]
    assert(checkForMultiCountry(l)) == "Multi"

# Confirm that the multi country check returns a positive for 'Global' if a list item
# contains the word.
def test_checkForMultiCountry_global():
    l = ["One", "Two", "Three", "Global"]
    assert(checkForMultiCountry(l)) == "Global"
    
    l = ["Checking", "For", "Globalisation"]
    assert(checkForMultiCountry(l)) == "Global"

# Confirm that the multi country check returns a negative match if the list is non-empty but
# contains neither 'Multi' nor 'Global'.
def test_checkForMultiCountry_none():
    l = ["These", "Are", "Not", "Countries"]
    assert(checkForMultiCountry(l)) == "None"