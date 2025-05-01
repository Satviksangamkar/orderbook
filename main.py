from fastapi import FastAPI
from models import OrderBook
from services import get_orderbook_data, run_feed
import asyncio
import platform
import sys

# Windows event loop policy
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI Order Book Feed is running"}

@app.get("/orderbook/{symbol}", response_model=OrderBook)
def get_orderbook(symbol: str):
    data = get_orderbook_data(symbol)
    if not data:
        return {"error": "No data available for symbol"}
    return data

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_feed())
