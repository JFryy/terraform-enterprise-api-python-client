import pyterprise

tfe_token = 'TOKENHERE'
client = pyterprise.Client()

# Supply your token as a parameter and the url for the terraform enterprise server.
# If you are not self hosting, use the one provided by hashicorp.
client.init(token=tfe_token, url='https://example-host.com')

org = client.set_organization(id='my-organization-name')
workspaces = org.list_workspaces()

for workspace in workspaces:
    # Skip Workspaces with no statefiles.
    if not workspace.get_current_state_version():
        continue
    download_url = workspace.get_current_state_version(
    ).attributes.hosted_state_download_url
    print(download_url)
