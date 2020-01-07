import time
from .exceptions import APIException
from ._api_response_object import object_helper, collections
from .run import Run
from .variable import Variable


class Workspace(object):

    def __init__(self, workspace, organization_name, api_handler):
        self._api_handler = api_handler
        self.id = workspace.id
        self.organization_name = organization_name

        relationships = workspace.relationships
        self.current_run = relationships.current_run
        self.latest_run = relationships.latest_run
        self.current_state_version = relationships.current_state_version

        attributes = workspace.attributes
        self.name = attributes.name
        self.auto_apply = attributes.auto_apply
        self.created_at = attributes.created_at
        self.environment = attributes.environment
        self.locked = attributes.locked
        self.queue_all_runs = attributes.queue_all_runs
        self.terraform_version = attributes.terraform_version
        self.working_directory = attributes.working_directory
        self.speculative_enabled = attributes.speculative_enabled
        self.latest_change_at = attributes.latest_change_at
        self.operations = attributes.operations
        self.vcs_repo = attributes.vcs_repo
        self.permissions = attributes.permissions
        self.actions = attributes.actions
        self.description = attributes.description
        self.file_triggers_enabled = attributes.file_triggers_enabled
        self.trigger_prefixes = attributes.trigger_prefixes
        self.source = attributes.source
        self.source_name = attributes.source_name
        self.source_url = attributes.source_url
        self.links = workspace.links

    def __str__(self):
        return str(self.__dict__)

    def run(self, message='Ran from Terraform API', destroy_flag=False):
        """ Applies a run in an instantiated workspace. Can optionally destroy. """
        payload = {
            "data": {
                "attributes": {
                    "is-destroy": destroy_flag,
                    "message": message
                },
                "type": "runs",
                "relationships": {
                    "workspace": {
                        "data": {
                            "type": "workspaces",
                            "id": self.id
                        }
                    }
                }
            }
        }
        response = self._api_handler.call(method='post',
                                          uri='runs',
                                          json=payload).data
        return Run(object_helper(response), self._api_handler)

    def plan_apply(self, message, destroy_flag=False, timeout=120):
        """ Prints Plan and Apply output of Workspace, if stuck in queue will eventually timeout. """
        counter = 0
        run = self.run(message, destroy_flag)
        while run.status == 'pending':
            if counter > 15:
                print('Plan queue timeout.')
                return
            run = self.get_run(run.id)
            counter += 5
            time.sleep(5)

        counter = 0
        while run.status != 'planned' and counter < timeout:
            time.sleep(10)
            counter += 10
            run = self.get_run(run_id=run.id)
            if run.status == 'planned_and_finished':
                print('No changes detected.')
                return
        print(run.get_plan_output())

        print(f'Applying run: {self.id}: {run.id}')
        run.apply()
        run = self.get_run(run.id)
        while run.status == 'applying':
            time.sleep(5)
            run = self.get_run(run_id=run.id)
        print('Run Completed.')
        return

    def delete(self):
        """ Remove instantiated workspace. Returns response json. """
        return self._api_handler.call(
            method='delete',
            uri=f'organizations/{self.organization_name}/workspaces/{self.name}'
        )

    def update(self,
               name=None,
               tf_version=None,
               working_directory=None,
               auto_apply=None,
               queue_all_runs=None,
               vcs_repo=None,
               trigger_prefixes=None):
        """ Updates workspace. Uses instantiated defaults to populate payload with non-supplied values. """
        defaults = {
            'name': self.name,
            'tf_version': self.terraform_version,
            'working_directory': self.working_directory,
            'auto_apply': self.auto_apply,
            'queue_all_runs': self.queue_all_runs,
            'vcs_repo': self.vcs_repo,
            'trigger_prefixes': self.trigger_prefixes
        }

        arguments = locals()
        del arguments['self']

        for arg, value in arguments.items():
            if value != None:
                defaults[arg] = value
        payload = {
            "data": {
                "attributes": {
                    "name": defaults['name'],
                    "terraform_version": defaults['tf_version'],
                    "working-directory": defaults['working_directory'],
                    "auto-apply": defaults['auto_apply'],
                    "queue-all-runs": defaults['queue_all_runs'],
                    "trigger-prefixes": defaults['trigger_prefixes'],
                    "vcs-repo": defaults['vcs_repo']
                },
                "type": "workspaces"
            }
        }
        return self._api_handler.call(
            uri=f'organizations/{self.organization_name}/workspaces/{self.name}',
            method='patch',
            json=payload).data

    def lock(self, reason=""):
        """ Lock workspace. Returns reponse json. """
        payload = {"reason": reason}
        return self._api_handler.call(uri=f'workspaces/{self.id}/actions/lock',
                                      method='post',
                                      json=payload).data

    def unlock(self, reason=""):
        """ Unlocks workspace. Returns response json. """
        payload = {"reason": reason}
        return self._api_handler.call(
            uri=f'workspaces/{self.id}/actions/unlock',
            method='post',
            json=payload).data

    def force_unlock(self, reason):
        payload = {"reason": reason}
        return \
            self._api_handler.call(uri=f'workspaces/{self.id}/actions/force-unlock', method='post', json=payload).data

    def assign_ssh_key(self, ssh_key_id=''):
        """ Assigns ssh key requires ssh-key id found from the ssh-key endpoint. Returns response json. """
        payload = {
            "data": {
                "attributes": {
                    "id": ssh_key_id
                },
                "type": "workspaces"
            }
        }
        return \
            self._api_handler.call(uri=f'workspaces/{self.id}/relationships/ssh-key', method='patch', json=payload).data

    def unassign_ssh_key(self):
        """ Unassigns the ssh key currently assigned to the workspace. """
        payload = {"data": {"attributes": {"id": None}, "type": "workspaces"}}
        return \
            self._api_handler.call(uri=f'workspaces/{self.id}/relationships/ssh-key', method='patch', json=payload).data

    def get_current_state_version(self):
        """ Gets current statefile for a workspace, returns None if none found. """
        try:
            return object_helper(
                self._api_handler.call(
                    uri=f'workspaces/{self.id}/current-state-version').data)
        except APIException:
            return None

    # Create a class for handling variables with an update and delete method included instead of using workspace class.
    def list_variables(self):
        """ Returns list of variable objects for workspace for modification. """
        variables = []
        params = {
            "filter[workspace][name]": self.name,
            "filter[organization][name]": self.organization_name
        }
        response = self._api_handler.call(uri=f'vars', params=params).data
        for variable in response:
            variables.append(
                Variable(object_helper(variable), self._api_handler))
        return variables

    def create_variable(self,
                        key,
                        value,
                        category="env",
                        hcl=False,
                        sensitive=False,
                        description=""):
        """ Create a new variable in a workspace. """
        payload = {
            "data": {
                "type": "vars",
                "attributes": {
                    "key": key,
                    "value": value,
                    "description": description,
                    "category": category,
                    "hcl": hcl,
                    "sensitive": sensitive
                },
                "relationships": {
                    "workspace": {
                        "data": {
                            "id": self.id,
                            "type": "workspaces"
                        }
                    }
                }
            }
        }
        return self._api_handler.call(uri=f'vars', method='post',
                                      json=payload).data

    def get_run(self, run_id):
        run = self._api_handler.call(uri=f'/runs/{run_id}').data
        return Run(run=object_helper(run), api_handler=self._api_handler)

    def list_runs(self):
        runs = []
        response = self._api_handler.call(uri=f'workspaces/{self.id}/runs').data
        for run in response:
            runs.append(
                Run(run=object_helper(run), api_handler=self._api_handler))
        return runs
