from clients.rest_client import CiscoIseRestClient
from rest_requests.internal_user import InternalUser

hostname = '10.66.72.69'
username = 'ersadmin'
password = '3r54!3nTT3LL#20'

client = CiscoIseRestClient(
    username=username,
    password=password,
    hostname=hostname,
    verify_ssl=False
)

client.send_request(
    InternalUser.GET_ALL,
    body_parms={
        "InternalUser": {
            "name": "jlazo.soft.com11",
            "password": "PEPito-5764333",
            "enablePassword": "PEPito-5764333",
            "enabled": True,
            "email": "jlazolock@softlabperu.com",
            "identityGroups": "5e6e1b80-38d3-11e9-90d9-0242f250cb09",
        }
    }
)
