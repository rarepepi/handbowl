import requests
from time import sleep
import config

r = requests.get(
    'https://app.handshake.com/api/latest/items?offset=4000',
    auth=(config.HANDSHAKE['APIKEY'], 'X'))
res = r.json()

print("Total Amount: {}".format(res['meta']['total_count']))

sleep(3)

while res['meta']['next'] is not None:
    r = requests.get(
        'https://app.handshake.com{}'.format(res['meta']['next']),
        auth=(config.HANDSHAKE['APIKEY'], 'X'))
    res = r.json()
    print(res['meta']['next'])
    print("Current batch: {}".format(res['meta']['offset']))
