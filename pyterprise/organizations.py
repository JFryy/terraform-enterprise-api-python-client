import requests


class Organziations():
    def list_organizations(self):
        url = self.url + 'organizations'
        return self._get_handler(url)

    def show_organization(self, organization):
        url = self.url + 'organizations/{}'.format(organization)
        return self._get_handler(url)

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
        return self._patch_handler(url=url, json=payload)

    def destroy_organization(self, organization_name):
        url = self.url + 'organizations/{}'.format(organization_name)
        return self._delete_handler(url)


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
        return self._post_handler(url=url, json=payload)

