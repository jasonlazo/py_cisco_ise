from http import HTTPStatus
from urllib.parse import ParseResult

import requests


class WebIseClient:
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
            verify_certificate: bool = True
    ):

        self._username = username
        self._password = password
        self._hostname = hostname
        self._port = port

        self._http_session = requests.Session()

        self._http_session.verify = verify_certificate

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()

    def login(self):
        body = {
            'username': self._username,
            'password': self._password,
            'rememberme': 'on',
            'name': self._username,
            'authType': 'Internal',
            'newPassword': '',
            'destinationURL': '',
            'xeniaUrl': '',
        }
        response = self._http_session.post(
            url=self._get_url_root(path="/admin/LoginAction.do"),
            data=body,
            headers=self.headers
        )
        if not ("load-message" in response.text):
            raise Exception("No ha podido iniciar sesion")

    def logout(self):
        prev_session_id = self._http_session.cookies.get_dict().get("APPSESSIONID", None)

        if prev_session_id:
            response = self._http_session.get(
                url=self._get_url_root(path="/admin/logout.jsp")
            )
            post_session_id = self._http_session.cookies.get_dict().get("APPSESSIONID", None)

            if prev_session_id == post_session_id:
                raise Exception("Not logout: Same SessionId")

            if any([
                len(response.history) != 3,
                not all([item.status_code == HTTPStatus.FOUND for item in response.history])
            ]):
                raise Exception("Not logout: Response not expected")
        else:
            raise Exception(f"Not previous SessionId: APPSESSIONID:[{prev_session_id}]")

    def _get_url_root(self, path: str, scheme: str = HTTPS_PROTOCOL, **kwargs):

        parser = ParseResult(
            scheme=scheme,
            # netloc=f"{self._hostname}:{self._port}",
            netloc=f"{self._hostname}",
            path=path,
            params='', query='', fragment=''
        )
        return parser.geturl()

    @staticmethod
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

    def create_identity_group(self, group_name: str, group_description: str = ""):

        response_form = self._http_session.get(
            url=self._get_url_root(path="/admin/idMgmtEndpointGroupAction.do"),
            params=dict(command="createPreload"),
            headers=self.headers
        )

        owasp_csrftoken = self._get_csrftoken(response_form.text)

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
        }

        response_create_identity_group = self._http_session.post(
            url=self._get_url_root(path="/admin/idMgmtUserGroupAction.do"),
            params=dict(command="save"),
            data=body,
            headers=self.headers,
        )

        response_as_json = response_create_identity_group.json()

        if response_as_json["respCode"] != "Success":
            raise Exception("Error creating identity group: {}".format(response_as_json["respMsg"]))

        return response_as_json

    def create_policy_set(self, police_name: str, identity_group: str, profiles: list):
        response_form = self._http_session.get(
            url=self._get_url_root(
                path="/admin/login.jsp#workcenters/workcenter_guest_access/workcenter_guest_access_policy_sets_new"
            ),
            params=dict(command="createPreload"),
            headers=self.headers
        )

        owasp_csrftoken = self._get_csrftoken(response_form.text)

        headers = {
            'X-Requested-With': 'XMLHttpRequest, OWASP CSRFGuard Project',
            'OWASP_CSRFTOKEN': owasp_csrftoken,
        }

        response_begin_transaction = self._http_session.post(
            url=self._get_url_root(
                path="/admin/rs/uiapi/policy/transactionmanager/begintransaction"
            ),
            params=dict(),
            headers={**self.headers, **headers}
        )

        if response_begin_transaction.status_code != HTTPStatus.OK:
            raise Exception("Error creating policy set: Can't start transaction")

        try:
            transaction_id = response_begin_transaction.headers["transaction_id"]
        except KeyError:
            raise Exception("Error creating policy set: Not transaction_id on response headers")

        body = {
            "state": "ENABLED",
            "name": police_name,
            "conditionObject": {
                "Field1": {
                    "type": "SINGLE",
                    "not": "",
                    "conditionId": None,
                    "attributes": {
                        "lhsDictionary": "IdentityGroup", "lhsAttribute": "Name",
                        "operator": "IN",
                        "attributeNameType": "STRING", "attributeValueType": "STATIC",
                        "attributeValue": "Endpoint Identity Groups:All Groups:{identity_group}".format(
                            identity_group=identity_group)
                    }
                }
            },
            "results": {
                "Profiles": profiles
            },
            "rank": 0
        }

        response_create_policy_set = self._http_session.post(
            url=self._get_url_root(
                path="/admin/rs/uiapi/policytable/radius/a875490e-e4ab-4e46-90b4-8de8d17e5085/authorization"
            ),
            params=dict(transaction_id=transaction_id),
            headers={**self.headers, **headers},
            json=body
        )

        if response_create_policy_set.status_code != HTTPStatus.ACCEPTED:
            raise Exception("Error creating policy set: Policy Set not valid")

        response_commit = self._http_session.post(
            url=self._get_url_root(path="/admin/rs/uiapi/policy/transactionmanager/committransaction"),
            params=dict(transaction_id=transaction_id),
            headers={**self.headers, **headers}
        )

        if response_commit.status_code != HTTPStatus.OK:
            raise Exception("Error creating policy set: Can't commit transaction")
