import threading
from datetime import datetime, timedelta, timezone
from typing import Dict, List


class AuctionStorage:

    def __init__(self):
        self.auctions: Dict[int, Dict] = {}
        self.bids: Dict[int, List[Dict]] = {}
        self.auction_id_counter = 1
        self.lock = threading.Lock()
    
    def create_auction(self, auction):
        end_time = datetime.now(timezone.utc) + timedelta(minutes=auction.duration_minutes)
        with self.lock:
            auction_id = self.auction_id_counter
            self.auction_id_counter += 1
            self.auctions[auction_id] = {
                "id": auction_id,
                "item_name": auction.item_name,
                "description": auction.description,
                "starting_price": auction.starting_price,
                "end_time": end_time,
                "active": True,
            }
            self.bids[auction_id] = []
        return {"auction_id": auction_id}

    def get_active_auctions(self):
        return [auction for auction in self.auctions.values() if auction["active"]]
    
    def get_auction(self, auction_id: int):
        if auction_id not in self.auctions:
            raise ValueError("Auction not found")
        return {**self.auctions[auction_id], "bids": self.bids[auction_id]}

    def place_bid(self, auction_id: int, bid):
        if auction_id not in self.auctions:
            raise ValueError("Auction not found")
        with self.lock:
            auction = self.auctions[auction_id]
            if not auction["active"]:
                raise ValueError("Auction has ended")
            if self.bids[auction_id] and bid.amount <= self.bids[auction_id][-1]["amount"]:
                raise ValueError("Bid must be higher than current highest bid")
            self.bids[auction_id].append({"user": bid.user, "amount": bid.amount, "time": datetime.now(timezone.utc)})
        return {"message": "Bid placed successfully"}
    
    def close_auction(self, auction_id: int):
        if auction_id not in self.auctions:
            raise ValueError("Auction not found")
        with self.lock:
            auction = self.auctions[auction_id]
            if not auction["active"]:
                raise ValueError("Auction already closed")
            auction["active"] = False
            winner = max(self.bids[auction_id], key=lambda b: b["amount"], default=None)
        return {"message": "Auction closed", "winner": winner}