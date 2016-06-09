import requests

HTTP_HEADER_COOOKIE = 'Cookie'
OB_HOST = "http://localhost:18469"
OB_USERNAME = "username"
OB_PASSWORD = "password"
OB_API_PREFIX = '/api/v1/'
SESSION_COOKIE_NAME = 'TWISTED_SESSION'

r = requests.post(
    '{}{}login'.format(OB_HOST, OB_API_PREFIX),
    data={'username': OB_USERNAME, 'password': OB_PASSWORD})

assert r.status_code == 200
assert 'success' in r.json()
assert r.json()['success']
assert SESSION_COOKIE_NAME in r.cookies

session_cookie = r.cookies[SESSION_COOKIE_NAME]

r = requests.post(
    '{}{}contracts'.format(OB_HOST, OB_API_PREFIX),
    cookies={SESSION_COOKIE_NAME: session_cookie},
    data={
        'title': 'Test Title',
        'description': 'Test Description',
        'currency_code': 'USD',
        'price': 1.23,
        'process_time': 'Test Process Time',
        'nsfw': False,
        'keywords': ['test', 'tag'],
        'category': 'Test Category',
        'condition': 'New',
        'sku': 'Test SKU',
        'images': ['076fc54335100a28d9e9fe7141efeb64769b3609'],
        'moderators': [],
        'options': {},
        'expiration_date': '',
        'metadata_category': 'physical good',
        'free_shipping': False,
        'shipping_origin': 'UNITED_STATES',
        'ships_to': ['UNITED_STATES'],
        'est_delivery_domestic': 'Test Domestic Shipping',
        'est_delivery_international': 'Test International Shipping',
        'shipping_currency_code': 'USD',
        'shipping_domestic': 0.01,
        'shipping_international': 0.02,
        'terms_conditions': 'Test Terms and Conditions',
        'returns': 'Test Return Policy.',
    })

assert r.status_code == 200
assert r.json()['success']

print 'Contract ID: {}'.format(r.json()['id'])

#"expiration_date=&metadata_category=hysical%20good&title=AWESOME&description=Test%20Description&currency_code=BTC&price=0.0015&process_time=1&nsfw=false&terms_conditions=&returns=&shipping_currency_code=BTC&shipping_domestic=0&shipping_international=0&category=&condition=New&sku=&images=5f4cd3e4304a5da50992ac077cf319543da89625&free_shipping=true&moderators=[]&keywords=['test']&contract_id=&ships_to=UNITED_STATES&shipping_origin=UNITED_STATES" http://localhost:18469/api/v1/contracts

# curl -H "Cookie: TWISTED_SESSION=5690d9ceade2e1b9aea75a917651a113" -X POST -d "expiration_date=&metadata_category=hysical%20good&title=AWESOME&description=Test%20Description&currency_code=BTC&price=0.0015&process_time=1&nsfw=false&terms_conditions=&returns=&shipping_currency_code=BTC&shipping_domestic=0&shipping_international=0&category=&condition=New&sku=&images=5f4cd3e4304a5da50992ac077cf319543da89625&free_shipping=true&moderators=[]&keywords=['test']&contract_id=&ships_to=UNITED_STATES&shipping_origin=UNITED_STATES" http://localhost:18469/api/v1/contracts
