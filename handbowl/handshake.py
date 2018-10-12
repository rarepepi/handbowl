import datetime
import requests
import config
import sys
from utils import run_once


@run_once
def get_category_id():
    date_prefix = "New Products | {}".format(
        datetime.now().strftime("%m/%d/%y"))

    data = {
        "name": date_prefix,
        "id": date_prefix,
        "categoryPosition": "0"
    }

    try:
        r = requests.post(
                'https://app.handshake.com/api/latest/categories',
                auth=(config.HANDSHAKE['APIKEY'], 'X'),
                json=data)

        res = r.json()
        category_id = res['objID']

        return category_id

    except requests.exceptions.ConnectionError as e:
        print("Error: Handshake get_category_id")
        sys.exit()


def update_order_status(order):
    payload = {
        "old": "Confirmed",
        "new": "Processing"
    }
    try:
        r = requests.post(
            'https://app.handshake.com/api/latest/orders/{}/'
            'actions/changeStatus'.format(order['id'].strip('#')),
            auth=('63a1ef5171d1827f37e0d2bcdc23c91a46e02b37', 'X'),
            json=payload)
        r.status_code

    except requests.exceptions.ConnectionError as e:
        print("Error: hs order status connection error!")
        sys.exit()


def create_missing_products(hs_products, fb_products):
    missing_products = []

    for product in fb_products:
        if not any(dict['sku'] == product[0] for dict in hs_products):
            temp_id_date = get_category_id()

            print("product missing in hs: {}".format(product[0]))
            if temp_id_date is not None:
                hs_category_id_and_name_date = temp_id_date[:]

            temp = {
                "category": {
                    "entityType": "Category",
                    "name": hs_category_id_and_name_date[1],
                    "id": hs_category_id_and_name_date[1],
                    "categoryPosition": 0,
                    "objID": hs_category_id_and_name_date[0]
                },
                "longDesc": product[2],
                "name": product[2],
                "sku": product[0],
                "unitPrice": product[5]
            }
            missing_products.append(temp)

    data = {
        "objects": missing_products
    }

    try:
        r = requests.patch(
            'https://app.handshake.com/api/latest/items',
            auth=(config.HANDSHAKE['APIKEY'], 'X'),
            json=data)
        r.status_code

    except requests.exceptions.ConnectionError as e:
        print("Error: catergory_id connection error!")
        sys.exit()


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
