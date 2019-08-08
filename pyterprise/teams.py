from json import load, loads
import requests

#TODO: Add team_add_user_method
class Teams():
    def show_user(self, user_id):
        url = self.url + 'users/{}'.format(user_id)
        return self._tfe_api_get(url)

    def get_teams(self, organization_name):
        url = self.url + 'organizations/{}/teams'.format(organization_name)
        return self._tfe_api_get(url)


    def create_team(self, organization, name):
        url = self.url + 'organizations/{}/teams'.format(organization)
        payload = {
            "data": {
                "type": "teams",
                "attributes": {
                    "name": name,
                    "organization-access": {
                        "manage-workspaces": True
                    }
                }
            }
        }
        response = requests.post(url=url, json=payload, headers=self.headers)
        self._error_handler(response)
        return response.content



    def show_team_information(self, team_id):
        url = self.url + 'teams/{}'.format(team_id)
        return self._tfe_api_get(url)


    def delete_team(self, team_id):
        url = self.url + 'teams/{}'.format(team_id)
        response = requests.delete(url)
        self._error_handler(response)
        return response.content
