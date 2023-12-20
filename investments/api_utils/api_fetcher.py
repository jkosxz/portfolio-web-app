import os
import finnhub
<<<<<<< HEAD
from .db_utils import load_symbols

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
apikey = open('investments/api_utils/apikeys/finnhub').read()

finnhub_client = finnhub.Client(api_key=apikey)

=======

apikey = open('investments/api_utils/apikeys/finnhub').read()

finnhub_client = finnhub.Client(api_key=apikey)
>>>>>>> e97ad1182e0e4750a3a41a97d41dc3702f89046e

def get_all_symbols():
    return finnhub_client.stock_symbols('US')
