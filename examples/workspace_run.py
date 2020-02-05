import pyterprise

tfe_token = 'TOKENHERE'
client = pyterprise.Client()

# Supply your token as a parameter and the url for the terraform enterprise server.
# If you are not self hosting, use the one provided by hashicorp.
client.init(token=tfe_token, url='https://example-host.com')

org = client.set_organization(id='my-organization-name')
workspace = org.get_workspace('my-test-workspace')

# Create and apply a run in a workspace without auto-apply settings. Logs terraform plan/apply output in console.
workspace.plan_apply(message='just testing.', destroy_flag=False)

# Basic terraform run, easy use on auto-apply workspaces. Enable destroy flag for destruction (Default is False.)
run = workspace.run(destroy_flag=False)

# Get terraform plan output of run.
print(run.get_plan_output())

# If plan output looks ok in run lets apply it
print(run.apply('Plan output look OK.'))

# List general run data, you can apply, cancel and perform other methods on specific runs with the instantiated run object.
for run in workspace.list_runs(page=1, page_size=100):
    print(run)
    print(run.id, run.status, run.status_timestamps)
