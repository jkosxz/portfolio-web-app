import os
import finnhub
from .db_utils import load_symbols

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
apikey = open('investments/api_utils/apikeys/finnhub').read()

finnhub_client = finnhub.Client(api_key=apikey)


def get_all_symbols():
    return finnhub_client.stock_symbols('US')
