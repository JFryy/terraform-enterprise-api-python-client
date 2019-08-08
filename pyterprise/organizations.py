import requests
import json

class Organziations():
    def list_organizations(self):
        url = self.url + 'organizations'
        return self._tfe_api_get(url)

    def show_organization(self, organization):
        url = self.url + 'organizations/{}'.format(organization)
        return self._tfe_api_get(url)

    def update_organization(self, organization_name, email):
        url = self.url + 'organizations/{}'.format(organization_name)
        payload = {
            "data": {
                "type": "organizations",
                "attributes": {
                    "name": "hashicorp",
                    "email": email
                }
            }
        }
        response = requests.patch(url=url, json=payload, headers=self.headers)
        self._error_handler(response)
        return response.content

    def destroy_organization(self, organization_name):
        url = self.url + 'organizations/{}'.format(organization_name)
        response = requests.delete(url)
        self._error_handler(response)
        return response.content

    def create_organization(self, organization_name, email):
        url = self.url + 'organizations'
        payload = {
            "data": {
                "type": organization_name,
                "attributes": {
                    "name": "hashicorp",
                    "email": email
                }
            }
        }
        response = requests.post(url=url, json=payload, headers=self.headers)
        self._error_handler(response)
        return response.content
