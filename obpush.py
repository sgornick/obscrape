import base64
import json
import requests
from io import BytesIO

HTTP_HEADER_COOOKIE = 'Cookie'
OB_HOST = "http://localhost:18469"
OB_USERNAME = "username"
OB_PASSWORD = "password"
OB_API_PREFIX = '/api/v1/'
SESSION_COOKIE_NAME = 'TWISTED_SESSION'

r = requests.post(
    u'{}{}login'.format(OB_HOST, OB_API_PREFIX),
    data={'username': OB_USERNAME, 'password': OB_PASSWORD})

assert r.status_code == 200
assert 'success' in r.json()
assert r.json()['success']
assert SESSION_COOKIE_NAME in r.cookies

session_cookie = r.cookies[SESSION_COOKIE_NAME]


def upload_image(url):
    response = requests.get(url)
    assert response.status_code == 200
    img_bytes = BytesIO(response.content).read()
    response = \
        requests.post(
            u'{}{}upload_image'.format(OB_HOST, OB_API_PREFIX),
            cookies={SESSION_COOKIE_NAME: session_cookie},
            files={'image': base64.b64encode(img_bytes)})
    assert response.status_code == 200
    # Return the image hash.
    return response.json()['image_hashes'][0]


with open('data/items.json') as json_data:
    data = json.load(json_data)

for row in data:
    img_hashes = []
    for photo_url in row['photos']:
        # Store the file on OB.
        img_hashes.append(upload_image(photo_url))

    response = \
        requests.post(
            u'{}{}contracts'.format(OB_HOST, OB_API_PREFIX),
            cookies={SESSION_COOKIE_NAME: session_cookie},
            data={
                'title': row['title'],
                'description':
                    '<pre>'
                    '**   NOTE - THIS IS JUST A TEST OF OPEN BAZAAR.  **<br />'
                    '** NO ITEMS IN THIS STORE ARE ACTUALLY FOR SALE. **<br />'
                    '</pre>{}<pre>'
                    '**   NOTE - THIS IS JUST A TEST OF OPEN BAZAAR.  **<br />'
                    '** NO ITEMS IN THIS STORE ARE ACTUALLY FOR SALE. **<br />'
                    'This data was scraped from <a href=\"{}\">{}</a>.'
                    '</pre>'.format(
                        row['description'], row['url'], row['title']),
                'currency_code': row['currency_code'],
                'price': row['price'],
                'process_time': 'TEST ONLY',
                'nsfw': False,
                'keywords': row['keywords'],
                'category': row['category'],
                'condition': 'New',
                'sku': row['sku'],
                'images': img_hashes,
                'moderators': [],
                'options': {},
                'expiration_date': '',
                'metadata_category': 'physical good',
                'free_shipping': True,
                'shipping_origin': 'ITALY',
                'ships_to': ['TUVALU'],
                'est_delivery_domestic': 'TEST ONLY',
                'est_delivery_international': 'TEST ONLY',
                'shipping_currency_code': row['currency_code'],
                'shipping_domestic': 0,
                'shipping_international': 0,
                'terms_conditions':
                    'NOTE - THIS IS JUST A TEST OF OPEN BAZAAR.\r\n'
                    'NO ITEMS IN THIS STORE ARE ACTUALLY FOR SALE.',
                'returns':
                    'NOTE - THIS IS JUST A TEST OF OPEN BAZAAR.\r\n'
                    'NO ITEMS IN THIS STORE ARE ACTUALLY FOR SALE.',
            })
