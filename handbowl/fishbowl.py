import csv
from requests_xml import XLMSession


class Request():
    """
    Contains methods that
    return proper fishbowl xml requests
    """
    pass
class Client():
    """ This is a wrapper
    for the Fishbowl XML API"""

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = _init_session()

    def _init_session(self):
        session = XLMSession()
        return session

    def get_products():
        # Open and return fishbowl products csv
        with open('../../products/fb_products.csv', 'r') as csvfile:
            fb_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(fb_reader)
            fb_products = list(fb_reader)

            return fb_products

    def get_inventory():
        # Open and return fishbowl inventory csv
        with open('../../products/fb_inventory.csv', 'r') as csvfile:
            fb_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(fb_reader)
            fb_inventory = list(fb_reader)

            return fb_inventory

    def get_customers():
        # Open and return fishbowl customers
        with open('../../customers/fb_customers.csv', 'r') as csvfile:
            fb_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(fb_reader)
            fb_customers = list(fb_reader)

        return fb_customers

    def create_order(order):
        first_header = [
            "Flag", "SONum", "Status", "CustomerName",
            "CustomerContact", "BillToName", "BillToAddress", "BillToCity",
            "BillToState", "BillToZip", "BillToCountry", "ShipToName",
            "ShipToAddress", "ShipToCity", "ShipToState", "ShipToZip",
            "ShipToCountry", "ShipToResidential", "CarrierName", "TaxRateName",
            "PriorityId", "PONum", "VendorPONum", "Date", "Salesman",
            "ShippingTerms", "PaymentTerms", "FOB", "Note",
            "QuickBooksClassName", "LocationGroupName",
            "FulfillmentDate", "URL", "CarrierService",
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
        normalwwwswwwerdtsewaehkuiytreiop0'[
        l;'kj']

        products = order['lines']

        filename = "../../orders/SO_{}.csv".format(order['id'])

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


    # def create_missing_customers(hs_customers, fb_customers):
    #     for customer in hs_customers:
    #         if not any
