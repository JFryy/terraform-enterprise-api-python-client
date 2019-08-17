import requests


class Variables():
    #TODO: Fallback to updating the workspace if this fails due to pre-existing variable
    def create_workspace_variable(self, workspace_id, key, value, category='terraform', hcl=False, sensitive=False):
        url = self.url + 'vars'
        payload = {
            "data": {
                "type": "vars",
                "attributes": {
                    "key": key,
                    "value": value,
                    "category": category,
                    "hcl": hcl,
                    "sensitive": sensitive
                },
                "relationships": {
                    "workspace": {
                        "data": {
                            "id": workspace_id,
                            "type": "workspaces"
                        }
                    }
                }
            }
        }
        response = requests.post(url, json=payload, headers=self.headers)
        self._error_handler(response)
        return response.content

    def list_variables(self, organization, workspace):
        url = self.url + 'vars?filter%5Borganization%5D%5Bname%5D={}&filter%5Bworkspace%5D%5Bname%5D={}'\
            .format(organization, workspace)
        return self._tfe_api_get(url)

    def delete_workspace_variable(self, variable_id):
        url = self.url + '/vars/{}'.format(variable_id)
        response = requests.delete(url)
        self._error_handler(response)
        return response
