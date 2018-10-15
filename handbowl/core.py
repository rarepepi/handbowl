import os
import config
from handshake import Client
from utils import logo


def main():
    hand = Client(config.handshake['key'])
    print(hand.get_recent_orders())


if __name__ == '__main__':
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print(logo)
    main()
