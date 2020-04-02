# Newrelic Resource for Concourse
An output only opinionated concourse resource for adding deployment markers in newrelic

## Newrelic Deployment markers

Details of Deployment markers can be found [here](https://docs.newrelic.com/docs/apm/new-relic-apm/maintenance/record-deployments)

## Source Configuration

* `api_key`: *Required.* Rest API key for adding deployment markers to an application
* `user`: *Required.* This Username will appear in the deployments dashboard

## `out`: Add a deployment marker

In order to add an deployment marker, a revision number and a description may be provided to the newrelic API.
For this purpose provide a `git` resource in the put step so that NewRelic concourse resource
takes the revision  from `(SHA of origin/HEAD commit)` and description from `(Commit message of origin/HEAD commit)`.

* `git_src_directory`: *Required.* source code of the deployed version. Format is `/tmp/put/build/<<name of git resource>>`
* `api_url`: *Mandatory.* Deployment [REST api endpoint](https://rpm.newrelic.com/api/explore/application_deployments/create)  
* `app_id`: *Optional* (`deprecated` in favour of api_url) Application ID from NewRelic, if `api_url` is not provided this defaults 

## Example Pipeline

```yaml

resource_types:
- name: newrelic-deployment-marker
  type: docker-image
  source:
    repository: shyamz22/newrelic-resource
    tag: latest

resources:
- name: src
  type: git
  source:
    uri: git@github.com:shyamz-22/PactIt.git
    branch: master
    private_key: ((git-key))

- name: deployment-marker
  type: newrelic-deployment-marker
  source:
    api_key: ((newrelic-rest-api-key))
    user: concourse-user@email.com


jobs:

- name: deploy
  plan:
  - get: src # <-- 🤓 source code of deployed app
    trigger: true
  - task: deploy
    config:
      platform: linux
      image_resource:
        type: docker-image
        source:
          repository: alpine
      inputs:
      - name: src
      run:
        path: sh
        args:
        - -exc
        - |
          export TERM=dumb
          set -x

          # deploy
          echo "deployment-successful"
  on_success:
    put: deployment-marker
    params:
      git_src_directory: /tmp/build/put/src # <-- 🤓
      api_url: https://api.newrelic.com/v2/applications/((app-id))/deployments.json

```



