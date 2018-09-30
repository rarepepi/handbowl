# Fishbowl and Handshake custom integration by Pepi
import os
import handshake as hand
import fishbowl as bowl

from utils import logo


def main():
    # Product Sync
    hs_products = hand.get_products()
    fb_products = bowl.get_products()
    fb_inventory = bowl.get_inventory()

    hand.create_missing_products(hs_products, fb_products)
    hand.update_product_inventory(fb_inventory)

    # Customer Sync
    # hs_customers = hand.get_customers()
    # fb_customers = bowl.get_customers()

    # bowl.create_missing_customers(hs_customers, fb_customers)

    # Order Sync
    # hs_orders = hand.get_orders(3)
    # for order in hs_orders:
    #     if order['status'] == 'Confirmed':
    #         bowl.create_order(order)
    #         hand.update_order_status(order)


if __name__ == '__main__':
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    print(logo)
    main()
