#!/usr/bin/python3
import os
import sys
import time
import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
token = os.environ['INPUT_TOKEN']
user = os.environ['INPUT_USER']
repo = os.environ['INPUT_REPO']
workflow = os.environ['INPUT_WORKFLOW']
gitSha = os.environ['INPUT_GITSHA']
branch = os.environ['INPUT_BRANCH']
cariqDockerRepo = os.environ['INPUT_CARIQ_DOCKER_REPO']
wait_max_attempt = 60
url_trigger = "https://api.github.com/repos/{0}/{1}/actions/workflows/{2}.yaml/dispatches".format(user, repo, workflow)
payload = json.dumps({
    "ref": "{0}".format(branch),
    "inputs": {
        "gitSha": "{0}".format(gitSha),
        "cariq-docker-repo": "{0}".format(cariqDockerRepo),
    }
})
headers = {
    'Accept': 'application/vnd.github.everest-preview+json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {0}'.format(token)
}
url_dispatch = "https://api.github.com/repos/{0}/{1}/actions/runs".format(user, repo)
headersGet = {
    'Accept': 'application/vnd.github.everest-preview+json',
    'Authorization': 'Bearer {0}'.format(token)
}

logging.info('Dispatch deploy action')
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
    while counter < wait_max_attempt:
        url = "https://api.github.com/repos/{0}/{1}/actions/runs/{2}".format(user, repo, node['id'])
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
        time.sleep(15)
        counter += 1
else:
    AssertionError("Failed to fetch run")
