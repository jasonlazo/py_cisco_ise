from enum import Enum
from urllib.parse import ParseResult

import requests

from rest_requests import CiscoIseRequest, get_path, get_body


class CiscoIseRestClient:

    def __init__(self, username, password, hostname, port=9060, **kwargs):
        self._username = username
        self._password = password
        self._hostname = hostname
        self._port = port
        self._scheme = kwargs.get("scheme", "https")
        self._verify_ssl = kwargs.get("verify_ssl", True)

    def _parse_url(self, path: str):
        parser = ParseResult(
            scheme=self._scheme,
            netloc=f"{self._hostname}:{self._port}",
            path=path,
            params='',
            query='',
            fragment=''
        )
        return parser.geturl()

    def send_request(self, cisco_request_enum: Enum, body_parms=None, path_params=None):
        if not isinstance(getattr(cisco_request_enum, "value", None), CiscoIseRequest):
            raise Exception("Should be cisco_request_enum")

        cisco_request: CiscoIseRequest = cisco_request_enum.value

        headers = {'Content-type': 'application/json'}
        http_response = requests.request(
            cisco_request.method,
            url=self._parse_url(
                get_path(cisco_request.path, path_params)
            ),
            json=get_body(cisco_request.body, body_parms),
            auth=(self._username, self._password),
            verify=self._verify_ssl,
            headers=headers
        )

        if http_response.status_code != cisco_request.ok_status_code:
            raise Exception("Fail")

        return http_response