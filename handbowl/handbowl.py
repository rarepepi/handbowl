# Fishbowl and Handshake custom integration by Pepi
import os
import csv
import requests
import config
import sys

from datetime import datetime
from utils import run_once
from progress.bar import ChargingBar
from utils import logo


@run_once
def get_hs_category_id():
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
        print("Error: {}".format(e))


def get_hs_products():
    try:
        # Get first 100 hs products
        print("Product Sync :")
        r = requests.get('https://app.handshake.com/api/latest/items', auth=(
            config.HANDSHAKE['APIKEY'], 'X'))

        res = r.json()
        hs_products = res['objects'][:]
        print("Total Amount: {}".format(res['meta']['total_count']))
        product_bar = ChargingBar(
            'Downloading Products', max=res['meta']['total_count']/100,
            suffix='%(percent).1f%% - %(elapsed_td)s')
        product_bar.next()
        # Use the next url to get the next 100 products
        while res['meta']['next'] is not None:
            r = requests.get(
                'https://app.handshake.com{}'.format(res['meta']['next']),
                auth=(config.HANDSHAKE['APIKEY'], 'X'))

            res = r.json()
            hs_products.extend(res['objects'])
            product_bar.next()

    except requests.exceptions.ConnectionError as e:
        print("Error: get_hs_products connection error!")
        sys.exit()

    # Return the full list of products
    product_bar.finish()
    return hs_products


def get_hs_customers():
    try:
        # Get first 100 hs customers
        r = requests.get(
            'https://app.handshake.com/api/latest/customers',
            auth=(config.HANDSHAKE['APIKEY'], 'X'))
        res = r.json()
        hs_customers = res['objects']
        print("Total Amount: {}".format(res['meta']['total_count']))

        customer_bar = ChargingBar(
            'Updating Customers', max=res['meta']['total_count']/100,
            suffix='%(percent).1f%% - %(elapsed_td)s')
        customer_bar.next()

        # Use the next url to get the next 100 customers
        while res['meta']['next'] is not None:
            r = requests.get(
                'https://app.handshake.com{}'.format(res['meta']['next']),
                auth=(config.HANDSHAKE['APIKEY'], 'X'))

            res = r.json()
            hs_customers.extend(res['objects'])
            customer_bar.next()

    except requests.exceptions.ConnectionError as e:
        print("Error: get_hs_products connection error!")
        sys.exit()

    # Return the full list of customers
    customer_bar.finish()
    return hs_customers


def get_hs_orders(amount):
    try:
        r = requests.get("https://app.handshake.com/api/latest/orders"
            "?order_by=-ctime&limit={}".format(amount),
            auth=(config.HANDSHAKE['APIKEY'], 'X'))
        res = r.json()

    except requests.exceptions.ConnectionError as e:
        print("Error: hs get order connection error!")
        sys.exit()

    return res['objects']


def get_fb_products():
    # Open and return fishbowl products csv
    with open('data/products/fb_products.csv', 'r') as csvfile:
        fb_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(fb_reader)
        fb_products = list(fb_reader)

        return fb_products


def get_fb_customers():
    # Open and return fishbowl customers
    with open('data/customers/fb_customers.csv', 'r') as csvfile:
        fb_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(fb_reader)
        fb_customers = list(fb_reader)

    return fb_customers


def create_fb_order(order):  
    first_header = [
        "Flag", "SONum", "Status", "CustomerName",
        "CustomerContact", "BillToName", "BillToAddress", "BillToCity",
        "BillToState", "BillToZip", "BillToCountry", "ShipToName",
        "ShipToAddress", "ShipToCity", "ShipToState", "ShipToZip",
        "ShipToCountry", "ShipToResidential", "CarrierName", "TaxRateName",
        "PriorityId", "PONum", "VendorPONum", "Date", "Salesman",
        "ShippingTerms", "PaymentTerms", "FOB", "Note", "QuickBooksClassName",
        "LocationGroupName", "FulfillmentDate", "URL", "CarrierService",
        "DateExpired", "Phone", "Email", "CF-Custom"
        ]

    second_header = [
        "Flag", "SOItemTypeID", "ProductNumber", "ProductDescription",
        "ProductQuantity", "UOM", "ProductPrice", "Taxable", "TaxCode",
        "Note", "QuickBooksClassName", "FulfillmentDate", "ShowItem",
        "KitItem", "RevisionLevel"
        ]

    # Gather customer and order info into variables
    order_id = order['id'].strip('#')
    customer_name = order['customer']['name']
    customer_address = order['billTo']['street']
    customer_city = order['billTo']['city']
    customer_state = order['billTo']['state']
    customer_zip = order['billTo']['postcode']
    customer_country = order['billTo']['country']
    normalized_date = order['cdate'][5:7] + \
        order['cdate'][7:10].replace('-', '/') + "/" + order['cdate'][:4]
    sales_rep = order['ownerName']
    payment_terms = order['paymentTerms']
    customer_phone = order['billTo']['phone']
    customer_email = order['customer']['email']

    customer_info = [
        "SO", order_id, '20', customer_name,
        customer_name, customer_name, customer_address, customer_city,
        customer_state, customer_zip, customer_country, customer_name,
        customer_address, customer_city, customer_state,
        customer_zip, customer_country, 'false', 'UW Truck', 'None', '30',
        '', '', normalized_date, sales_rep, "Invoiced", payment_terms,
        'Origin', '', 'None', 'Main', normalized_date, '', '', '',
        customer_phone, customer_email, ''
     ]

    products = order['lines']

    filename = "orders/SO_{}.csv".format(order['id'])

    with open(filename, 'w') as csvfile:
        so = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)

        so.writerow(first_header)
        so.writerow(second_header)
        so.writerow(customer_info)

        for product in products:
            product_info = [
                'Item', 10, product['sku'], product['description'],
                str(product['qty']), 'ea', product['unitPrice'], 'false',
                'NON', product['notes'], 'None', normalized_date, 'true',
                'false'
                ]

            so.writerow(product_info)
    print("Fishbowl csv created for order {}".format(order['id']))


def create_missing_hs_products(hs, fb):
    missing_products = []

    for product in fb:
        if not any(dict['sku'] == product[0] for dict in hs):
            try:
                temp_id_date = get_hs_category_id()
            except requests.exceptions.ConnectionError as e:
                print("Error: catergory_id connection error!")
                sys.exit()


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


def update_hs_product_inventory(fb):
    for product in fb_products:
        if any(dict['sku'] == product[0] for dict in hs_products):
            data = {
                "idk": "find out"
            }
            try:
                r = requests.patch('')

            except requests.exceptions.ConnectionError as e:
                print("Error: get_hs_products connection error!")
                sys.exit()

def create_fb_sales_orders(hs):
    for order in hs:
        if order['status'] == "Confirmed":
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

                create_sales_csv(order)

            except requests.exceptions.ConnectionError as e:
                print("Error: hs order status connection error!")
                sys.exit()

def create_missing_fb_customers():
    pass

def main():
    # Product Sync
    hs_products = get_hs_products()
    # https://app.hand?shake.com/api/latest/item_stock_units
    fb_products = get_fb_products()
    # fb_inventory = get_fb_products()

    create_missing_hs_products(hs_products, fb_products)
    # update_hs_product_inventory(fb_inventory)

    # Customer Sync
    # hs_customers = get_hs_customers()
    # fb_customers = get_fb_customers()

    # create_missing_fb_customers(hs_customers, fb_customers)

    # Order Sync
    # confirmed_hs_orders = get_hs_orders()

    # create_fb_sales_orders(confirmed_hs_orders)


if __name__ == '__main__':
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    print(logo)
    main()
