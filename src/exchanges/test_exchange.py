from src.exchanges.exchange import Exchange
import random


class TestExchange(Exchange):
    def __init__(self,
                 name,
                 tickers_map={"BTC": ("BTC", ("EUR", "USD")),
                              "ETH": ("ETH", ("EUR", "USD")),
                              "XRP": ("XRP", ("EUR", "USD")),
                              "DASH": ("DASH", ("EUR", "USD"))},
                 fees=None):
        super().__init__(name, tickers_map, fees)

    def fetch_price(self, crypto, fiat):
        ticker_pair = self.__get_ticker_pair(crypto, fiat)
        if ticker_pair == "ETHUSD":
            return random.uniform(900, 1100)
        elif ticker_pair == "XRPUSD":
            return random.uniform(2.5, 3.5)
        elif ticker_pair == "XRPEUR":
            return random.uniform(2, 3)
        elif ticker_pair == "BTCUSD":
            return random.uniform(15500, 18000)
        elif ticker_pair == "DASHUSD":
            return random.uniform(1300, 1600)
        return -1

    def __get_ticker_pair(self, crypto, fiat):
        return crypto+fiat
