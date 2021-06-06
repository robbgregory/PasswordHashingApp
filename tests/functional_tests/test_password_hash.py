"""
Tests are written in PyTest. Please see the requirements.txt file for all dependencies needed.
Note: PyTest tests can be included in single Python file, as shown here, or as separate files.
Including this file as an example of non-BDD approach, but Gherkin-based frameworks are great for..
..integration and end-to-end testing to this file may not be needed.
Lastly, using mark to help with searching, tagging, etc., which is a great practice to follow.
"""
from pytest import mark  # Using the mark function from PyTest to help group tests
import requests  # Requests is an additional dependency needed for using PyTest for API functional testing
from jsonschema import validate


@mark.smoke  # Include as part of smoke tests
@mark.regression  # Include as part of regression tests
@mark.password_hash  # Include as part of password_hash test suite
# Creating post request test for hash endpoint
def test_post_hash_endpoint(base_url, hash_endpoint, post_payload, headers):
    url = base_url + hash_endpoint
    # url = "http://127.0.0.1:8088/hash"
    payload = post_payload
    headers = headers

    response = requests.request("POST", url, headers=headers, data=payload)  # Create variable to capture response
    print(response.text)
    assert response.status_code == 200


# Negative test to check for invalid (NULL) body passed
@mark.regression  # Include as part of regression tests
@mark.password_hash  # Include as part of password_hash test suite
def test_post_negative_missing_password(base_url, hash_endpoint, headers):
    url = base_url + hash_endpoint

    payload = "{ \"password\":\"\"\r\n}"
    headers = headers

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    assert response.status_code == 400  # Should get 400 since no password is sent


# Negative test to check for NO body passed
# Should get 400 response
@mark.regression  # Include as part of regression tests
@mark.password_hash  # Include as part of password_hash test suite
def test_post_negative_no_body(base_url, hash_endpoint, headers):
    url = base_url + hash_endpoint

    payload = ""
    headers = headers

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    assert response.status_code == 400  # Should get 400 since no password is sent


# Creating post request and then checking this is created with Get
@mark.smoke  # Include as part of smoke tests
@mark.regression  # Include as part of regression tests
@mark.password_hash  # Include as part of password_hash test suite
def test_post_end2end_hash(base_url, hash_endpoint, post_payload, headers):
    # Create a Post request to generate new identifier
    url = base_url + hash_endpoint
    # url = "http://127.0.0.1:8088/hash"
    payload = post_payload
    headers = headers
    response = requests.request("POST", url, headers=headers, data=payload)  # Create variable to capture response
    print(response.text)

    job_identifier = response.text  # Capture the response value as variable
    # Now send get request to check the latest identifier and retrieve hash result
    url = base_url + hash_endpoint + '/' + job_identifier  # Use the base URL with /hash and new identifier
    headers = headers
    response = requests.request("GET", url, headers=headers)

    print(response.text)
    assert response.status_code == 200


# Test a basic get call to hash for existing identifier
@mark.smoke
@mark.regression
@mark.password_hash
def test_get_functions_as_expected(base_url, hash_endpoint, headers):

    url = base_url + hash_endpoint + '/1'
    headers = headers

    response = requests.request("GET", url, headers=headers)

    print(response.text)
    assert response.status_code == 200


# Test to validate that when sending a identifier that does not exist, 400 returned
@mark.regression
@mark.password_hash
def test_get_invalid_identifier_check_400(base_url, hash_endpoint, headers):

    url = base_url + hash_endpoint + '/1000'
    headers = headers

    response = requests.request("GET", url, headers=headers)

    print(response.text)
    assert response.status_code == 400  # Should get a 400 response in this scenario


# Test a basic get call to stats for 200 response
@mark.smoke
@mark.regression
@mark.password_hash
def test_get_stats_check_status_code_equals_200(base_url, stats_endpoint, schema):
    url = base_url + stats_endpoint

    response = requests.request("GET", url)

    print(response.text)

    # Validate response headers and body contents, such as status code.
    assert response.status_code == 200
    # Validate response content type header is JSON
    assert response.headers["Content-Type"] == "application/json"

    # Example of validating against expected schema
    data = requests.get(url).json()
    validate(data, schema)

