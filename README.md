# PasswordHashingApp
This is a sample application that includes a PyTest API automation framework, along with test results documentation and sample K6 performance tests.

This is not intended to serve as a comprehensive test automation framework with all applicable tests, but does showcase certain features such as:
  - Use of test fixtures to reduce excessive code, which are stored in conftest.py file
  - Use of pytest.ini file that can list naming conventions for discovering tests for pytest to run, along with markers, which helps with searching and long term project maintenance
  - Use of K6 for performance testing, which is a very light-weight tool that uses JavaScript for scripting but pairs well with other tools like Postman (i.e. Postman collections
    can easily be converted to K6 scripts with k6-tp-postman converter plugin)
  - Some basic test examples and assertions for validation
  - Pytest-xdist which allows for executing tests in parallel from command line
  
**Other notes on tools:**
  - To add in BDD, we could use pytest-bdd as this is a plugin that complements and takes advantage of pytest's list of great features and is not a separate BDD tool like Behave or Lettuce.
  - To limit the amount of external dependencies, Locust.io could be added as an additional Python dependency and this could be used instead of K6.
     - Locust also utilizes Pythong for scripting, which is an advantage over introducing JS to this project, but K6 is multithreaded by default where as Locust is not
     - K6 is also written in Go and performs very well
     - Locust does not offer distributed load testing, where as K6 requires the paid version for this feature. 
     
 **System Requirements:**
   Python 3.8+
   
 **Setting up the project:**
  1. Clone the git repository
  2. Navigate to project folder
  3. Install the requirements using: pip install -r requirements.txt
  4. Execute tests using 'pytest' from terminal at project root directory

**Note to reviewers:** 
Please start with the "Test-Plan-Password-Hashing-Application-Gregory" file to review test plan and test cases
