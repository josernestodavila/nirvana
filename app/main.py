import asyncio

from fastapi import FastAPI

from app.http_requests import http_get
from app.models import Item
from app.strategies import get_strategy

app = FastAPI()

THIRD_PARTY_API_URLS = [
    'http://127.0.0.1:8000/api_one',
    'http://127.0.0.1:8000/api_two',
    'http://127.0.0.1:8000/api_three',
]


@app.get("/", response_model=Item)
async def index(member_id: int, strategy: str = "avg"):

    results = await asyncio.gather(
        *[http_get(url, {"member_id": member_id}) for url in THIRD_PARTY_API_URLS]
    )
    strategy_function = get_strategy(strategy)
    coalesced_data = strategy_function(results)

    return Item(**coalesced_data)


@app.get("/api_one", response_model=Item)
def api_one(member_id: int):
    return {"deductible": 1000, "stop_loss": 10000, "oop_max": 5000}


@app.get("/api_two", response_model=Item)
def api_two(member_id: int):
    return {"deductible": 1200, "stop_loss": 13000, "oop_max": 6000}


@app.get("/api_three", response_model=Item)
def api_three(member_id: int):
    return {"deductible": 1000, "stop_loss": 10000, "oop_max": 6000}
