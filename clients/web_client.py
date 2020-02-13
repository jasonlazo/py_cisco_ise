from urllib.parse import ParseResult

import requests


class CiscoIseClient:
    HTTPS_PROTOCOL = "https"
    headers = {
        # 'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://10.66.72.69',
        'DNT': '1',
        'Referer': 'https://10.66.72.69/admin/login.jsp',
    }

    def __init__(
            self,
            username: str,
            password: str,
            hostname: str,
            port: int = 9060,
            ignore_certificate: bool = True
    ):

        self._username = username
        self._password = password
        self._hostname = hostname
        self._port = port

        self._http_session = requests.Session()
        if ignore_certificate:
            self._http_session.verify = False

    def login(self):
        data = {
            'username': self._username,
            'password': self._password,
            'rememberme': 'on',
            'name': self._username,
            'authType': 'Internal',
            'newPassword': '',
            'destinationURL': '',
            'xeniaUrl': '',
        }
        res = self._http_session.post(
            url='https://10.66.72.69/admin/LoginAction.do',
            data=data,
            headers=self.headers
        )
        if not ("load-message" in res.text):
            raise Exception("No ha podido iniciar sesion")

    def _parse_url(self, path: str, params: dict = {}, scheme: str = HTTPS_PROTOCOL, is_rest: bool = True):
        params = params if params else {}
        if not params:
            for k, d in params.items():
                pass

        parser = ParseResult(
            scheme=scheme,
            netloc=f"{self._hostname}:{self._port}" if is_rest else self._hostname,
            path=path,
            params='', query='', fragment=''
        )
        return parser.geturl()

    def _send_req(self, url, body):
        headers = {'Content-type': 'application/json'}
        res = requests.post(
            url,
            json=body,
            auth=(self._username, self._password),
            verify=False,
            headers=headers

        )

        return res

    def create_group(self):
        _ = self.url
        _ = 'https://10.66.72.69:9060/ers/config/identitygroup'
        res = self._send_req(
            url=_,
            body={
                "IdentityGroup": {

                    "id": "id",

                    "name": "test_24",

                    "description": "description",

                    "parent": "parent"

                }
            }
        )
        print(res)

    def create_internal_user(self, **kwargs):
        body = {
            "InternalUser": {
                "id": "id",
                "name": "jlazo.soft.com",
                "description": "description",
                "enabled": False,
                "email": "email@domain.com",
                # "password": "PEPito-5764333$%&!\"$%&'()*+,-./:;<=>?[\\]^_`{|}~",
                "password": "_a7Ocmfp",
                "firstName": "jason",
                "lastName": "lazo locke",
                "changePassword": False,
                "identityGroups": "grupo_001",
                "expiryDateEnabled": False,
                "expiryDate": "2026-12-11",
                "enablePassword": "enablePassword",
                "customAttributes": {
                    "key1": "value1",
                    "key2": "value3"
                },
                "passwordIDStore": "Internal Users"
            }
        }

        res = self._send_req(
            url=self._parse_url(path="/ers/config/internaluser"),
            body=body
        )

        print(res)

    def create_identity_group(self, group_name: str, group_description: str = ""):
        def _get_csrftoken(html: str):
            owasp_key = "OWASP_CSRFTOKEN="
            len_owasp_key = len(owasp_key)
            len_csrftoken = 39

            idx_start = html.find(owasp_key)
            if idx_start == -1:
                raise Exception("No se encontro el CSRFTOKEN")
            idx_start += len_owasp_key

            csrftoken = html[idx_start: idx_start + len_csrftoken]
            return csrftoken

        response_form = self._http_session.get(
            # url="https://10.66.72.69/admin/idMgmtEndpointGroupAction.do?command=createPreload",
            url=self._parse_url(path="/admin/idMgmtEndpointGroupAction.do", is_rest=False),
            params=dict(command="createPreload"),
            headers=self.headers
        )

        owasp_csrftoken = _get_csrftoken(response_form.text)

        body = {
            'selectedItemName': '',
            'idGroupType': '',
            'crud': 'Create',
            'createAction': 'createTopGroup',
            'assignedUsersJsonStr': '',
            'loggedInUserRBACFullPermission': 'true',
            'logInUserPermOnSelectedRecord': '',
            'nsfIdGroup.name': group_name,
            'nsfIdGroup.description': group_description,
            'OWASP_CSRFTOKEN': owasp_csrftoken,
            # 'dojo.preventCache': '1581508490471',
        }

        response_create_identity_group = self._http_session.post(
            # url="https://10.66.72.69/admin/idMgmtUserGroupAction.do?command=save",
            url=self._parse_url(path="/admin/idMgmtUserGroupAction.do", is_rest=False),
            params=dict(command="save"),
            data=body,
            headers=self.headers,
        )

        response_as_json = response_create_identity_group.json()

        if response_as_json["respCode"] != "Success":
            raise Exception(response_as_json["respMsg"])

        print(response_create_identity_group)
