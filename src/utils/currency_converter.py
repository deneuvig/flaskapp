import requests
from functools import lru_cache

SUPPORTED_CURRENCIES = {
    "EUR": "European euro",
    "USD": "US dollar",
    "GBP": "Pound sterling",
    "BRL": "Brazilian real"
}


CURRENCY_CODES = {
    1: "EUR",
    2: "USD",
    3: "GBP",
    4: "BRL"
}

APIKEY ='OhKLzGIYmwXD7bvqo8cohtd9PAPMPk5V'

@lru_cache(10)
def get_exchange_rate(base_currency, target_currency):
    if not (base_currency in SUPPORTED_CURRENCIES.keys()):
        raise ValueError("base currency {} not supported".format(base_currency))
    if not (target_currency in SUPPORTED_CURRENCIES.keys()):
        raise ValueError("target currency {} not supported".format(target_currency))

    if base_currency == target_currency:
        return 1
    api_uri = 'https://forex.1forge.com/1.0.2/convert?from={}&to={}&quantity=1&api_key={}'.format(
        base_currency, target_currency, APIKEY)
    api_response = requests.get(api_uri)

    if api_response.status_code == 200:
        return api_response.json()["value"]

def exchange_currencies(amount, src, trgt):
    if amount:
        return amount * get_exchange_rate(src, trgt)