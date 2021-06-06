//Using K6 for load testing as this is a simple but powerful tool that uses JS for scripting
//These tests can be run from command line, so no GUI is needed
//Other options include Locust.io written in Python
import http from 'k6/http';
import { check, group, sleep } from 'k6';

//Here we can set stages, including duration, ramp-up and target VUs
//We can also set thresholds as part of the validation
export let options = {
  stages: [
    { duration: '1m', target: 50 }, // simulate ramp-up of traffic from 1 to 50 users over 1 minute.
    { duration: '5m', target: 50 }, // stay at 50 users for 5 minutes
    { duration: '1m', target: 0 }, // ramp-down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<5000'], // 95% of requests must complete below 5s
    'Identifier returned successfully': ['p(95)<5000'],
  },
};

//Here we set variables like url, payload, and other parameters
export default function () {
  var url = 'http://127.0.0.1:8088/hash';
  var payload = JSON.stringify({
    password: 'robertog1234'
  });
  var params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };
  http.post(url, payload, params);
}
