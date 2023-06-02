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
branch = os.environ['INPUT_DEPLOYENV']
appName = os.environ['INPUT_APPNAME']
wait_max_attempt = 120

if token is None:
    sys.exit("Token is not set")

base_url = "https://api.github.com/repos/gocariq/environments/actions"
url_check = base_url + "/runs"
url_trigger = base_url + "/workflows/update-tag.yaml/dispatches"
payload = json.dumps({
    "ref": "main",
    "inputs": {
        "appName": "{0}".format(appName),
        "deployEnv": "{0}".format(branch),
        "tag": "{0}".format(gitSha),
    }
})
headers = {
    'Accept': 'application/vnd.github.everest-preview+json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {0}'.format(token)
}
headersGet = {
    'Accept': 'application/vnd.github.everest-preview+json',
    'Authorization': 'Bearer {0}'.format(token)
}

validateStatusCounter = 0
while validateStatusCounter <= 100:
    response = requests.request("GET", url_check, headers=headersGet)
    if response.reason == 'OK':
        jsonResponse = response.json()
        currentStatus = jsonResponse['workflow_runs'][0]['status']
        logging.info("Latest job status: {0}".format(currentStatus))
        if currentStatus != "queued" and currentStatus != "in_progress":
            logging.info("I do not need to wait, no active actions with status 'in_progress' or 'queued'")
            break
    else:
        max_retry = 3
        logging.warning("Failed to get run I will try {0} times".format(max_retry - validateStatusCounter))
        if validateStatusCounter >= max_retry:
            sys.exit('Failed to get workflow runs: {0}'.format(response.text))
    validateStatusCounter += 1
    time.sleep(10)


logging.info('Dispatch helm update action action')
logging.info(payload)
response = requests.request("POST", url_trigger, headers=headers, data=payload)
if response.status_code != 204:
    sys.exit(response.text)
time.sleep(3)

workflowId = ''
response = requests.request("GET", url_check, headers=headersGet)
if response.reason == 'OK':
    json = json.loads(response.text)
    for node in json['workflow_runs']:
        if node['status'] != 'completed':
            break
    workflowId = node['id']
    logging.info("Found build with id {0}".format(workflowId))
    counter = 0
    while counter < wait_max_attempt:
        url = "https://api.github.com/repos/gocariq/environments/actions/runs/{0}".format(node['id'])
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
