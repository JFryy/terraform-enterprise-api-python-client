from json import load, loads
import requests

class Runs():
    def apply_terraform_run(self, run_id, message="This action was performed via the rest API."):
        url = self.url + 'runs/{}/actions/apply'.format(run_id)
        payload = {
            "comment": message
        }
        response = requests.post(url=url, json=payload, headers=self.headers)
        self._error_handler(response)
        return response.content

    def force_execute_run(self, run_id):
        url = self.url + 'runs/{}/actions/force-execute'.format(run_id)
        response = requests.post(url=url, headers=self.headers)
        self._error_handler(response)
        return response

    def run_terraform_workspace(self, workspace_id, message):
        url = self.url + 'runs'
        with open(self.payloads_dir + 'tf-run.json') as payload:
            payload = load(payload)
            payload["data"]["relationships"]["workspace"]["data"]["id"] = str(workspace_id)
            payload["data"]["attributes"]["message"] = str(message)

        response = requests.post(url=url, json=payload, headers=self.headers)
        self._error_handler(response)
        return response.content

    def get_workspace_runs(self, workspace_id):
        url = self.url + 'workspaces/{}/runs'.format(workspace_id)
        return self._tfe_api_get(url)

    def discard_run(self, run_id, comment):
        url = self.url + '/runs/{}/actions/discard'.format(run_id)
        payload = {
            "comment": comment
        }
        response = requests.post(url, json=payload, headers=self.headers)
        self._error_handler(response)
        return response

    def cancel_run(self, run_id, comment, force_cancel=False):
        cancel = 'cancel'
        if force_cancel:
            cancel = 'force-cancel'
        url = self.url + 'runs/{}/actions/{}'.format(run_id, cancel)
        payload = {
            "comment": comment
        }
        response = requests.post(url, json=payload, headers=self.headers)
        self._error_handler(response)
        return response

