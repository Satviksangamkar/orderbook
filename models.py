from pydantic import BaseModel
from typing import Dict

class OrderBook(BaseModel):
    exchange: str
    symbol: str
    timestamp: str
    bids: Dict[str, float]
    asks: Dict[str, float]
