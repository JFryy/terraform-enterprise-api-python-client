import pyterprise

tfe_token = 'TOKENHERE'
client = pyterprise.Client()

# Supply your token as a parameter and the url for the terraform enterprise server.
# If you are not self hosting, use the one provided by hashicorp.
client.init(token=tfe_token, url='https://example-host.com')

org = client.set_organization(id='my-organization-name')
workspace = org.get_workspace(name='test')

# Create a variable
print(workspace.create_variable(key='foo', value='bar', sensitive=False, category='env'))

# Get variables for a workspace
variables = workspace.list_variables()

# Update a variable.
for variable in variables:
    if variable.key == 'foo':
        print(variable.update(value='baz'))


# Delete the variable we created.
for variable in variables:
    if variable.key == 'foo':
        variable.delete()
