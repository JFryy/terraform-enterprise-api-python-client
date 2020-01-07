import collections
import requests
from .exceptions import APIException


class APICaller(object):
    def __init__(self,base_url, headers):
        self._base_url = base_url
        self._headers = headers

    def call(self, uri, method="get", *args, **kwargs):
        requester = getattr(requests, method.lower())
        url = self._base_url + uri
        response = requester(url=url, headers=self._headers, *args, **kwargs)
        if response.status_code < 400:
            if method in ["get", "post", "patch", "put"]:
                response_json = response.json()
                if response_json and "data" in response_json:
                    return APIResponse(response_json)
                else:
                    return response.status_code
            elif method == "delete":
                return response.status_code
        else:
            raise APIException(f"Error: {response.status_code}: {response.content}, {url}", response)


class APIResponse(object):
    def __init__(self, response):
        self.data = response.get("data", [])
        self.meta = response.get("meta", [])
        self.links = response.get("links", [])
        self.included = response.get("included", [])
        self.errors = response.get("errors", [])

    def __str__(self):
        if self.data:
            if isinstance(self.data, collections.abc.Iterable):
                return str(self.data)
