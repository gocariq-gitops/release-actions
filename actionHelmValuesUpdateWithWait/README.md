# action-trigger-test-wait

## Inputs
### token
**Required** - Token of user that will create issue
### branch
**Required** - branch name where build should be triggered, main is default value
### appName
**Required** - appliation name for which tag shoul be changed


## Usages
```yaml
- uses: psingh-cariq/customActions/helmValuesUpdateWithWait@main
  name: Trigger deploy and wait
  with:
    authToken: ${{secrets.GH_AUTH_TOKEN}}
    deployEnv: branch name which match deploy env
    tag: gitsha to be deployed
```
