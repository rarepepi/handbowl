# Handbowl

Handbowl connects Handshake B2B Sales to Fishbowl Inventory through using the Handshake API and creating import files for Fishbowl.
The app is fully extendable and I encourage people to add to the project.

### Usage
	import handbowl

	hb = Handbowl('API KEY')
	
	fishbowl_products = handbowl.get_fishbowl_products()
	for product in fishbowl_products:
		handbowl.update_handshake_product()