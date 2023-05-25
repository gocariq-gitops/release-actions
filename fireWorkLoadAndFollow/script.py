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
target_repository = os.environ['INPUT_TARGETREPO']
wait_max_attempt = 120

if target_repository is None or target_repository == '':
    target_repository = 'payment-automation'

if token is None or token == '':
    sys.exit("Token is not set")

base_url = "https://api.github.com/repos/gocariq/{0}".format(target_repository)

url_trigger = "{0}/actions/workflows/{1}.yaml/dispatches".format(base_url, workflowName)
logging.info(url_trigger)
payload = json.dumps({
    "ref": "main",
    "inputs": {
        "target-env": "{0}".format(targetEnv),
        "tag": "{0}".format(gitSha),
    }
})
headers = {
    'Accept': 'application/vnd.github.everest-preview+json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {0}'.format(token)
}
url_runs = "{0}/actions/runs".format(base_url)
headersGet = {
    'Accept': 'application/vnd.github.everest-preview+json',
    'Authorization': 'Bearer {0}'.format(token)
}

logging.info('Dispatch helm update action')
logging.info(payload)
response = requests.request("POST", url_trigger, headers=headers, data=payload)
if response.status_code != 204:
    sys.exit(response.text)
time.sleep(3)

workflowId = ''
response = requests.request("GET", url_runs, headers=headersGet)
if response.reason == 'OK':
    json = json.loads(response.text)
    for node in json['workflow_runs']:
        if node['status'] != 'completed':
            break
    workflowId = node['id']
    url_run = node['url']
    logging.info("Found build with id {0}".format(workflowId))
    counter = 0
    while counter < wait_max_attempt:
        run = requests.request("GET", url_run, headers=headersGet)
        runJson = run.json()
        currentStatus = runJson['status']
        logging.info("Current run id: {0} has status: {1} ".format(runJson['id'], runJson['status']))
        conclusion = runJson['conclusion']
        run_number = runJson['run_number']
        if currentStatus == "completed":
            if conclusion != 'success':
                message = "Test Run number:{0} concluded with status:{1} with run has been finished".format(run_number, conclusion)
                logging.info("Test run url: {0}".format(runJson['html_url']))
                assert False, message
            else:
                logging.info("Run:{0} has been finished with conclusion:{1}".format(run_number, conclusion))
            break
        time.sleep(10)
        counter += 1
else:
    AssertionError("Failed to fetch run")
