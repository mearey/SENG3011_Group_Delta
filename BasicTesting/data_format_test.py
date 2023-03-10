# File containing tests for the Data Formatting
#Github CI will not come up green if any test is unsuccessful.

# Library imports
import pytest
import re
import json
import requests

# Import functions to be tested
from FormattingData import formattingWHOData, formattingEpiwatchData, combiningDataSets

# Empty test to allow CI to pass & ensure pytest is running correctly.
def test_empty():
    pass

def testWHOTemplate():
    data = formattingWHOData()
    assert list(data.keys()) == ['data_source', 'dataset_type', 'dataset_id', 'time_object', 'events']
    assert data['data_source'] == 'WHO.int'
    assert data['dataset_type'] == 'Disease Info'
    assert data['dataset_id'] == 'https://www.who.int/emergencies/disease-outbreak-news/'
    assert list(data['time_object'].keys()) == ['timestamp', 'timezone']
    for event in data['events']:
        assert list(event) == ['time_object', 'event_type', 'attribute']
        for time_object in event['time_object']:
            assert list(event['time_object']) == ['timestamp', 'duration', 'duration_unit', 'timezone']
        assert event['event_type'] == 'article'
        for attribute in event['attribute']:
            assert list(event['attribute']) == ['disease', 'syndrome', 'location', 'event_date', 'date_of_publication']
        
def testEpiwatchTemplate():
    data = formattingEpiwatchData()
    assert list(data.keys()) == ['data_source', 'dataset_type', 'dataset_id', 'time_object', 'events']
    assert data['data_source'] == 'epiwatch.org'
    assert data['dataset_type'] == 'Disease Info'
    assert data['dataset_id'] == 'https://www.epiwatch.org/reports'
    assert list(data['time_object'].keys()) == ['timestamp', 'timezone']
    for event in data['events']:
        assert list(event) == ['time_object', 'event_type', 'attribute']
        for time_object in event['time_object']:
            assert list(event['time_object']) == ['timestamp', 'duration', 'duration_unit', 'timezone']
        assert event['event_type'] == 'article'
        for attribute in event['attribute']:
            assert list(event['attribute']) == ['disease', 'syndrome', 'location', 'event_date', 'date_of_publication']

"""
def testCombined():
    whoData = formattingWHOData()
    epiwatchData = formattingEpiwatchData()
    combinedData = combiningDataSets()
    assert whoData in combinedData and epiwatchData in combinedData
"""