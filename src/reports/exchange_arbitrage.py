import src.utils.currency_converter as currency_converter


class ExchangeArbitrage:
    def __init__(self, exchanges):
        self.exchanges = exchanges
        self.spreads = []

    def run_intra_exchange_arbitrage(self, name):
        if len(self.spreads):
            self.spreads = []

        exchange = None
        for ex in self.exchanges:
            if ex.name == name:
                exchange = ex

        if not exchange:
            print("Did not find exchange {}".format(name))
            return

        currencies = exchange.get_currencies()
        crypto_prices = self.__get_all_prices(exchange, [], currencies)
        self.spreads = self.__get_spreads(crypto_prices)

        return "Intra exchange arbitrage:\n" + self.__format_spreads(self.spreads)

    def run_multi_exchange_arbitrage(self):
        if len(self.spreads):
            self.spreads = []

        for i in range(len(self.exchanges)):
            for j in range(i + 1, len(self.exchanges)):
                # Get common currencies
                e1, e2 = self.exchanges[i], self.exchanges[j]
                currencies = self.__get_common_currencies(e1, e2)

                # Fetch currency price
                crypto_prices = self.__get_all_prices(e1, e2, currencies)

                # Calculate spread opportunity
                self.spreads += self.__get_spreads(crypto_prices)

        return "Inter CEX arbitrage:" + self.__format_spreads(self.spreads)

    def __get_common_currencies(self, e1, e2):
        e1_cur = e1.get_currencies()
        e2_cur = e2.get_currencies()
        return set(e1_cur).intersection(e2_cur)

    def __get_all_prices(self, e1, e2, currencies, base_currency='EUR'):
        prices = {}
        for crypto in currencies:
            prices[crypto] = []
            for exchange in (e1, e2):
                if not exchange:
                    continue

                for fiat in exchange.get_fiats(crypto):
                    key = "{}:{}{}".format(exchange.name, crypto, fiat)
                    price = exchange.fetch_price(crypto, fiat)
                    converted_price = price
                    if fiat != base_currency:
                        converted_price = currency_converter.exchange_currencies(price, fiat, base_currency)
                    if price:
                        prices[crypto].append((key, (price, converted_price)))
        return prices

    def __get_spreads(self, crypto_prices):
        spreads = []
        for crypto in crypto_prices:
            prices = crypto_prices[crypto]
            for i, (first_pair, (first_native_price, first_price)) in enumerate(prices):
                for second_pair, (second_native_price, second_price) in prices[min(i+1, len(prices)):]:
                    if first_pair == second_pair:
                        continue
                    spread = max(first_price / second_price,
                                 second_price / first_price) -1

                    spreads.append((first_pair,
                                    second_pair,
                                    first_price,
                                    second_price,
                                    first_native_price,
                                    second_native_price,
                                    100 * spread))
        return spreads

    def __format_spreads(self, spreads):
        #  First sort list
        spreads.sort(key=lambda tup: -tup[-1])

        #TODO: Changer: ne pas formter sure spreads au dessus, mais l
        # le faire ici. Faire BUY pair and SELL pair as well en triant
        header = ('BUY', 'O. PRICE','C. PRICE', 'SELL', 'O. PRICE', 'C. PRICE', 'SPREAD')
        for i in range(len(spreads)):
            low_pair, high_pair, \
             low_price, high_price, \
             low_native_price, high_native_price, spread = spreads[i]

            if low_price > high_price:
                low_price, high_price = high_price, low_price
                low_pair, high_pair = high_pair, low_pair
                low_native_price, high_native_price = high_native_price, low_native_price

            spreads[i] = (low_pair,
                          round(low_native_price, 2),
                          round(low_price, 2),
                          high_pair,
                          round(high_native_price, 2),
                          round(high_price, 2),
                          round(spread, 2))

        return "\n".join("\t".join(map(str,spread)) for spread in [header] + spreads)
