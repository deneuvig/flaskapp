from src.exchanges.exchange import Exchange
import requests


class CexioExchange(Exchange):

    def fetch_price(self, crypto, fiat):
        api_uri = 'https://cex.io/api/order_book/{}/{}'.format(crypto.upper(), fiat.upper())
        api_response = requests.get(api_uri)

        if api_response.status_code == 200:
            json = api_response.json()
            bids = json['bids']
            asks = json['asks']
            ask = None
            bid = None

            if len(asks):
                ask = asks[0][0]
            if len(bids):
                bid = bids[0][0]

            return float(bid), float(ask)

'''
ce = CexioExchange('krak',
                         {"ETH": ("ETH", ("EUR", "USD", 'GBP')),
                          "DASH": ("DASH", ("EUR", "USD"))},
                         'kraken'
                         )
p = ce.fetch_price('ETH', 'EUR')
print(p)
'''