# [COIN MARKET CAP API]
key = ''  # TODO: 1. Enter Personal API Key
quotes_latest_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'  # Endpoint For querying prices
id_map_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'  # Endpoint for querying coin information


# [TELEGRAM API]
telegram_url = 'https://api.telegram.org/bot'
telegram_bot_id = ''  # TODO: 1. Enter bot id here
telegram_bot_link = 't.me/@bot_name'  # Not needed, just a reference link
telegram_channel_id = '@channel_id'  # TODO: 3. Enter channel name here
telegram_channel_link = ''  # Not needed, just a reference link


# [FIND_COIN_INFORMATION.PY]
find_coin_ids_parameters = {
    'symbol': 'BTC,ETH,ADA,DOGE,XRP,DOT,SHIB,XLM,CAKE', }  # TODO: 4. Manually enter coin symbols you wish to track
currency_precisions = {'Bitcoin': 7, 'Ethereum': 6, 'Cardano': 4, 'Dogecoin': 3, 'XRP': 4, 'Polkadot': 4,
                       'SHIBA INU': 4, 'Stellar': 3, 'PancakeSwap': 4}  # For formatting messages to Telegram


#  [MAIN.PY]
parameters = {
    'id': '1,1027,2010,74,52,6636,5994,512,7186',
    'convert': 'AUD'}  # TODO: 5. Manually enter IDs from find_coin_information.py output
headers = {
    'Accepts': 'application/json',
    'Accept-Encoding': 'deflate,gzip',
    'X-CMC_PRO_API_KEY': key}
titles = {'check_changes': ' CHECKING FOR CHANGES', 'dictionary_existing': ' EXISTING COINS ',
          'dictionary_scraped': ' SCRAPED COINS ', 'name': '', 'scrape': ' SCRAPE INFORMATION ', 'start': ' START ',
          'sleep': ' SLEEPING ', 'small': " SMALL CHANGE"}  # Logging purposes
message_types = {'increase': 'Increase', 'decrease': 'Decrease', 'small_increase': 'Small Increase',
                 'small_decrease': 'Small Decrease'}
coin_ids = [coin_id for coin_id in parameters['id'].split(',')]
sleep_time = 300  # TODO: 6. Change time between iterations. Default checks every 5 minutes for free developer account
percentage_threshold = 0.03  # TODO: 7. Change to desired percentage you wished to be notified on
