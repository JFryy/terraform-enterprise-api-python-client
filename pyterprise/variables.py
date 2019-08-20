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
        return self._post_handler(url=url, json=payload)

    def modify_workspace_variable(self, workspace_id, attributes):
        """
        Modify an existing workspace variable in a given workspace, omit fields to not overwrite them.
        :param workspace_id: String of workspace id for terraform variables
        :param attributes: A map of attributes. i.e.
        "id": workspace_id,
                {
                    "key": "name",
                    "value": "value",
                    "category": "terraform",
                    "hcl": False,
                    "sensitive": False
                }
        """
        url = self.url + 'vars/{}'.format(workspace_id)
        payload = {
            "data": {
                "id": workspace_id,
                "attributes": attributes,
                "type": "vars"
            }
        }

        return self._post_handler(url=url, json=payload)

    def list_variables(self, organization, workspace):
        """
        Lists variables in a given workspace.
        :param organization: String of organization Name
        :param workspace: String of workspace id for terraform variables
        """
        url = self.url + 'vars?filter%5Borganization%5D%5Bname%5D={}&filter%5Bworkspace%5D%5Bname%5D={}'\
            .format(organization, workspace)
        return self._get_handler(url)

    def delete_workspace_variable(self, variable_id):
        """
        Deletes variable for a given variable id.
        :param variable_id: string, variable id found via list variables
        """
        url = self.url + '/vars/{}'.format(variable_id)
        return self._delete_handler(url)
