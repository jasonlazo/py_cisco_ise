import requests

# from . import CiscoIseClient

# c = CiscoIseClient(
#     url='10.66.72.69',
#     username='ersadmin',
#     password='3r54!3nTT3LL#20',
# )
#
# c.create_group()


s = requests.Session()
s.verify = False
# url = 'https://10.66.72.69/admin/login.jsp'
# s.get(
#     url=url
# )

data = {
    'username': 'apiadmin',
    'password': ['3nT3L.2020', '3nT3L.2020'],
    'rememberme': 'on',
    'name': 'apiadmin',
    'authType': 'Internal',
    'newPassword': '',
    'destinationURL': '',
    'xeniaUrl': '',
}
data = {
    'username': 'apiadmin',
    'password': '3nT3L.2020',
    'rememberme': 'on',
    'name': 'apiadmin',
    'authType': 'Internal',
    'newPassword': '',
    'destinationURL': '',
    'xeniaUrl': '',
}
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://10.66.72.69',
    'DNT': '1',
    'Referer': 'https://10.66.72.69/admin/login.jsp',
}
url = 'https://10.66.72.69/admin/LoginAction.do'
res = s.post(
    url=url,
    data=data,
    headers=headers
)

res_2 = s.get(
    url='https://10.66.72.69/admin/idMgmtEndpointGroupAction.do?command=createPreload',
    headers=headers
)


def get_token(res_2):
    searched = "OWASP_CSRFTOKEN="
    p = res_2.find(searched)

    _ = res_2[p + len(searched): p + len(searched) + 39]

    return _


token = get_token(res_2.text)
print(res_2)

body_create = {
    'selectedItemName': '',
    'idGroupType': '',
    'crud': 'Create',
    'createAction': 'createTopGroup',
    'assignedUsersJsonStr': '',
    'loggedInUserRBACFullPermission': 'true',
    'logInUserPermOnSelectedRecord': '',
    'nsfIdGroup.name': 'test_group_002',
    'nsfIdGroup.description': 'descripcion',
    'OWASP_CSRFTOKEN': '1HVH-310F-HD5D-4PEZ-E0WY-KQ8Y-9KSD-9GXZ',
    # 'dojo.preventCache': '1581508490471',
}

body_create['OWASP_CSRFTOKEN'] = token

res_crear = s.post(
    url="https://10.66.72.69/admin/idMgmtUserGroupAction.do?command=save",
    data=body_create,
    headers=headers
)

print(res_crear)
