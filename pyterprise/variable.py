class Variable(object):

    def __init__(self, variable, api_handler):
        self._api_handler = api_handler

        self.id = variable.id
        attributes = variable.attributes
        self.key = attributes.key
        self.value = attributes.value
        self.category = attributes.category
        self.hcl = attributes.hcl
        self.sensitive = attributes.sensitive
        self.workspace_id = variable.relationships.configurable.data.id

    def __str__(self):
        return str(self.__dict__)

    def update(self,
               key=None,
               value=None,
               category=None,
               hcl=None,
               sensitive=None,
               description=None):
        """ Update variable with supplied fields. """
        defaults = {
            'key': self.key,
            'value': self.value,
            'category': self.category,
            'hcl': self.hcl,
            'sensitive': self.sensitive,
            'description': ""
        }

        arguments = locals()
        del arguments['self']

        for arg, value in arguments.items():
            if value != None:
                defaults[arg] = value

        payload = {
            "data": {
                "type": "vars",
                "attributes": {
                    "key": defaults["key"],
                    "value": defaults["value"],
                    "description": defaults["description"],
                    "category": defaults["category"],
                    "hcl": defaults["hcl"],
                    "sensitive": defaults["sensitive"]
                },
                "relationships": {
                    "workspace": {
                        "data": {
                            "id": self.workspace_id,
                            "type": "workspaces"
                        }
                    }
                }
            }
        }
        return self._api_handler.call(uri=f'vars/{self.id}',
                                      method='patch',
                                      json=payload).data

    def delete(self):
        return self._api_handler.call(uri=f'vars/{self.id}', method='delete')
