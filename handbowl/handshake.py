import requests
import datetime


class Client():
    """
    This is a wrapper
    for the Handshake JSON API
    """

    def __init__(self, key):
        """
        Checks apiKey and starts session
        with Handshake API
        """

        self.apiKey = key
        self.session = self._init_session()

    def _init_session(self):
        """
        Tests api key validility
        And initalizes session with Handshake
        """

        if self._is_api_key_valid():
            print("api key is valid")
            session = requests.Session()
            session.auth = (self.apiKey, 'X')

            return session

        else:
            raise ValueError("Must provide correct API Key")

    def _is_api_key_valid(self):
        """
        Returns boolean on api key validility
        """

        r = requests.get(
            'https://app.handshake.com',
            auth=(self.apiKey, 'X'))

        if r.status_code == 200:
            return True

        else:
            return False

    def get_products(self, sku=None):
        """
        Returns product/s
        Depending on whether a sku is passed
        """
        r = self.session.get(
            'https://app.handshake.com/api/latest/items')
        res = r.json()

        products = res['objects']

        while res['meta']['next'] is not None:
            r = self.session.get(
                'https://app.handshake.com{}'.format(
                    res['meta']['next']))
            res = r.json()

            products.extend(res['objects'])

        return products

    def get_full_inventory_list(self):
        """
        Returns list of all inventory items
        """

        r = self.session.get(
            'https://app.handshake.com/api/latest/item_stock_units')
        res = r.json()

        inventory = res['objects']

        while res['meta']['next'] is not None:
            r = self.session.get(
                'https://app.handshake.com/api/latest/item_stock_units')
            res = r.json()

            inventory.extend(res['objects'])

    def get_full_customer_list(self):
        """
        Returns list of all customers objects
        """

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
        """
        Returns last 5 orders objects in a list
        """

        r = self.session.get(
            'https://app.handshake.com/api/latest/orders'
            '?order_by=-ctime&limit=5')
        res = r.json()

        return res['objects']

    def create_new_product_category_id(self):
        """
        Creates a new product category in product tree
        returns object id of new category
        """

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

    def change_order_status(self, order_id, old_status, new_status):
        """
        Takes in the order id and changes the status of that order
        using the passed in old status and new status
        """
        payload = {
            "old": old_status,
            "new": new_status
        }

        r = self.session.post(
            'https://app.handshake.com/api/latest/orders/{}/'
            'actions/changeStatus'.format(order_id),
            json=payload)

        r

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
