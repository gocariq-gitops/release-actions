#!/usr/bin/python3
import json
import os
import requests


def trigger_workflow(auth_token, git_sha, repo_name, env):
    dispatch_url = "https://api.github.com/repos/gocariq/devops/actions/workflows/devDeployer.yaml/dispatches"
    print(dispatch_url)
    payload = json.dumps({
        "ref": "main",
        "inputs": {
            "gitSha": "{}".format(git_sha),
            "gitRepo": "{}".format(repo_name),
            "envName": "{}".format(env)
        }
    })
    headers = {
        'Accept': 'application/vnd.github.everest-preview+json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(auth_token)
    }
    response = requests.request("POST", dispatch_url, headers=headers, data=payload)
    assert response.status_code == 204, "Failed to trigger workflow\n Response code {}\n Error: {}".format(response.status_code, response.json())


def main():
    auth_token = os.environ['INPUT_TOKEN']
    repo_name = os.environ['INPUT_REPONAME'].replace(" ", "").lower()
    print("Requested Repo name: {}".format(repo_name))
    git_sha = os.environ['INPUT_GITSHA'].replace(" ", "").lower()
    print("Requested Git Sha: {}".format(git_sha))
    env = os.environ['INPUT_ENVNAME'].replace(" ", "").lower()
    print("Requested Env name: {}".format(env))
    trigger_workflow(auth_token, git_sha, repo_name, env)


if __name__ == '__main__':
    main()
