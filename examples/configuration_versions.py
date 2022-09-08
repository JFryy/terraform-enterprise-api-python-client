import pyterprise

tfe_token = 'TOKENHERE'
client = pyterprise.Client()

# Supply your token as a parameter and the url for the terraform enterprise server.
# If you are not self hosting, use the one provided by hashicorp.
client.init(token=tfe_token, url='https://example-host.com')

org = client.set_organization(id='my-organization-name')
workspace = org.get_workspace('my-test-workspace')

# Get all configuration versions for this workspace
print(workspace.configuration_versions())

# Create a new configuration version
config = workspace.create_configuration_version(
    auto_queue_runs=True,
    speculative=True
)

print(config)

# Get a specific configuration version
print(client.get_configuration_version('cv-Y4aZPkaR7Yr6PwUb'))