class TFCClientException(Exception):
    pass


class APIException(TFCClientException):
    def __init__(self, message, response):
        self.message = message
        self.response = response
