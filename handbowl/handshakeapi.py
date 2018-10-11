import requests


class Handshake():
    """This is a class wrapper
    for the handshake json api"""

    def __init__(self, key):
        self.apiKey = key
        self.products = []

    def check_api_key(self):
        r = requests.get(
            'https://app.handshake.com/api/latest/items',
            auth=(self.apiKey, 'X'))

        return r.status_code

    def get_products(self):
        r = requests.get(
            'https://app.handshake.com/api/latest/items',
            auth=(self.apiKey, 'X'))

        res = r.json()

        products = res['objects'][:]

        while res['meta']['next'] is not None:
            r = requests.get(
                'https://app.handshake.com{}'.format(
                        res['meta']['next']),
                auth=(self.apiKey, 'X'))

            res = r.json()
            products.extend(res['objects'])

        return products
