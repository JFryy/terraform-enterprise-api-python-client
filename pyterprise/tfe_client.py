import requests
import os
import logging as log
from .pyterprise_exceptions import UnauthorizedError, InternalServerError
from json import load, loads
from .uri_methods import Calls


class Client(Calls):
    log.basicConfig(
        level=log.WARN
    )

    def __init__(self):
        self.payloads_dir = os.path.dirname(os.path.realpath(__file__)) + '/payloads/'

    def init(self, token, url):
        self.token = token
        self.url = url + '/api/v2/'
        self.headers = {
            'Content-Type': 'application/vnd.api+json',
            'Authorization': 'Bearer {}'.format(token)
        }

    def _tfe_api_get(self, url):
        response = requests.get(url=url, headers=self.headers)
        self._error_handler(response)
        return response.content

    def _error_handler(self, response):
        if response.status_code == 401 or response.status_code == 403:
            raise UnauthorizedError(
                message=response.content,
                errors=response.status_code
            )
        if response.status_code in range(500, 504):
            raise InternalServerError(
                message=response.content,
                errors=response.status_code
            )

        if response.status_code not in range(200, 202):
            log.error('{}: {}'.format(response.url, response.status_code))
