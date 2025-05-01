import asyncio
from datetime import datetime
from typing import Dict
from cryptofeed import FeedHandler
from cryptofeed.defines import L2_BOOK
from cryptofeed.exchanges import Binance

orderbook_data: Dict[str, Dict] = {}

async def orderbook_callback(book, receipt_timestamp):
    orderbook_data[book.symbol] = {
        "exchange": book.exchange,
        "symbol": book.symbol,
        "timestamp": str(datetime.fromtimestamp(receipt_timestamp)),
        "bids": {f"{price:.2f}": book.book.bids[price] for price in sorted(book.book.bids.keys(), reverse=True)},
        "asks": {f"{price:.2f}": book.book.asks[price] for price in sorted(book.book.asks.keys())}
    }

def get_orderbook_data(symbol: str):
    return orderbook_data.get(symbol)

async def run_feed():
    f = FeedHandler()
    f.add_feed(Binance(
        symbols=['BTC-USDT'],
        channels=[L2_BOOK],
        max_depth=1000,
        callbacks={L2_BOOK: orderbook_callback}
    ))
    f.run(start_loop=False)
