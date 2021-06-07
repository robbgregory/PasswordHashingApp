"""
Tests are written in PyTest. Please see the requirements.txt file for all dependencies needed.
Note: PyTest tests can be included in single Python file, as shown here, or as separate files.
Lastly, using mark to help with searching, tagging, etc., which is a great practice to follow.
"""
from pytest import mark  # Using the mark function from PyTest to help group tests
import requests  # Requests is an additional dependency needed for using PyTest for API functional testing
from jsonschema import validate


@mark.smoke  # Include as part of smoke tests
@mark.regression  # Include as part of regression tests
@mark.password_hash  # Include as part of password_hash test suite
# Creating post request test for hash endpoint
def test_post_hash_endpoint(post_hash):

    new_post = post_hash  # Make use of the test fixture that runs this post

    print(new_post)

    assert new_post.status_code == 200  # Basic 200 assertion here

    assert int(new_post.text) >= 1  # The identifier returned should at least be one if successful


@mark.regression  # Include as part of regression tests
@mark.password_hash  # Include as part of password_hash test suite
# Negative test to check for invalid (NULL) body passed
def test_post_negative_missing_password(host_url, hash_endpoint, headers):

    url = host_url + hash_endpoint  # This time I am passing these through individually

    payload = "{ \"password\":\"\"\r\n}"  # Sending a custom payload so not using the fixture for base request

    headers = headers

    response = requests.post(url, headers=headers, data=payload)

    print(response.text)

    assert response.status_code == 400  # Should get 400 since no password is sent


@mark.regression
@mark.password_hash
# Negative test to check for NO body passed
# Should get 400 response
def test_post_negative_no_body(host_url, hash_endpoint, headers):

    url = host_url + hash_endpoint

    payload = ""  # Passing NULL / empty payload

    headers = headers

    response = requests.post(url, headers=headers, data=payload)

    print(response.text)

    assert response.status_code == 400  # Should get 400 since no password is sent


@mark.smoke
@mark.regression
@mark.password_hash
# Creating post request and then checking this is created with Get
def test_post_end2end_hash(post_hash, host_url, hash_endpoint, headers):
    # Create a Post request to generate new identifier
    new_post = post_hash  # Make use of the test fixture that runs this post

    job_identifier = new_post.text  # Capture the response value as a variable
    # Now send get request to check the latest identifier and retrieve hash result
    url = host_url + hash_endpoint + '/' + str(job_identifier) # Use the base URL with /hash and new identifier

    new_get = requests.get(url)  # Create response variable to capture result

    print(new_get.text)  # Print out the value
    assert new_get.status_code == 200  # Check for 200 response that confirms new POST request created a valid identifier


@mark.smoke
@mark.regression
@mark.password_hash
# Test a basic get call to hash for existing identifier
def test_get_functions_as_expected(get_hash):

    new_get = get_hash  # Using the test fixture that uses 1 as the identifier by default

    print(new_get.text)  # Print out the value

    assert new_get.status_code == 200  # Check for 200 response
    # Note: Following practice of Arrange, Act & Assert, so since one action here, more than one assertion is acceptable
    assert len(new_get.text) == 88 # This is not a direct test of a base64 response, but does check if it has correct length


@mark.regression
@mark.password_hash
# Test to validate that when sending a identifier that does not exist, 400 returned
def test_get_invalid_identifier_check_400(host_url, hash_endpoint):

    url = host_url + hash_endpoint + '/1000' # Just using a known value that will NOT exist

    new_get = requests.get(url)  # Create response variable to capture result

    print(new_get.text)
    assert new_get.status_code == 400  # Should get a 400 response in this scenario


@mark.smoke
@mark.regression
@mark.password_hash
# Test a basic get call to stats for 200 response using schema
def test_get_stats_check_status_code_equals_200(get_stats, schema):

    new_get = get_stats
    print(new_get.text)

    # Validate response headers and body contents, such as status code.
    assert new_get.status_code == 200
    # Validate response content type header is JSON
    assert new_get.headers["Content-Type"] == "application/json"

    # Example of validating against expected schema
    data = new_get.json()
    validate(data, schema)


@mark.smoke
@mark.regression
@mark.password_hash
# Test that max number of requests is also available as a valid identifier
# So this tests runs the get to stats and then checks the value against /hash as a get
def test_max_requests_exists_as_identifier(get_stats, host_url, hash_endpoint):

    new_get = get_stats  # Start with a get to stats

    response_data = new_get.json()  # Capture the json body from results

    print(response_data["TotalRequests"])  # Print out the value for for TotalRequests

    total_request_val = response_data['TotalRequests']  # Capture the TotalRequests value as variable

    url = host_url + hash_endpoint + '/' + str(total_request_val) # Use the base URL with /hash and new identifier

    new_get = requests.get(url)  # Create response variable to capture result

    print(new_get.text)

    assert new_get.status_code == 200  # Check that this identifier exists
