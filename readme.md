# Handbowl

Handbowl connects Handshake B2B Sales to Fishbowl Inventory by using the Handshake API and creating import spreadsheets for Fishbowl.

### Setup/Usage

1. Clone the project into ~/Documents folder of user with fishbowl client

2. Set Fishbowl Schedule module settings:
    export(products) --> ~/Documents/products/fb_product.csv

    export(inventory) --> ~/Documents/products/fb_inventory.csv

    import(customers) --> ~/Documents/customers/hs_customers.csv

    import(orders) --> ~/Documents/orders/SO_*.csv

3. Set windows task to run handbowl/core.py every 10   
mins