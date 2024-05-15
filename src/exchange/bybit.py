import requests
import ccxt
from config.config import money_per_trade, stop_money_threshold, leverage
import ccxt.base as ccxt_base
from log.logger import Logger


class BybitClient:
    def __init__(self, bybit):
        self.bybit = bybit
        self.base_url = 'https://api.bybit.com'
        self.exchange = self.bybit
        self.logger = Logger()

    def get_all_symbols_perceptual(self) -> dict[str, float]:
        exchange = self.exchange
        tickers = exchange.fetch_tickers()
        symbol_volume = {}
        symbols_with_prices = {}
        for symbol, ticker in tickers.items():
            if (symbol.endswith(":USDT")):
                symbols_with_prices[symbol] = ticker['last']
                symbol_volume[symbol] = ticker['quoteVolume']

        return symbols_with_prices, symbol_volume

    def get_symbol_volume(self, symbol: str) -> float:
        exchange = self.exchange  # Replace with the appropriate exchange you're using
        ticker = exchange.fetch_ticker(symbol)
        symbol_volume = ticker['quoteVolume']
        return symbol_volume

    def get_symbol_liquidity(self, symbol: str) -> float:
        exchange = self.exchange  # Replace with the appropriate exchange you're using
        order_book = exchange.fetch_order_book(symbol)
        # Example: Using top bid and ask liquidity
        symbol_liquidity = order_book['bids'][0][1] + order_book['asks'][0][1]
        return symbol_liquidity

    def place_order(self, symbol, price, side):
        self.logger.info("Start placing order-------------------------------")
        balance = self.exchange.fetch_balance(params={'type': 'future'})
        # Retrieve the USDT balance
        usdt_balance = balance['total']['USDT']
        if usdt_balance <= stop_money_threshold:
            self.logger.warning(
                f"Account do not have enough balance:  {usdt_balance}. Skipping order placement.")
            return

        # Set the take profit and stop loss percentages
        take_profit_percentage = 0.25
        stop_loss_percentage = 0.25

        # Calculate the take profit and stop loss prices
        if side == "buy":
            take_profit_price = price * (1 + (take_profit_percentage / 100))
            stop_loss_price = price * (1 - (stop_loss_percentage / 100))
        elif side == "sell":
            take_profit_price = price * (1 - (take_profit_percentage / 100))
            stop_loss_price = price * (1 + (stop_loss_percentage / 100))
        positions = self.exchange.fetch_positions()
        for position in positions:
            if position['symbol'] == symbol:
                self.logger.warning(
                    f"Position already exists for symbol {symbol}. Skipping order placement.")
            return
        try:
            opening_order = self.exchange.create_order(symbol, 'market', side, (money_per_trade/price)*leverage*0.8, None,  params={
                                                       'leverage': leverage, 'stopLoss': str(stop_loss_price), 'takeProfit': str(take_profit_price)})
            opening_order_id = opening_order['info']['orderId']
            self.logger.info(
                f"{side} {(money_per_trade/price)*leverage*0.8} {symbol} at {price}: id {opening_order_id}")
            self.logger.info(
                f"setting {symbol} sl and tp at {stop_loss_price} and {take_profit_price}.")
        except Exception as e:
            self.logger.error(
                f"Error occurred while placing the order {symbol}: {e}")
            return

    def get_account_balance(self) -> float:
        # Fetch the account balance
        balance = self.bybit.fetch_balance()
        usdt_balance = balance['USDT']['total']

        return usdt_balance

    def get_ticker_price(self, symbol):
        endpoint = '/v2/public/tickers'
        params = {'symbol': symbol}
        response = requests.get(self.base_url + endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            for ticker in data['result']:
                if ticker['symbol'] == symbol:
                    return float(ticker['last_price'])
            raise Exception('Symbol not found in Bybit response')
        else:
            raise Exception('Failed to retrieve ticker price from Bybit')
