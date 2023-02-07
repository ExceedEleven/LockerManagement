import os
import urllib

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv('.env')

exceeduser = os.getenv('exceeduser')
password = os.getenv('password')

client = MongoClient(f"mongodb://{exceeduser}:{password}@mongo.exceed19.online:8443/?authMechanism=DEFAULT")
db = client['exceed11']

SEED_DATA = [
    {
        "locker_id": 0,
        "available": True,
        "reservation_id": None
    },
    {
        "locker_id": 1,
        "available": True,
        "reservation_id": None
    },
    {
        "locker_id": 2,
        "available": True,
        "reservation_id": None
    },
    {
        "locker_id": 3,
        "available": True,
        "reservation_id": None
    },
    {
        "locker_id": 4,
        "available": True,
        "reservation_id": None
    },
    {
        "locker_id": 5,
        "available": True,
        "reservation_id": None
    },
]

def main():
    collection = db["locker"]
    collection.delete_many({})
    collection.insert_many(SEED_DATA)
    print("Seed data inserted successfully.")

if __name__ == "__main__":
    main()