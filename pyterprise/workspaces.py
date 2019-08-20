from json import loads
import requests


class Workspaces():
    def list_workspaces(self, organization):
        url = self.url + 'organizations/{}/workspaces'.format(organization)
        return self._get_handler(url)

    def create_workspace(self, organization, workspace_name):
        url = self.url + 'organizations/{}/workspaces'.format(organization)
        payload = {
            "data": {
                "attributes": {
                    "name": workspace_name
                },
                "type": "workspaces"
            }
        }
        return self._post_handler(url=url, json=payload)

    def delete_workspace(self, organization, workspace_name):
        url = self.url + 'organizations/{}/workspaces/{}'.format(organization, workspace_name)
        return self._delete_handler(url)

    def list_workspace_ids(self, organization):
        return [str(workspaces["id"]) for workspaces in loads
                (self.list_workspaces(organization))["data"]]

    def get_workspace_non_confirmed_runs(self, workspace_id):
        return [runs for runs in loads(self.get_workspace_runs(workspace_id))["data"] if
                runs["attributes"]["actions"]["is-confirmable"]]

    def get_workspace_current_state_version(self, workspace_id):
        url = self.url + 'workspaces/{}/current-state-version'.format(workspace_id)
        return self._get_handler(url)

    def get_workspace_current_statefile(self, workspace_id):
        try:
            url = loads(
                self.get_workspace_current_state_version(workspace_id)
            )["data"]["attributes"]["hosted-state-download-url"]
        except KeyError:
            return
        return requests.get(url=url).content

    def show_workspace(self, organization, workspace_name):
        url = self.url + 'organizations/{}/workspaces/{}'.format(organization, workspace_name)
        return self._get_handler(url)

    def update_workspace(self, update_params, organization):
        """
        :param organization: Organization of workspace
        :param update_params: Parameters to update, omit fields to not alter them. i.e.
        {
        "name": "test-workspace",
        "terraform_version": "0.12.1",
        "working-directory": "test/awesome-directory",
        "vcs-repo": {
            "identifier": "github/Terraform-Testing",
            "branch": "test",
            "ingress-submodules": False,
            "oauth-token-id": "ot-XXXXXXXXX"
            }
        }
        """
        url = self.url + 'organizations/{}/workspaces/{}'.format(organization, update_params["name"])
        payload = {
            "data": {
                "attributes": update_params,
                "type": "workspaces"
            }
        }
        return self._patch_handler(url=url, json=payload)
