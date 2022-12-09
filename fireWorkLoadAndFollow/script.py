#!/usr/bin/python3
import os
import sys
import time
import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
token = os.environ['INPUT_AUTHTOKEN']
gitSha = os.environ['INPUT_TAG']
targetEnv = os.environ['INPUT_TARGETENV']
workflowName = os.environ['INPUT_WORKFLOWFILENAME']
wait_max_attempt = 120

if token is None:
    sys.exit("Token is not set")
else:
    logging.info("this is token: {0}".format(token))

url_trigger = "https://api.github.com/repos/gocariq/environments/actions/{0}.yaml/dispatches".format(workflowName)
payload = json.dumps({
    "ref": "main",
    "inputs": {
        "target-env": "{0}".format(targetEnv ),
        "tag": "{0}".format(gitSha),
    }
})
headers = {
    'Accept': 'application/vnd.github.everest-preview+json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {0}'.format(token)
}
url_dispatch = "https://api.github.com/repos/gocariq/payment-automation/actions/runs"
headersGet = {
    'Accept': 'application/vnd.github.everest-preview+json',
    'Authorization': 'Bearer {0}'.format(token)
}

logging.info('Dispatch helm update action action')
logging.info(payload)
response = requests.request("POST", url_trigger, headers=headers, data=payload)
if response.status_code != 204:
    sys.exit(response.text)
time.sleep(3)

workflowId = ''
response = requests.request("GET", url_dispatch, headers=headersGet)
if response.reason == 'OK':
    json = json.loads(response.text)
    for node in json['workflow_runs']:
        if node['status'] != 'completed':
            break
    workflowId = node['id']
    logging.info("Found build with id {0}".format(workflowId))
    counter = 0
    url = "https://api.github.com/repos/gocariq/payment-automation/actions/runs/{0}".format(workflowId)
    while counter < wait_max_attempt:
        run = requests.request("GET", url, headers=headersGet)
        runJson = run.json()
        currentStatus = runJson['status']
        logging.info("Current run id: {0} has status: {1} ".format(runJson['id'], runJson['status']))
        conclusion = runJson['conclusion']
        run_number = runJson['run_number']
        if currentStatus == "completed":
            if conclusion != 'success':
                message = "Run number:{0} concluded with status:{1} with run has been finished".format(run_number, conclusion)
                assert False, message
            else:
                logging.info("Run:{0} has been finished with conclusion:{1}".format(run_number, conclusion))
            break
        time.sleep(10)
        counter += 1
else:
    AssertionError("Failed to fetch run")
