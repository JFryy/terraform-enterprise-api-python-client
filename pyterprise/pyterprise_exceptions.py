class APIErrors(Exception):
   pass


class UnauthorizedError(APIErrors):
    def __init__(self, message, errors):
        super(UnauthorizedError, self).__init__(message)
        self.errors = errors
        print('Unauthorized Error. Please verify validity of access token.')
        pass

class InternalServerError(APIErrors):
    def __init__(self, message, errors):
        super(InternalServerError, self).__init__(message)
        self.errors = errors
        print('Internal Server Error. Please verify availability of the service.')
        pass
