import pyterprise

tfe_token = 'TOKENHERE'
client = pyterprise.Client()

# Supply your token as a parameter and the url for the terraform enterprise server.
# If you are not self hosting, use the one provided by hashicorp.
client.init(token=tfe_token, url='https://example-host.com')

org = client.set_organization(id='my-organization-name')
workspace = org.get_workspace('test')

# Create SSH Key
ssh_key = org.create_ssh_key(name='test2', key='Your RSA Private Key')

# Assign created SSH Key
workspace.assign_ssh_key(ssh_key_id=ssh_key.id)

# List SSH Keys in organization, get method is also available if you know the id.
for ssh_key in org.list_ssh_keys():
    print(ssh_key)

