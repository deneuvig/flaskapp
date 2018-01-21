from src.exchanges.exchange import Exchange
import requests


class CryptonatorExchange(Exchange):
    supported_exchanges = {
        'kraken' : 'Kraken',
        'cex.io' : 'Cex.io',
    }

    def fetch_price(self, crypto, fiat):
        api_uri = 'https://api.cryptonator.com/api/full/{}-{}'.format(crypto, fiat)
        api_response = requests.get(api_uri)

        exchange_name = CryptonatorExchange.supported_exchanges.get(self.name.lower())

        if not exchange_name:
            print('Unsupported exchange: {}'.format(self.name))
            return

        if api_response.status_code == 200:
            json = api_response.json()
            markets = json['ticker']['markets']
            for market in markets:
                if market['market'] == exchange_name:
                    return float(market['price'])