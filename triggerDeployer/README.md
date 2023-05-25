# action-trigger-test-wait

## Inputs
### token
**Required** - Token of user that will create issue
### repoName
**Required** - GitHub repo name
### gitSha
**Required** - GitSha

## Usages
```yaml
- uses: psingh-cariq/customActions/triggerDeployer@main
  name: Trigger deploy to dev env
  with:
    token: yourToken
    repoName: repo name
    gitSha: git sha to be deployed
    envName: name of env
```
