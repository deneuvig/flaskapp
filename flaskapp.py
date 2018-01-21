from flask import Flask
from src.exchanges.cryptonator_exchange import CryptonatorExchange
from src.reports.exchange_arbitrage import ExchangeArbitrage

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

if __name__ == '__main__':
    app.run()

@app.route('/arbitrage/<input_str>')
def arbitrage(input_str):
    exchanges = [
        CryptonatorExchange('Cex.io',
                        {'ETH': ('ETH', ('EUR', 'USD', 'GBP')),
                         'BTC': ('BTC', ('EUR', 'USD', 'GBP')),
                         'DASH': ('DASH', ('EUR', 'USD', 'GBP')),
                         'XRP': ('XRP', ('EUR', 'USD', 'GBP')),
                         'BCH': ('BCH', ('EUR', 'USD', 'GBP')),
                         'ZEC': ('ZEC', ('EUR', 'USD', 'GBP')),
                         'BTG': ('BTG', ('EUR', 'USD', 'GBP')),}
                        ),
        CryptonatorExchange('Kraken',
                        {'ETH': ('ETH', ('EUR',))}),
    ]
    arb_engine = ExchangeArbitrage(exchanges)
    arb_engine.run_intra_exchange_arbitrage('Cex.io')
    print("---")
    arb_engine.run_multi_exchange_arbitrage()

