import base64
import json
import requests
from io import BytesIO

HTTP_HEADER_COOOKIE = 'Cookie'
OB_HOST = "https://localhost:18469"
OB_USERNAME = "steve"
OB_PASSWORD = "obclub1234"
OB_API_PREFIX = '/api/v1/'
SESSION_COOKIE_NAME = 'TWISTED_SESSION'

r = requests.post(
    u'{}{}login'.format(OB_HOST, OB_API_PREFIX),
    cert=(
        '/home/openbazaar/OpenBazaar-Server/server.crt',
        '/home/openbazaar/OpenBazaar-Server/server.key'),
    data={'username': OB_USERNAME, 'password': OB_PASSWORD})

assert r.status_code == 200
assert 'success' in r.json()
assert r.json()['success']
assert SESSION_COOKIE_NAME in r.cookies

session_cookie = r.cookies[SESSION_COOKIE_NAME]

print (session_cookie)
