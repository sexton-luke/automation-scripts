"""
Title: Find Coin Information
Author: Luke Sexton
GitHub: https://github.com/valentina-valentine

CoinMarketCap Developers: https://pro.coinmarketcap.com/
CoinMarketCap API: https://coinmarketcap.com/api/
CoinMarketCap Best practices: https://coinmarketcap.com/api/documentation/v1/#section/Best-Practices

Telegram Bot API: https://core.telegram.org/bots

Description: Use this script to get IDs of cryptocurrencies to follow best practices in main.py when using API
"""

import requests
from prettytable import PrettyTable

from config_ignore import id_map_url, find_coin_ids_parameters, headers

# Initialize symbols list from config file
symbols = [symbol for symbol in find_coin_ids_parameters['symbol'].split(',')]
try:
    # Initialize table
    table = PrettyTable(['ID', 'Name', 'Symbol', 'Slug'])
    # Send GET request
    response = requests.get(id_map_url, params=find_coin_ids_parameters, headers=headers).json()
    # Handle response data
    coins = response['data']
    # Get coin information from JSON data
    for coin in coins:
        if coin['symbol'] in symbols:
            coin_id = coin['id']
            table.add_row([coin['id'], coin['name'], coin['symbol'], coin['slug']])
    # Align and print table
    table.align = 'l'
    print(table)

except (ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
    print(e)
