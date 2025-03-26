from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .storage import AuctionStorage

app = FastAPI()
storage = AuctionStorage()

class AuctionCreate(BaseModel):
    item_name: str
    description: str
    starting_price: float
    duration_minutes: int

class Bid(BaseModel):
    user: str
    amount: float

@app.post("/auctions/")
def create_auction(auction: AuctionCreate):
    try:
        return storage.create_auction(auction)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/auctions/")
def get_active_auctions():
    try:
        return storage.get_active_auctions()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/auctions/{auction_id}")
def get_auction(auction_id: int):
    try:
        return storage.get_auction(auction_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auctions/{auction_id}/bid")
def place_bid(auction_id: int, bid: Bid):
    try:
        return storage.place_bid(auction_id, bid)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auctions/{auction_id}/close")
def close_auction(auction_id: int):
    try:
        return storage.close_auction(auction_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
