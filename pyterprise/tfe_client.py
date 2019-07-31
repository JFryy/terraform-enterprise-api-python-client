import requests
import os
import logging as log
from .pyterprise_exceptions import UnauthorizedError, InternalServerError
from json import load, loads


class Client:
    log.basicConfig(
        level=log.WARN
    )

    def __init__(self):
        self.payloads_dir = os.path.dirname(os.path.realpath(__file__)) + '/payloads/'

    def init(self, token, url):
        self.token = token
        self.url = url
        self.headers = {
            'Content-Type': 'application/vnd.api+json',
            'Authorization': 'Bearer {}'.format(token)
        }

    def _tfe_api_get(self, url):
        response = requests.get(url=url, headers=self.headers)
        self._error_handler(response)
        return response.content

    def _error_handler(self, response):
        if response.status_code == 401 or response.status_code == 403:
            raise UnauthorizedError(
                message=response.content,
                errors=response.status_code
            )
        if response.status_code in range(500, 504):
            raise InternalServerError(
                message=response.content,
                errors=response.status_code
            )

        if response.status_code not in range(200, 202):
            log.error('{}: {}'.format(response.url, response.status_code))

    def run_terraform_workspace(self, workspace_id, message):
        url = self.url + '/api/v2/runs'
        with open(self.payloads_dir + 'tf-run.json') as payload:
            payload = load(payload)
            payload["data"]["relationships"]["workspace"]["data"]["id"] = str(workspace_id)
            payload["data"]["attributes"]["message"] = str(message)

        response = requests.post(url=url, json=payload, headers=self.headers)
        self._error_handler(response)
        return response.content

    def apply_terraform_run(self, run_id, message="This action was performed via the rest API."):
        url = self.url + '/api/v2/runs/{}/actions/apply'.format(run_id)
        payload = {
            "comment": message
        }
        response = requests.post(url=url, json=payload, headers=self.headers)
        self._error_handler(response)
        return response.content

    def list_workspaces(self, organization):
        url = self.url + '/api/v2/organizations/{}/workspaces'.format(organization)
        return self._tfe_api_get(url)

    def list_workspace_ids(self, organization):
        return [str(workspaces["id"]) for workspaces in loads(self.list_workspaces(organization))["data"]]

    def get_workspace_runs(self, workspace_id):
        url = self.url + '/api/v2/workspaces/{}/runs'.format(workspace_id)
        return self._tfe_api_get(url)

    def get_workspace_non_confirmed_runs(self, workspace_id):
        return [runs for runs in loads(self.get_workspace_runs(workspace_id))["data"] if
                runs["attributes"]["actions"]["is-confirmable"]]

    def get_terraform_plan(self, plan_id):
        url = self.url + '/api/v2/plans/{}'.format(plan_id)
        return self._tfe_api_get(url)

    def get_workspace_current_state_version(self, workspace_id):
        url = self.url + '/api/v2/workspaces/{}/current-state-version'.format(workspace_id)
        return self._tfe_api_get(url)

    def get_workspace_current_statefile(self, workspace_id):
        url = loads(
            self.get_workspace_current_state_version(workspace_id)
        )["data"]["attributes"]["hosted-state-download-url"]
        return requests.get(url=url).content
