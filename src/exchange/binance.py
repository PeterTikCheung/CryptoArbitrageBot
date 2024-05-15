import requests
import ccxt


class BinanceClient:
    def __init__(self, binance):
        self.base_url = 'https://api.binance.com'
        self.binance = binance

    def get_all_symbols_perceptual(self) -> dict[str, float]:
        exchange = self.binance
        symbols_with_prices = {}
        tickers = exchange.fetch_tickers()
        for symbol, ticker in tickers.items():
            if (symbol.endswith(":USDT")):
                symbols_with_prices[symbol] = ticker['last']

        return symbols_with_prices

    def get_ticker_price(self, symbol):
        endpoint = '/api/v3/ticker/price'
        params = {'symbol': symbol}
        response = requests.get(self.base_url + endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            return float(data['price'])
        else:
            raise Exception('Failed to retrieve ticker price from Binance')

    def create_order(self, symbol, side, quantity, price, order_type='LIMIT'):
        endpoint = '/api/v3/order'
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
            'price': price,
            'timeInForce': 'GTC',  # Good Till Cancelled
            'recvWindow': 5000,  # Optional parameter for request timeout
        }
        headers = {
            'X-MBX-APIKEY': self.api_key,
        }
        response = requests.post(
            self.base_url + endpoint, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception('Failed to create order on Binance')
