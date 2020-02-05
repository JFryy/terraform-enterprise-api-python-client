import pyterprise

tfe_token = 'TOKENHERE'
client = pyterprise.Client()

# Supply your token as a parameter and the url for the terraform enterprise server.
# If you are not self hosting, use the one provided by hashicorp.
client.init(token=tfe_token, url='https://example-host.com')

org = client.set_organization(id='my-organization-name')

# Version Control options dictionary
vcs_options = {
    "identifier": "my-org/my-repo",
    "oauth-token-id": "ot-xxxxxxxxxxx",
    "branch": "master",
    "default-branch": False
}
print(
    org.create_workspace(name='test-delete-me2',
                         vcs_repo=vcs_options,
                         auto_apply=False,
                         queue_all_runs=False,
                         working_directory='/',
                         trigger_prefixes=['modules/']))
