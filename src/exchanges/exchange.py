

class Exchange:

    def __init__(self,
                 name,
                 tickers_map={},
                 fees=None,
                 default_fiat="USD"):
        self.name = name
        self.tickers_map = tickers_map
        self.fees = fees
        self.default_fiat = default_fiat
        pass

    def fetch_price(self, crypto, fiat):
        pass

    def __get_ticker_pair(self, cur1, cur2):
        pass

    def get_currencies(self):
        return self.tickers_map.keys()

    def get_fiats(self, crypto):
        return self.tickers_map.get(crypto, set((None,())))[1]

    def __str__(self):
        return "{}: {}".format(self.name, self.tickers_map.keys())

