from enum import Enum
from http import HTTPStatus

from py_cisco_ise import http_methods
from py_cisco_ise.rest_requests.base import CiscoIseRequest


class DownloadableACL(Enum):
    # GET_BY_ID = CiscoIseRequest(
    #     path="/ers/config/identitygroup/{}",
    #     method=http_methods.GET
    # )
    #
    # GET_ALL = CiscoIseRequest(
    #     path="/ers/config/identitygroup/?size={size}&page={page}",
    #     method=http_methods.GET,
    #
    # )

    CREATE = CiscoIseRequest(
        path="/ers/config/downloadableacl",
        method=http_methods.POST,
        ok_status_code=HTTPStatus.CREATED,
        body={
            "DownloadableAcl": {
                "name": "",
                "description": "",
                "dacl": ""
            }
        }
    )
