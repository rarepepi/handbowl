import requests
import datetime


class Client():
    """This is a class wrapper
    for the handshake json api"""

    def __init__(self, key):
        self.apiKey = key
        self.session = self._init_session()

    def _init_session(self):

        if self._is_api_key_valid():
            print("api key is valid")
            session = requests.Session()
            session.auth = (self.apiKey, 'X')

            return session

        else:
            raise ValueError("Must provide correct API Key")

    def _is_api_key_valid(self):
        r = requests.get(
            'https://app.handshake.com',
            auth=(self.apiKey, 'X'))

        if r.status_code == 200:
            return True

        else:
            return False

    def get_full_product_list(self):
        print("in product list")
        r = self.session.get(
            'https://app.handshake.com/api/latest/items')

        res = r.json()

        products = res['objects'][:]
        print("total: {}".format(res['meta']['total_count']))

        while res['meta']['next'] is not None:
            print(res['meta']['next'])
            r = self.session.get(
                'https://app.handshake.com{}'.format(
                    res['meta']['next']))

            res = r.json()
            products.extend(res['objects'])

        return products

    def get_full_inventory_list(self):
        pass

    def get_full_customer_list(self):
        r = self.session.get(
            'https://app.handshake.com/api/latest/customers')

        res = r.json()

        customers = res['objects']

        while res['meta']['next'] is not None:
            print(res['meta']['next'])
            r = self.session.get(
                'https://app.handshake.com{}'.format(
                    res['meta']['next']))

            res = r.json()
            customers.extend(res['objects'])

        return customers

    def get_recent_orders(self):
        r = self.session.get(
            'https://app.handshake.com/api/latest/orders'
            '?order_by=-ctime&limit=5')

        res = r.json()

        return res['objects']

    def create_new_product_category_id(self):
        date = datetime.now().strftime("%m/%d/%y")
        hs_category_name = "New Products | {}".format(date)

        data = {
            "name": hs_category_name,
            "id": hs_category_name,
            "categoryPosition": "0"
        }

        r = self.session.post(
            'https://app.handshake.com/api/latest/categories',
            json=data)

        res = r.json()
        category_id = res['objID']

        return category_id

    def update_order_status(self, order):
        payload = {
            "old": "Confirmed",
            "new": "Processing"
        }
        r = self.session.post(
            'https://app.handshake.com/api/latest/orders/{}/'
            'actions/changeStatus'.format(order['id'].strip('#')),
            json=payload)

        r.status_code

    # def create_missing_products(hs_products, fb_products):
    #     missing_products = []

    #     for product in fb_products:
    #         if not any(dict['sku'] == product[0] for dict in hs_products):
    #             temp_id_date = self.get_category_id()

    #             print("product missing in hs: {}".format(product[0]))
    #             if temp_id_date is not None:
    #                 hs_category_id_and_name_date = temp_id_date[:]

    #             temp = {
    #                 "category": {
    #                     "entityType": "Category",
    #                     "name": hs_category_id_and_name_date[1],
    #                     "id": hs_category_id_and_name_date[1],
    #                     "categoryPosition": 0,
    #                     "objID": hs_category_id_and_name_date[0]
    #                 },
    #                 "longDesc": product[2],
    #                 "name": product[2],
    #                 "sku": product[0],
    #                 "unitPrice": product[5]
    #             }
    #             missing_products.append(temp)

    #     data = {
    #         "objects": missing_products
    #     }

    #     try:
    #         r = requests.patch(
    #             'https://app.handshake.com/api/latest/items',
    #             auth=(config.HANDSHAKE['APIKEY'], 'X'),
    #             json=data)
    #         r.status_code

    #     except requests.exceptions.ConnectionError as e:
    #         print("Error: catergory_id connection error!")
    #         sys.exit()

    # def update_product_inventory(hs_products, fb_products):
    #     for product in fb_products:
    #         if any(dict['sku'] == product[0] for dict in hs_products):
    #             data = {
    #                 "idk": "find out"
    #             }
    #             try:
    #                 r = requests.patch('')

    #             except requests.exceptions.ConnectionError as e:
    #                 print("Error: get_hs_products connection error!")
    #                 sys.exit()
