# Release Actions

This repository contains code for build and deployment, 
but it can be used just from other repositories, ex: microservice.

## How To Onboard Microservice to CICDv2

### Build and deploy to TEST envs

1. Move your old CICD files to the folder deprecated/.github/workflows
2. Copy files from the current repository from `docs/examples/user-service/` 
   to the directory `.github/workflows` in your repository.
3. Update required settings

[More information](https://cariq.atlassian.net/wiki/spaces/INFRA/pages/1780777011/How+to+implement+a+Workflow+V2)

### Deploy to PROD

Add your service to the [release.yaml](https://github.com/gocariq/release-manifest/blob/main/release.yaml) file in 
the [release-manifest](https://github.com/gocariq/release-manifest) repository.

[More information](https://github.com/gocariq/release-manifest)
