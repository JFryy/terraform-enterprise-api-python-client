class SSHKey(object):

    def __init__(self, ssh_key, api_handler):
        self._api_handler = api_handler
        self.id = ssh_key.id
        self.name = ssh_key.attributes.name

    def __str__(self):
        return str(self.__dict__)

    def update(self, name):
        payload = {"data": {"attributes": {"name": name}}}
        return self._api_handler.call(method='patch',
                                      uri=f'ssh-keys/{self.id}',
                                      json=payload)

    def delete(self):
        return self._api_handler.call(method='delete',
                                      uri=f'ssh-keys/{self.id}')
