from config.config import binance_api_key, binance_api_secret, bybit_api_key, bybit_api_secret
from exchange.binance import BinanceClient
from exchange.bybit import BybitClient
from arbitrage.arbitrage_service import ArbitrageService
import ccxt
import asyncio
# from arbitrage import execute_arbitrage_strategy


async def main():
    # Initialize Binance and Bybit clients
    bybit = ccxt.bybit({
        'apiKey': bybit_api_key,
        'secret': bybit_api_secret,
        'enableRateLimit': True
    })
    binance = ccxt.binance({
        'options': {
            'defaultType': 'future',
        },
    })
    binance_client = BinanceClient(binance)
    bybit_client = BybitClient(bybit)
    arbitrage_service = ArbitrageService(binance_client, bybit_client)

    while True:
        await arbitrage_service.compare_prices()
        await asyncio.sleep(2)
    # await arbitrage_service.compare_prices()

if __name__ == "__main__":
    asyncio.run(main())
