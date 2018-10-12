import requests


class Handshake():
    """This is a class wrapper
    for the handshake json api"""

    def __init__(self, key):
        self.apiKey = key
        self.products = []

        if not self.is_api_key_valid():
            raise ValueError("Must provide correct API Key")

    def is_api_key_valid(self):
        r = requests.get(
            'https://app.handshake.com/api/latest/orders',
            auth=(self.apiKey, 'X'))

        if r.status_code == 200:
            return True

        return False

    def fetch_full_product_list(self):
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

    def fetch_full_inventory_list(self):
        pass

    def fetch_full_customer_list(self):
        r = requests.get(
            'https://app.handshake.com/api/latest/customers',
            auth=(self.apiKey, 'X'))

        res = r.json()

        customers = res['objects']

        while res['meta']['next'] is not None:
            r = requests.get(
                'https://app.handshake.com{}'.format(
                    res['meta']['next']),
                auth=(self.apiKey, 'X'))
            res = r.json()
            customers.extend(res['objects'])

        return customers

    def fetch_recent_orders(self):
        r = requests.get(
            'https://app.handshake.com/latest/orders'
            '?order_by=-ctime&limit=5',
            auth=(self.apiKey))

        res = r.json()

        return res['objects']
