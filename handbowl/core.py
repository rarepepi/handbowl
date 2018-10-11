# Fishbowl and Handshake custom integration by Pepi
import os
import handshake as hand
import fishbowl as bowl

from utils import logo


def main():

    # Read the config file for settings and keys
    # start the handshake api and the fishbowl api
    # for handshake pass in the api key and server setting for fishbowl ? both from config file

    # Check if handshake api key is valid and fishbowl connection is good
    # if so then continue sync

# if orders sync then customers and products have to sync no matter what
    # if product sync is true
    # then run product sync
        # for every prodcut in fb check if hs has it if not then add it as a new one
            # you can do that by checking if the url for that sku hs api call returns null or no product
        # for every product in fishbowl get the current stock amount and pass that through a post request to hs
            # make a hs method call update_inventory(sku, amount)

    # if customer sync is true
    # then run customer sync
        # for every customer id in hs check if fb has it, if not then add it as a new customer
            # fishbowl api: create_customer(dict)

    # if order sync is true
    # then run order sync
        # check for the last 5 orders and if they are confimered then new_sales_order(dict)

    # Product Sync
    hs_products = hand.get_products()
    fb_products = bowl.get_products()
    fb_inventory = bowl.get_inventory()

    hand.create_missing_products(hs_products, fb_products)
    hand.update_product_inventory(fb_inventory)

    # Customer Sync
    hs_customers = hand.get_customers()
    fb_customers = bowl.get_customers()

    # bowl.create_missing_customers(hs_customers, fb_customers)

    # Order Sync
    hs_orders = hand.get_orders(3)
    for order in hs_orders:
        if order['status'] == 'Confirmed':
            bowl.create_order(order)
            hand.update_order_status(order)


if __name__ == '__main__':
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    print(logo)
    main()
