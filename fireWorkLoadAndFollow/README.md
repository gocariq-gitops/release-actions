# action-trigger-test-wait

## Inputs
### token
**Required** - Token of user that will create issue
### targetEnv
**Required** - env where test needs to be targeted
### workFlowFileName
**Required** - Name of the yaml file which needs to be triggered
### tag
**Required** - Git tag under the test


## Usages
```yaml
        uses: gocariq-gitops/release-actions/fireWorkLoadAndFollow@main
        with:
          authToken: ${{secrets.GHA_DEVOPS_DISPATCH}}
          targetEnv: ${{ steps.branch-name.outputs.current_branch }}
          tag: ${{ env.SHORT_SHA }}
          workFlowFileName: core-service-test
```
