import unittest
from src.storage import AuctionStorage
from types import SimpleNamespace

class TestAuctionStorage(unittest.TestCase):
    def setUp(self):
        self.storage = AuctionStorage()

    def test_create_auction(self):
        auction = SimpleNamespace(item_name="Laptop", description="Gaming laptop", starting_price=500, duration_minutes=10)
        result = self.storage.create_auction(auction)
        self.assertIn("auction_id", result)
        self.assertEqual(len(self.storage.auctions), 1)

    def test_get_active_auctions(self):
        auction = SimpleNamespace(item_name="Phone", description="New smartphone", starting_price=300, duration_minutes=5)
        self.storage.create_auction(auction)
        active_auctions = self.storage.get_active_auctions()
        self.assertEqual(len(active_auctions), 1)
        self.assertTrue(active_auctions[0]["active"])

    def test_get_auction(self):
        auction = SimpleNamespace(item_name="Watch", description="Smartwatch", starting_price=200, duration_minutes=5)
        result = self.storage.create_auction(auction)
        auction_id = result["auction_id"]
        auction_data = self.storage.get_auction(auction_id)
        self.assertEqual(auction_data["id"], auction_id)
        self.assertEqual(auction_data["item_name"], "Watch")

    def test_place_bid(self):
        auction = SimpleNamespace(item_name="Tablet", description="Android tablet", starting_price=150, duration_minutes=5)
        result = self.storage.create_auction(auction)
        auction_id = result["auction_id"]
        bid = SimpleNamespace(user="Alice", amount=200)
        response = self.storage.place_bid(auction_id, bid)
        self.assertEqual(response["message"], "Bid placed successfully")
        self.assertEqual(len(self.storage.bids[auction_id]), 1)

    def test_close_auction(self):
        auction = SimpleNamespace(item_name="Camera", description="DSLR camera", starting_price=400, duration_minutes=5)
        result = self.storage.create_auction(auction)
        auction_id = result["auction_id"]
        bid1 = SimpleNamespace(user="Bob", amount=450)
        bid2 = SimpleNamespace(user="Charlie", amount=500)
        self.storage.place_bid(auction_id, bid1)
        self.storage.place_bid(auction_id, bid2)
        close_result = self.storage.close_auction(auction_id)
        self.assertEqual(close_result["message"], "Auction closed")
        self.assertEqual(close_result["winner"]["user"], "Charlie")
        self.assertFalse(self.storage.auctions[auction_id]["active"])

if __name__ == "__main__":
    unittest.main()
