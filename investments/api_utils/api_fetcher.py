import os
import finnhub
from investments.models import Asset
import requests


FINNHUB_APIKEY = open('investments/api_utils/apikeys/finnhub').read()
FINNHUB_CLIENT = finnhub.Client(api_key=FINNHUB_APIKEY)
COINMARKETCAP_API_URL = "https://pro-api.coinmarketcap.com/"

def get_all_symbols():
    """Fetches all stock symbols availble on Finnhub API"""
    return FINNHUB_CLIENT.stock_symbols('US')

def get_all_crypto(): # coinmarketcapp API
    """Fetches all crypto symbols availble on Coinmarketcap API"""
    r = requests.get(f"${COINMARKETCAP_API_URL}v2/cryptocurrency/quotes/latest", headers=open('investments/api_utils/apikeys/coinmarketcap').read())
    print(r)
 
def get_prices(array_of_symbols):  # argument as QueryList
    """
    Fetches latest quotes from Finnhub API
    array_of_symbols: array of symbols, output from get_all_symbols method
    """
    res = {}
    get_all_crypto()
    for symbol in list(array_of_symbols):
        res[str(symbol)] = dict(FINNHUB_CLIENT.quote(symbol))

    return res


def get_current_prices(array_of_symbols_and_prices):
    res = {}
    prices = get_prices(array_of_symbols_and_prices)

    for item, values in prices.items():
        res[item] = values['c']
    return res

