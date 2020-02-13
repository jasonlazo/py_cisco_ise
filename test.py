from conector import CiscoIseClient

username = 'apiadmin'
password = '3nT3L.2020'
hostname = '10.66.72.69'

username = 'ersadmin'
password = '3r54!3nTT3LL#20'

client = CiscoIseClient(
    username=username,
    password=password,
    hostname=hostname
)

# client.login()

client.create_internal_user(
    group_name="grupo_001"
)
