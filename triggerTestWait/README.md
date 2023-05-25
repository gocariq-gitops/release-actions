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
### group
**Required** - Test group which needs to be triggered
### env
**Required** - Target test env such as dev,int,staging, whatever

## Usages
```yaml
- uses: alexgocariq/action-trigger-test-wait@v1.1
  name: Trigger job and wait
  with:
    user: alexgocariq
    token: ${{secrets.GH_AUTH_TOKEN}}
    repo: actions-play
    workflow: pr_build
    branch: main
    group: smoke
    env: test
```
