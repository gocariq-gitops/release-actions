# action-trigger-test-wait

## Inputs
### user
**Required** - GitHub user
### token
**Required** - Token of user that will create issue
### repo
**Required** - GitHub repo name
### workflow
**Required** - Name of workflow file without extension
### branch
**Required** - branch name where build should be triggered, main is default value
### cariq-docker-repo
**Required** - CarIq Docker repository

## Usages
```yaml
- uses: psingh-cariq/customActions/k8sAppDeploy@main
  name: Trigger deploy and wait
  with:
    user: user
    token: ${{secrets.GH_AUTH_TOKEN}}
    repo: repo name
    workflow: name of the yaml file 
    branch: brancNamedocker_repo
    cariqDockerRepo: name of your doker repository
    gitSha: gitsha to be deployed
```
