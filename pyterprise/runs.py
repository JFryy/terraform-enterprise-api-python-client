import requests


class Runs():
    def apply_terraform_run(self, run_id, message="This action was performed via the rest API."):
        url = self.url + 'runs/{}/actions/apply'.format(run_id)
        payload = {
            "comment": message
        }
        return self._post_handler(url=url, json=payload)

    def force_execute_run(self, run_id):
        url = self.url + 'runs/{}/actions/force-execute'.format(run_id)
        response = requests.post(url=url, headers=self.headers)
        self._error_handler(response)
        return response

    def run_terraform_workspace(self, workspace_id, message, destroy=False):
        url = self.url + 'runs'
        payload = {
            "data": {
                "attributes": {
                    "is-destroy": destroy,
                    "message": message
                },
                "type": "runs",
                "relationships": {
                    "workspace": {
                        "data": {
                            "type": "workspaces",
                            "id": workspace_id
                        }
                    }
                }
            }
        }

        return self._post_handler(url=url, json=payload)

    def get_workspace_runs(self, workspace_id):
        url = self.url + 'workspaces/{}/runs'.format(workspace_id)
        return self._tfe_api_get(url)

    def discard_run(self, run_id, comment):
        url = self.url + '/runs/{}/actions/discard'.format(run_id)
        payload = {
            "comment": comment
        }
        return self._post_handler(url=url, json=payload)

    def cancel_run(self, run_id, comment, force_cancel=False):
        cancel = 'cancel'
        if force_cancel:
            cancel = 'force-cancel'
        url = self.url + 'runs/{}/actions/{}'.format(run_id, cancel)
        payload = {
            "comment": comment
        }
        return self._post_handler(url=url, json=payload)
