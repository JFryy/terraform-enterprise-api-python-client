from ._api_response_object import object_helper
from .workspace import Workspace
from .ssh_key import SSHKey


class Organization(object):
    """ Organization class instaniated with api response attributes for organizations. """

    def __init__(self, organization, api_handler):
        self._api_handler = api_handler

        organization = organization.attributes
        self.name = organization.name
        self.external_id = organization.external_id
        self.created_at = organization.created_at
        self.email = organization.email
        self.session_timeout = organization.session_timeout
        self.session_remember = organization.session_remember
        self.collaborator_auth_policy = organization.collaborator_auth_policy
        self.enterprise_plan = organization.enterprise_plan
        self.plan_expired = organization.plan_expired
        self.cost_estimation_enabled = organization.cost_estimation_enabled
        self.permissions = organization.permissions
        self.fair_run_queuing_enabled = organization.fair_run_queuing_enabled
        self.saml_enabled = organization.saml_enabled
        self.two_factor_conformant = organization.two_factor_conformant
        self.preview_request = organization.preview_request

    def __str__(self):
        return str(self.__dict__)

    def list_workspaces(self):
        """
        Returns list of all workspace objects in the provided organization.
        If data response is empty (empty page) stop making queries.
        """
        workspaces = []
        params = {"page[size]": 100, "page[number]": 1}
        while True:
            response = self._api_handler.call(
                uri=f'organizations/{self.name}/workspaces', params=params)
            if not response.data:
                break
            for workspace in response.data:
                workspaces.append(
                    Workspace(workspace=object_helper(workspace),
                              organization_name=self.name,
                              api_handler=self._api_handler))
            params["page[number]"] += 1
        return workspaces

    def search_workspaces(self, keyword):
        """ Get workspace objects by substring of name. """
        workspaces = []
        for workspace in self.list_workspaces():
            if keyword.lower() in workspace.name.lower():
                workspaces.append(workspace)
        return workspaces

    def create_workspace(self,
                         name,
                         tf_version=None,
                         working_directory="",
                         auto_apply=False,
                         queue_all_runs=False,
                         vcs_repo=None,
                         trigger_prefixes=[]):
        """
        Creates workspace, must pass vcs payload as dictionary. Returns response json. Example vcs-repo payload:
        {
            "identifier": "skierkowski/terraform-test-proj",
            "oauth-token-id": "ot-hmAyP66qk2AMVdbJ",
            "branch": "",
            "default-branch": True
        }

        """
        payload = {
            "data": {
                "attributes": {
                    "name": name,
                    "terraform_version": tf_version,
                    "working-directory": working_directory,
                    "auto-apply": auto_apply,
                    "queue-all-runs": queue_all_runs,
                    "trigger-prefixes": trigger_prefixes,
                    "vcs-repo": vcs_repo
                },
                "type": "workspaces"
            }
        }
        return self._api_handler.call(
            uri=f'organizations/{self.name}/workspaces',
            method='post',
            json=payload).data

    def delete_workspace(self, name):
        """ Delete a workspace by name within the organization. """
        return self._api_handler.call(
            method='delete', uri=f'organizations/{self.name}/workspaces/{name}')

    def get_workspace(self, name):
        """ Referred to as show workspace in official documentation, returns a single workspace object. """
        response = self._api_handler.call(
            uri=f'organizations/{self.name}/workspaces/{name}')
        return Workspace(workspace=object_helper(response.data),
                         organization_name=self.name,
                         api_handler=self._api_handler)

    def list_ssh_keys(self):
        """ List all SSH Keys in a given account. """
        ssh_keys = []
        response = self._api_handler.call(
            uri=f'organizations/{self.name}/ssh-keys')
        for ssh_key in response.data:
            ssh_keys.append(SSHKey(object_helper(ssh_key), self._api_handler))
        return ssh_keys

    def create_ssh_key(self, name, key):
        """ Create an ssh key, requires the string of the private key. """
        payload = {
            "data": {
                "type": "ssh-keys",
                "attributes": {
                    "name": name,
                    "value": key
                }
            }
        }
        response = self._api_handler.call(
            method='post',
            uri=f'organizations/{self.name}/ssh-keys',
            json=payload).data
        return SSHKey(ssh_key=object_helper(response),
                      api_handler=self._api_handler)
