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

Example:
```python

# Get all most recent workspace statefiles to stdout.
workspaces = client.list_workspace_ids('awesome-organization')
for workspace in workspaces:
    print(client.get_workspace_current_statefile(workspace_id=workspace))

# Deleting and creating workspaces.
client.create_workspace(organization='test-org', workspace_name='test-workspace')
client.delete_workspace(organization='test-org', workspace_name='test-workspace')

# Set a workspace environmental variable in a given workspace id.
client.create_workspace_variable('test-workspace', key='TF_LOG', value='DEBUG')
```

Please consult module contents or [terraform enterprise api documentation](https://www.terraform.io/docs/cloud/api/) for
available methods most should be covered within this module and should have near identical function names compared to 
the REST documentation.

### Contributions
Contributions are extremely appreciated! Please feel free to do so to improve this client library. I originally created this library
because it seemed there weren't any recent community client libraries for Python for the Terraform Enterprise REST API.
As of writing this I am still actively working on this library to include the remaining API methods and include unit testing.
