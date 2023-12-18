import os
import finnhub

apikey = open('investments/api_utils/apikeys/finnhub').read()

finnhub_client = finnhub.Client(api_key=apikey)

def get_all_symbols():
    return finnhub_client.stock_symbols('US')
