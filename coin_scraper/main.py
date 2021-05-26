"""
Title: Coin Scraper
Author: Luke Sexton
GitHub:https://github.com/valentina-valentine

CoinMarketCap Developers: https://pro.coinmarketcap.com/
CoinMarketCap API: https://coinmarketcap.com/api/
CoinMarketCap Best practices: https://coinmarketcap.com/api/documentation/v1/#section/Best-Practices

Telegram Bot API: https://core.telegram.org/bots

Description: Coin Scraper utilizes the Coin Market Cap API to retrieve the costs of specified cryptocurrencies
periodically and notifies the user when the price has changed by a specified percentage.
"""
# Imports
import atexit
import decimal
import logging
import sys
import time

import requests
from prettytable import PrettyTable

from config import coin_ids, currency_precisions, headers, message_types, parameters, percentage_threshold, \
    quotes_latest_url, sleep_time, telegram_bot_id, telegram_channel_id, telegram_url, titles


def add_initial_coins(scraped_coins):
    """Return dictionary of initial scraped coins"""
    dictionary = {}
    for key, value in scraped_coins.items():
        dictionary[key] = value
    return dictionary


def calculate_decreased_threshold(price):
    """Decrease price by threshold percentage"""
    return price + (-percentage_threshold * price)


def calculate_increased_threshold(price):
    """Increase price by threshold percentage"""
    return price + (percentage_threshold * price)


def calculate_percent_increase(original_value, new_value):
    """Return percentage value increase of new value from original value"""
    increase = new_value - original_value
    percent = (increase / original_value) * 100
    return '{:.2f}'.format(percent)


def calculate_percent_decrease(original_value, new_value):
    """Return percentage value decrease of new value from original value"""
    decrease = original_value - new_value
    percent = (decrease / original_value) * 100
    return '{:.2f}'.format(percent)


def check_for_changes(existing_coins, scraped_coins):
    """Return dictionary of currencies whose values have changed beyond the threshold"""
    changes = []
    table = PrettyTable(['Name', 'Price', 'Increase Threshold', 'Decrease Threshold'])

    for existing_name, existing_price in existing_coins.items():
        # Set increased price (float): current price + threshold percentage
        increased_price_threshold = calculate_increased_threshold(existing_price)
        # Set decreased price (float): current price - threshold percentage
        decreased_price_threshold = calculate_decreased_threshold(existing_price)
        # Add thresholds to table
        table.add_row([existing_name, existing_price, increased_price_threshold, decreased_price_threshold])
        # Check if existing coin is in the scraped coin dictionary
        if existing_name in scraped_coins.keys():
            scraped_price = scraped_coins[existing_name]
            # Check if scraped price breaches threshold to add to changes dictionary
            if scraped_price > increased_price_threshold:  # Big increase
                # Calculate percent increase
                percentage = calculate_percent_increase(existing_price, scraped_price)
                # Create and add row to changes list of lists
                change = [existing_name, scraped_price, message_types['increase'], percentage]
                changes.append(change)
            elif scraped_price < decreased_price_threshold:  # Big decrease
                # Calculate percent increase
                percentage = calculate_percent_decrease(existing_price, scraped_price)
                # Create and add row to changes list of lists
                change = [existing_name, scraped_price, message_types['decrease'], percentage]
                changes.append(change)
            # Log smaller changes if applicable
            elif existing_price < scraped_price:  # Small increase
                log_small_change(existing_name, existing_price, scraped_price)
            elif existing_price > scraped_price:  # Small decrease
                log_small_change(existing_name, existing_price, scraped_price)
            else:  # No change
                print(">>> No change... Existing Price:", existing_price, "Scraped Price:", scraped_price)
    table.align = 'l'
    print(table)
    return changes


def get_max_value_string_length(dictionary):
    """Return max value of string length in given dictionary"""
    max_value = 0
    for value in dictionary.values():
        length = len(value)
        if length > max_value:
            max_value = length
    return max_value


def initialize_telegram_logger():
    """Initialize logger for Telegram"""
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def log_dictionary(dictionary):
    """Log given dictionary to console"""
    table = PrettyTable(['Name', 'Price'])
    for key, value in dictionary.items():
        table.add_row([key, value])
    print(table)


def log_small_change(name, existing_price, scraped_price):
    """Log small change of scraped price to console"""
    print(">>> Slight Change!\tName: ", name, "\tExisting Price:", existing_price, "\tScraped Price:", scraped_price)


def log_title(title):
    """Log title to console"""
    multiplier = 3
    print("")
    print(title.center(MAX_TITLE_LENGTH * multiplier, '*'))
    print("")


def notify_script_start():
    """Notify script start to Telegram group"""
    message = "Coin Scraper script has started!"
    post_telegram_request(message)


def notify_script_stop():
    """Notify script stop to Telegram group"""
    message = "Coin Scraper script has stopped!"
    post_telegram_request(message)


def notify_telegram(changes):
    """Send message to Telegram group"""
    print(">>> Notifying Telegram!")

    for row in changes:
        # Row elements: Name, Price Type, Percentage
        # Format price to currency
        decimal_price = to_decimal(row[0], row[1])
        currency = to_currency(decimal_price)

        message = "{0} New Price: {1} - {2} by {3}%".format(row[0].upper(), currency, row[2], row[3])
        post_telegram_request(message)


def post_telegram_request(message):
    """Post request to Telegram channel"""
    post_parameters = {'chat_id': telegram_channel_id, 'text': message}
    try:
        requests.post(telegram_url + telegram_bot_id + "/" + 'sendMessage?', data=post_parameters)
    except requests.exceptions.RequestException:
        print('>>> Error sending message to Telegram...')


def request_coin_data():
    """Return dictionary of coin names and prices from API call"""
    print("Requesting coin data")
    # Initialize scraped coin dictionary
    coin_dictionary = {}
    # Initialize session and update headers
    try:
        # Send GET request and retrieve coin data
        response = requests.get(quotes_latest_url, params=parameters, headers=headers, timeout=5).json()
        data = response['data']
        for coin_id in coin_ids:
            # Get coin name and price
            name = data[coin_id]['name']
            price = data[coin_id]['quote']['AUD']['price']
            # Add to coin dictionary
            coin_dictionary[name] = price
        return coin_dictionary
    except (requests.ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
        print(e)


def sleep_and_log(seconds):
    """Sleep for given time and log text to console"""
    start = seconds
    stop = 0
    step = -1
    log_title(titles['sleep'])
    print('>>> Checking again in...')
    for i in range(start, stop, step):
        print('>>>', i, 'seconds...')
        time.sleep(1)


def to_decimal(name, price):
    """Return given price in decimal form"""
    if name in currency_precisions:
        context = decimal.Context()
        context.prec = currency_precisions[name]
        price = context.create_decimal_from_float(price)
    return price


def to_currency(price):
    """Return given price formatted to currency"""
    return '${:,}'.format(price)


def update_existing_coin_dictionary(existing_coins, changes):
    """Return updated coins dictionary"""
    for row in changes:
        name = row[0]
        price = row[1]
        # Find coin name in existing dictionary
        if name in existing_coins:
            # Update price in existing dictionary
            existing_coins[name] = price
    return existing_coins


MAX_TITLE_LENGTH = get_max_value_string_length(titles)  # For title formatting purposes
if __name__ == '__main__':
    log_title(titles['start'])
    # Initialize logger and notify Telegram script has started
    initialize_telegram_logger()
    notify_script_start()
    # Initialize empty dictionary when script first runs
    existing_coin_dictionary = {}
    # Set handler to notify Telegram that script has stopped
    atexit.register(notify_script_stop)
    # Start console logging
    log_title(titles['dictionary_existing'])
    log_dictionary(existing_coin_dictionary)
    # Run until cancelled
    while True:
        try:
            # Get coin names and prices
            log_title(titles['scrape'])
            scraped_coin_dictionary = request_coin_data()
            # Log scraped dictionary
            log_dictionary(scraped_coin_dictionary)
            # Get all changes if thresholds are breached
            log_title(titles['check_changes'])
            # Check if existing coin dictionary is empty
            if not bool(existing_coin_dictionary):
                # Existing coin dictionary is empty. Add initial coins
                existing_coin_dictionary = add_initial_coins(scraped_coin_dictionary)
            else:
                # Get changes
                coin_changes = check_for_changes(existing_coin_dictionary, scraped_coin_dictionary)
                print('>>> Coin changes: ', coin_changes)
                # Check if there are any coin changes
                if bool(coin_changes):
                    # Change exists
                    existing_coin_dictionary = update_existing_coin_dictionary(existing_coin_dictionary, coin_changes)
                    log_dictionary(existing_coin_dictionary)
                    # Notify changes to telegram
                    notify_telegram(coin_changes)

            # Sleep for specified time before starting again
            sleep_and_log(sleep_time)
        except KeyboardInterrupt:
            log_title(titles['stop'])
            notify_script_stop()
            print(">>> Script stopping... Goodbye...")
            sys.exit()
