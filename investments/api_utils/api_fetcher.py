import os
import finnhub

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
apikey = open('investments/api_utils/apikeys/finnhub').read()

finnhub_client = finnhub.Client(api_key=apikey)


def get_all_symbols():
    return finnhub_client.stock_symbols('US')


def get_prices(array_of_symbols):  # format SYMBOL, current_PRICE
    res = {}
    for symbol in array_of_symbols:
        res[symbol] = dict(finnhub_client.quote(symbol))

    return res


def get_current_prices(array_of_symbols_and_prices):
    res = {}
    for item, values in array_of_symbols_and_prices.items():
        for value in values:
            res[item] = values['c']
    print(res)


print(get_prices(['AAPL', 'NVDA']))
get_current_prices(get_prices(['AAPL', 'NVDA']))
