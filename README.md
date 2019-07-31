### Pyterprise

This is a small Python client library for Terraform Enterprise with helper functions to abstract usage of the HTTP API - this is a work in progress 
and likely not all functionality of the API has (or will) be ported over - but most common uses will attempted to be covered here.

The methods used are straightforward and relatively self documenting so I won't have too much uses covered here.

#### Installation:

This module is available publicly and can be downloaded simply using pip3:

`pip3 install --user pyterprise`

#### Usage:

First import the module and authenticate using the init method, you can retrieve a token from the terraform enterprise UI.
```python
import pyterprise


tfe_token = 'TOKENHERE'
client = pyterprise.TerraformAPI()

# Supply your token as a parameter and the url for the terraform enterprise server.
client.init(token=tfe_token, url='Endpoint for TFE')
```


Once initialized, you should be able to run various methods for accessing the API, most of the methods are basic python implementations 
of http requests that will simply return the json response content as a string. Here is some example usage that you can combine with the authentication example below:

```python
# returns a list of all workspace IDs for a given organization
client.list_workspace_ids(organization='<org-name>')

# returns the most current statefile of a given workspace
client.get_workspace_current_statefile(workspace_id='example')

# run the terraform in a given workspace
client.run_terraform_workspace(workspace_id='<workspace id>', message='test of api client')

# get terraform plan information for a given workspace
client.get_terraform_plan(plan_id='test_id')

```


Please read the main code here for more methods to use for the API.

