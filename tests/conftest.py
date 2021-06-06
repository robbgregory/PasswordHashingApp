"""
This is a sample confest.py file that should be placed under the tests folder
The file is used to store fixtures and make them available to any tests in their Scope
Should the project expand to include UI, etc., separate conftest files can also be created under subfolders
"""
import pytest
from faker import Faker

myFactory = Faker()  # Using the Faker class to create a myFactory object, used to create Faker 'words' for password


# Create fixtures for repeated actions like getting URLs
@pytest.fixture(scope="module")
def base_url():
    return "http://127.0.0.1:8088"


# Create fixture for endpoints
@pytest.fixture(scope="module")
def hash_endpoint():
    return "/hash"


# Create fixture for endpoints
@pytest.fixture(scope="module")
def stats_endpoint():
    return "/stats"


# Create fixture for Post body
@pytest.fixture(scope="module")
def post_payload():
    data = "{ \"password\":\"myFactory.words()\"\r\n}"  # Using Faker to create random word for password
    return data


# Create fixture for headers
@pytest.fixture(scope="module")
def headers():
    headers = {
        'Accept': 'application/json'
    }
    return headers


# Create fixture for schema validation
@pytest.fixture(scope="module")
def schema():
    schema = {
        "TotalRequests": "integer",
        "AverageTime": "integer"
    }
    return schema
