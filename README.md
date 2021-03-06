# PasswordHashingApp
This is a sample application that includes a PyTest API automation framework, along with test results documentation and sample K6 performance tests.

This is not intended to serve as a comprehensive test automation framework with all applicable tests, but does showcase certain features such as:
  - Use of test fixtures to reduce excessive code, which are stored in conftest.py file
  - Use of pytest.ini file that can list naming conventions for discovering tests for pytest to run, along with markers, which helps with searching and long term project maintenance
  - Use of K6 for performance testing, which is a very light-weight tool that uses JavaScript for scripting but pairs well with other tools like Postman (i.e. Postman collections
    can easily be converted to K6 scripts with k6-to-postman converter plugin)
  - Some basic test examples and assertions for validation
  - Pytest-xdist which allows for executing tests in parallel from command line
  
**Other notes on tools:**
  - To add in BDD, we could use pytest-bdd as this is a plugin that complements and takes advantage of pytest's list of great features and is not a separate BDD tool like Behave or Lettuce.
  - To limit the amount of external dependencies, Locust.io could be added as an additional Python dependency and this could be used instead of K6.
     - Locust also utilizes Pythong for scripting, which is an advantage over introducing JS to this project, but K6 is multithreaded by default where as Locust is not
     - K6 is also written in Go and performs very well
     - Locust does offer distributed load testing (which is a huge plus), where as K6 requires the paid version for this feature. 
     
 **System Requirements:**
 
   Python 3.8+

   K6 Installed 

      macOS -- $ brew install k6
      windows -- choco install k6 
   
 **Setting up the project:**
  1. Clone the git repository
  2. Navigate to project folder
  3. Install the requirements using: pip install -r requirements.txt
  4. Execute tests using 'pytest' from terminal at project root directory

**Dashboard & Reporting:**
Many teams will use a tool like Jira or Rally for capturing and reporting on test cases and defects, but for this project, the options evaluated were:
  
   - ReportPortal.io 
  
   - Allure plus InfluxDB and Grafana (could be generated with Docker Compose for simplicity and repeatibility)

Here I chose to integrate ReportPortal.io by (1) signing up for a demo account (https://reportportal.io/), (2) using the configuration details for my ReportPortal.io account with the project conftest.py file, and (3) simply adding the pytest-reportportal dependency to the project (requirements file). 

ReportPortal integrates very well with pytest and considering that the project already uses markers to segment testing, these existing pytest markers can be used as "launches" for ReportPortal. From there it is just a matter of adding widgets to the dashboard. Note: A defect widget would be ideal, but I am unable to pull data in for defects.

Added a PDF version of an example dashboard created for this project.

**Note to reviewers:** 
Please start with the "Test-Plan-Password-Hashing-Application-Gregory" file to review test plan and test cases

**Running pytest tests by tag**

pytest -k smoke

pytest -k regression

pytest -k password_hash

**Running pytest tests with html report**

pytest --html=report.html

**Running k6 tests with html report**

cd tests/perf_tests

k6 run test_post_k6.js --out html

**Running pytest with ReportPortal integration**

pytest -m smoke --reportportal

(Note: "smoke" can be substituted for any valid marker setup in the project with the mark class)
k6 run test_post_k6.js --out html
