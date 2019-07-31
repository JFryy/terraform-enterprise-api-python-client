class Calls():
    def run_terraform_workspace(self, workspace_id, message):
        url = self.url + 'runs'
        with open(self.payloads_dir + 'tf-run.json') as payload:
            payload = load(payload)
            payload["data"]["relationships"]["workspace"]["data"]["id"] = str(workspace_id)
            payload["data"]["attributes"]["message"] = str(message)

        response = requests.post(url=url, json=payload, headers=self.headers)
        self._error_handler(response)
        return response.content

    def apply_terraform_run(self, run_id, message="This action was performed via the rest API."):
        url = self.url + 'runs/{}/actions/apply'.format(run_id)
        payload = {
            "comment": message
        }
        response = requests.post(url=url, json=payload, headers=self.headers)
        self._error_handler(response)
        return response.content

    def create_workspace(self, organization, workspace_name):
        url = self.url + 'organizations/{}/workspaces'.format(organization)
        with open(self.payloads_dir + 'create-workspace.json') as payload:
            payload = load(payload)
            payload["data"]["attributes"]["name"] = workspace_name
        response = requests.post(url=url, json=payload, headers=self.headers)
        self._error_handler(response)
        return response.content

    def delete_workspace(self, organization, workspace_name):
        url = self.url + 'organizations/{}/workspaces/{}'.format(organization, workspace_name)
        response = requests.delete(url=url)
        self._error_handler(response)
        return response.content

    def list_workspaces(self, organization):
        url = self.url + 'organizations/{}/workspaces'.format(organization)
        return self._tfe_api_get(url)

    def list_workspace_ids(self, organization):
        return [str(workspaces["id"]) for workspaces in loads(self.list_workspaces(organization))["data"]]

    def get_workspace_runs(self, workspace_id):
        url = self.url + 'workspaces/{}/runs'.format(workspace_id)
        return self._tfe_api_get(url)

    def get_workspace_non_confirmed_runs(self, workspace_id):
        return [runs for runs in loads(self.get_workspace_runs(workspace_id))["data"] if
                runs["attributes"]["actions"]["is-confirmable"]]

    def get_terraform_plan(self, plan_id):
        url = self.url + 'plans/{}'.format(plan_id)
        return self._tfe_api_get(url)

    def get_workspace_current_state_version(self, workspace_id):
        url = self.url + 'workspaces/{}/current-state-version'.format(workspace_id)
        return self._tfe_api_get(url)

    def get_workspace_current_statefile(self, workspace_id):
        url = loads(
            self.get_workspace_current_state_version(workspace_id)
        )["data"]["attributes"]["hosted-state-download-url"]
        return requests.get(url=url).content

    def show_workspace(self, organization, workspace_name):
        url = self.url + 'organizations/{}/workspaces/{}'.format(organization, workspace_name)
        return self._tfe_api_get(url)

    def show_user(self, user_id):
        url = self.url + 'users/{}'.format(user_id)
        return self._tfe_api_get(url)
