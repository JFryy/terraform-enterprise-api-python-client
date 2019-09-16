import requests
import logging as log
import json
from .pyterprise_exceptions import UnauthorizedError, InternalServerError
from .organizations import Organziations
from .plans import Plans
from .teams import Teams
from .runs import Runs
from .variables import Variables
from .workspaces import Workspaces
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

"""
Copyright (c) 2018 The Python Packaging Authority

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class Client(Organziations, Plans, Teams, Runs, Variables, Workspaces):
    """
    Client class which inherits subclasses for different method types as defined in the TFE API Documentation. Set token
    and V2 API URL using the non default 'init' construcutor method.
    """
    log.basicConfig(
        level=log.WARNING
    )

    def __init__(self):
        return

    def init(self, token, url, ssl_verification=True, version='v2'):
        self.token = token
        self.url = url + '/api/{}/'.format(version)
        self.headers = {
            'Content-Type': 'application/vnd.api+json',
            'Authorization': 'Bearer {}'.format(token)
        }
        
        self.ssl_verification = ssl_verification

    # HTTP helper methods
    def _get_handler(self, url):
        response = requests.get(url=url, verify=self.ssl_verification, headers=self.headers)
        self._error_handler(response)
        return response.content

    def _post_handler(self, url, json):
        response = requests.post(url=url, verify=self.ssl_verification, headers=self.headers, json=json)
        self._error_handler(response)
        return response.content

    def _patch_handler(self, url, json):
        response = requests.patch(url=url, verify=self.ssl_verification, headers=self.headers, json=json)
        self._error_handler(response)
        return response.content

    def _delete_handler(self, url):
        response = requests.delete(url, verify=self.ssl_verification)
        self._error_handler(response)
        return response.content

    @staticmethod
    def _error_handler(response):
            if response.status_code in range(400, 499):
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
                log.warning('{}: {}'.format(response.url, response.status_code))

