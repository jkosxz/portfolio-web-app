import os
import finnhub
import db_utils as dbutl

apikey = open('api_utils/apikeys/finnhub').read()

finnhub_client = finnhub.Client(api_key=apikey)
print(finnhub_client.stock_symbols('US'))


def get_all_symbols():
    return finnhub_client.stock_symbols('US')


dbutl.load_symbols(get_all_symbols())
