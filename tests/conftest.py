"""
This is a sample confest.py file that should be placed under the tests folder.
The file is used to store fixtures and make them available to any tests in their Scope.
Should the project expand to include UI, etc., separate conftest files can also be created under subfolders.
"""
import pytest
from faker import Faker
import requests  # Requests is an additional dependency needed for using PyTest for API functional testing

myFactory = Faker()  # Using the Faker class to create a myFactory object, used to create Faker 'words' for password


# The below configurations are used for ReportPortal integration
# These settings could be added to the pytest.ini file, but adding here in the Conftest.py file
def pytest_addoption(parser):
    # Method to add the option to pytest.ini file
    parser.addini("rp_uuid",'help',type="pathlist")
    parser.addini("rp_endpoint",'help',type="pathlist")
    parser.addini("rp_project",'help',type="pathlist")
    parser.addini("rp_launch",'help',type="pathlist")

@pytest.hookimpl()
def pytest_configure(config):
    # Sets the launch name based on the marker selected.
    # Specific values for report portal come from settings page on ReportPortal
    suite = config.getoption("markexpr")
    try:
        config._inicache["rp_uuid"]="eca258d8-0389-4473-bdf0-b9573cd7f2fc"
        config._inicache["rp_endpoint"]="https://demo.reportportal.io"
        config._inicache["rp_project"]="robertg1979_personal"
        if suite == "password_hash":
            config._inicache["rp_launch"]="password_hash"
        elif suite == "smoke":
            config._inicache["rp_launch"]="smoke"
        elif suite == "regression":
            config._inicache["rp_launch"]="regression"

    except Exception as e:  # Capture exception
        print (str(e))


# Define the host URL that will be used as a test fixture
# Note: URLs can also be captured in separate config file once we have more than one environment
@pytest.fixture(scope="module")
def host_url():
    return "http://127.0.0.1:8088"


# Create fixture for Post body that uses Fake test data
@pytest.fixture(scope="module")
def hash_payload():
    data = "{ \"password\":\"myFactory.words()\"\r\n}"  # Using Faker to create random word for password
    return data


# Create fixture for hash endpoint that will be be passed in request
@pytest.fixture(scope="module")
def hash_endpoint():
    return "/hash"


# Create fixture for stats endpoint that will be be passed in request
@pytest.fixture(scope="module")
def stats_endpoint():
    return "/stats"


# Create fixture for headers that will be be passed in request
@pytest.fixture(scope="module")
def headers():
    headers = {
        'Accept': 'application/json'
    }
    return headers


# Create fixture for POST to /hash path that all tests can utilize
@pytest.fixture(scope="module")
def post_hash(host_url, hash_endpoint, headers, hash_payload):
    """Http POST method"""
    url = host_url + hash_endpoint # Using the base url and hash endpoints as full URL

    headers = headers

    payload = hash_payload  # Using default payload set above

    response = requests.post(url, headers=headers, data=payload)  # Create response variable to capture result
    return response


# Create fixture for GET to /hash path that all tests can utilize
@pytest.fixture(scope="module")
def get_hash(host_url, hash_endpoint):
    """Http GET method"""
    url = host_url + hash_endpoint + '/1'  # Using the base url, hash endpoint and safe value of 1

    response = requests.get(url)  # Create response variable to capture result
    return response


# Create fixture for GET to /stats path that all tests can utilize
@pytest.fixture(scope="module")
def get_stats(host_url, stats_endpoint):
    """Http GET method"""
    url = host_url + stats_endpoint # Using the base url and stats endpoints as full URL

    response = requests.get(url)  # Create response variable to capture result
    return response


# Create fixture for schema validation
@pytest.fixture(scope="module")
def schema():
    schema = {
        "TotalRequests": "integer",
        "AverageTime": "integer"
    }
    return schema
