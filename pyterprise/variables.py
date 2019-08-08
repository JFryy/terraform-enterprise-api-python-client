from json import load, loads
import requests

class Variables():
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
