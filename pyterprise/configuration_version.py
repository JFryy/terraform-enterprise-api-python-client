class ConfigurationVersion(object):

    def __init__(self, configuration, api_handler):
        self._api_handler = api_handler

        self.id = configuration.id

        attributes = configuration.attributes
        self.auto_queue_runs = attributes.auto_queue_runs
        self.error = attributes.error
        self.error_message = attributes.error_message
        self.source = attributes.source
        self.status = attributes.status
        self.status_timestamps = attributes.status_timestamps
        self.changed_files = attributes.changed_files

    def __str__(self):
        return str(self.__dict__)
