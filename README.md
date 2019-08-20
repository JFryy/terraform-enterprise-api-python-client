## Pyterprise

This is a very simple Python Client Library for Terraform Enterprise with helper functions to abstract usage of the HTTP 
API and handle errors in a normalized fashion. 
The methods included in this library generally map 1 to 1 in terms of function naming conventions to 
[terraform enterprise documentation](https://www.terraform.io/docs/cloud/api/), so please review the available methods if you are uncertain on this library's usage.

### Installation:
This module can be installed via pip3, this library is compatible and can used be with python2 but is not available through PyPa for 2.7 versions.

`pip3 install --user pyterprise`

### Usage:

First import the module and authenticate using the init method, you can retrieve a token from the terraform enterprise UI.
```python
import pyterprise


tfe_token = 'TOKENHERE'
client = pyterprise.Client()

# Supply your token as a parameter and the url for the terraform enterprise server.
client.init(token=tfe_token, url='https://example-host.com')
```


Once initialized, you should be able to run various methods for accessing the API, most of the methods are basic python implementations 
of http requests that will simply return the json response content as a string.

Examples:
```python

# Get all most recent workspace statefiles to stdout.
workspaces = client.list_workspace_ids('awesome-organization')
for workspace in workspaces:
    print(client.get_workspace_current_statefile(workspace_id=workspace))

# Create a workspace.
client.create_workspace(organization='test-org', workspace_name='test-workspace')

# Update Workspace: Include any params to update, exclude any to not change.
update_params = {
    "name": "test-workspace",
    "terraform_version": "0.12.1",
    "working-directory": "test/awesome-directory",
    "vcs-repo": {
        "identifier": "github/Terraform-Testing",
        "branch": "test",
        "ingress-submodules": False,
        "oauth-token-id": "ot-XXXXXXXXX"
        }
    }
client.update_workspace(organization='test-org', update_params=update_params)


# Set a workspace environmental variable in a given workspace id.
client.create_workspace_variable('test-workspace', key='TF_LOG', value='DEBUG')

# Remove the created and modified workspace.
client.delete_workspace(organization='test-org', workspace_name='test-workspace')
```

Please consult module contents or [terraform enterprise api documentation](https://www.terraform.io/docs/cloud/api/) for
available methods most should be covered within this module and should have near identical function names compared to 
the REST documentation.


### API Coverage/Helper Methods

##### [Workspaces](https://www.terraform.io/docs/enterprise/api/workspaces.html)
- [x] list workspaces
- [x] create workspace
- [x] delete workspace
- [x] list workspace ids
- [x] get workspace non confirmed runs
- [x] get workspace current statefile
- [x] show workspace
- [x] update workspace

##### [Runs](https://www.terraform.io/docs/enterprise/api/run.html)
- [x] apply terraform run 
- [x] force execute run
- [x] run terraform workspace (destroy option included)
- [x] get workspace runs
- [x] discard run
- [x] cancel runs

##### [Teams](https://www.terraform.io/docs/enterprise/api/teams.html)
- [x] show user
- [x] get teams
- [x] create team
- [x] show team information
- [x] delete team

##### [Variables](https://www.terraform.io/docs/enterprise/api/variables.html)
- [x] create workspace variable
- [x] list variables
- [x] delete workspace variable

##### Other
- [x] get terraform plan
- [x] list organizations
- [x] show organization
- [x] update organization
- [x] destroy organization
- [x] create organization

### Contributions
Contributions are extremely appreciated! Please feel free to do so to improve this client library. I created this library
as at the time there was not a simple python library for performing basic administrative tasks in Terraform Enterprise.

*Disclaimer*: *This Client Library is considered in an 'alpha' state at this time as unit-testing is yet to be implemented. Please use at your own risk*
