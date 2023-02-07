from pymongo import MongoClient

USERNAME = "exceed11"
PASSWORD = "sRS47gYL"
DB_NAME = "exceed11"
MONGO_DB_PORT = 8443
MONGO_DB_URL = f"mongodb://{USERNAME}:{PASSWORD}@mongo.exceed19.online:{MONGO_DB_PORT}"

LOCKER_COLLECTION_NAME = "locker"

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
    client = MongoClient(MONGO_DB_URL)
    db = client[DB_NAME]
    collection = db[LOCKER_COLLECTION_NAME]
    collection.delete_many({})
    collection.insert_many(SEED_DATA)
    print("Seed data inserted successfully.")

if __name__ == "__main__":
    main()