class Teams():
    def show_user(self, user_id):
        url = self.url + 'users/{}'.format(user_id)
        return self._get_handler(url)

    def get_teams(self, organization_name):
        url = self.url + 'organizations/{}/teams'.format(organization_name)
        return self._get_handler(url)

    def create_team(self, organization, name, is_managed_workspace=True):
        url = self.url + 'organizations/{}/teams'.format(organization)
        payload = {
            "data": {
                "type": "teams",
                "attributes": {
                    "name": name,
                    "organization-access": {
                        "manage-workspaces": is_managed_workspace
                    }
                }
            }
        }
        return self._post_handler(url, json=payload)

    def show_team_information(self, team_id):
        """
        Returns information on a given team id.
        :param team_id: String of team ID.
        """
        url = self.url + 'teams/{}'.format(team_id)
        return self._get_handler(url)

    def delete_team(self, team_id):
        """
        Removes a given team from Terraform Enterprise
        :param team_id: String of team ID.
        """
        url = self.url + 'teams/{}'.format(team_id)
        return self._delete_handler(url)
