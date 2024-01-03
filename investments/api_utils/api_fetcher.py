import os
import finnhub
from investments.models import Asset

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
apikey = open('investments/api_utils/apikeys/finnhub').read()

finnhub_client = finnhub.Client(api_key=apikey)


def get_all_symbols():
    return finnhub_client.stock_symbols('US')


def get_prices(array_of_symbols):  # argument as QueryList
    res = {}
    for symbol in list(array_of_symbols):
        res[str(symbol)] = dict(finnhub_client.quote(symbol))

    return res


def get_current_prices(array_of_symbols_and_prices):
    res = {}
    prices = get_prices(array_of_symbols_and_prices)

    for item, values in prices.items():
        res[item] = values['c']
    return res
