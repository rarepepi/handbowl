import os
import config
from handshake import Client as hs_client
from fishbowl import Client as fb_client
from utils import logo


def main():
    hand = hs_client(config.handshake['key'], config.handshake['password'])
    bowl = fb_client(
        config.fishbowl['host'],
        config.fishbowl['user'],
        config.fishbowl['password']
    )


if __name__ == '__main__':
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print(logo)
    main()
