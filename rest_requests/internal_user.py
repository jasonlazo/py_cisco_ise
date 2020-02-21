from enum import Enum
from http import HTTPStatus

from py_cisco_ise import http_methods
from py_cisco_ise.rest_requests.base import CiscoIseRequest


class InternalUser(Enum):
    GET_BY_ID = CiscoIseRequest(
        path="/ers/config/internaluser/{}",
        method=http_methods.GET
    )

    UPDATE = CiscoIseRequest(
        path="/ers/config/internaluser/{}",
        method=http_methods.PUT,
        body={
            "InternalUser": {
                "id": "",
                "name": "",
                "description": "",
                "enabled": False,
                "email": "",
                "password": "",
                "firstName": "",
                "lastName": "",
                "changePassword": False,
                "identityGroups": "",
                "expiryDateEnabled": False,
                "expiryDate": "",
                "enablePassword": "",
                "customAttributes": {},
                "passwordIDStore": ""
            }
        }
    )

    DELETE = CiscoIseRequest(
        path="/ers/config/internaluser/{}",
        method=http_methods.DELETE,
        ok_status_code=HTTPStatus.NO_CONTENT
    )

    CREATE = CiscoIseRequest(
        path="/ers/config/internaluser/",
        method=http_methods.POST,
        ok_status_code=HTTPStatus.CREATED,
        body={
            "InternalUser": {
                "id": "",
                "name": "",
                "description": "",
                "enabled": False,
                "email": "",
                "password": "",
                "firstName": "",
                "lastName": "",
                "changePassword": False,
                "identityGroups": "",
                "expiryDateEnabled": False,
                "expiryDate": "",
                "enablePassword": "",
                "customAttributes": {},
                "passwordIDStore": ""
            }
        }
    )

    GET_ALL = CiscoIseRequest(
        path="/ers/config/internaluser/",
        method=http_methods.GET
    )
