import requests
import random
from multiprocessing import Pool


API_URL = "http://127.0.0.1:8000"


def create_auction():
    auction_data = {
        "item_name": f"Item_{random.randint(1, 100)}",
        "description": f"Description_{random.randint(1, 100)}",
        "starting_price": random.randint(100, 500),
        "duration_minutes": random.randint(10, 60)
    }
    response = requests.post(f"{API_URL}/auctions/", json=auction_data)
    if response.status_code == 200:
        auction_id = response.json().get("auction_id")
        print(f"Created auction with ID: {auction_id}")
        return auction_id
    else:
        print(f"Err creating auction: {response.text}")
        return None

def get_auction():
    auction_id = random.randint(1, 10)
    response = requests.get(f"{API_URL}/auctions/{auction_id}")
    if response.status_code == 200:
        auction_data = response.json()
        print(f"Auction {auction_id} details: {auction_data}")
    else:
        print(f"Err getting auction {auction_id}: {response.text}")

def place_bid(auction_id):
    user = f"user_{random.randint(1, 100)}"
    amount = random.randint(100, 500)
    bid_data = {"user": user, "amount": amount}
    
    response = requests.post(f"{API_URL}/auctions/{auction_id}/bid", json=bid_data)
    if response.status_code == 200:
        print(f"Bid: {user} with amount: {amount} for auction {auction_id} is OK!")
    else:
        print(f"Err: {user} - {response.text}")

def close_auction(auction_id):
    response = requests.post(f"{API_URL}/auctions/{auction_id}/close")
    if response.status_code == 200:
        print(f"Auction {auction_id} closed successfully.")
    else:
        print(f"Err closing auction {auction_id}: {response.text}")

def random_task(_, num_tasks):
    for _ in range(num_tasks):
        task = random.choice([create_auction, get_auction, place_bid, close_auction])
        
        if task == create_auction:
            task()
        elif task == get_auction:
            task()
        elif task == place_bid:
            auction_id = random.randint(1, 10)
            task(auction_id)
        elif task == close_auction:
            auction_id = random.randint(1, 10)
            task(auction_id)

def run_workers(num_workers, num_tasks):
    with Pool(num_workers) as pool:
        pool.starmap(random_task, [(i, num_tasks) for i in range(num_workers)])

if __name__ == "__main__":
    response = requests.post(f"{API_URL}/auctions/", json={
        "item_name": "Laptop",
        "description": "Laptop gaming",
        "starting_price": 300,
        "duration_minutes": 10
    })
    
    if response.status_code == 200:
        auction_id = response.json()["auction_id"]
        print(f"Auction OK with id: {auction_id}")
        
        run_workers(num_workers=20, num_tasks=100)
    else:
        print(f"Err creating auction: {response.text}")