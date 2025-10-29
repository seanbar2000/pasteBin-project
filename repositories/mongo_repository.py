from pymongo import MongoClient
import random
import string
from models.item import Item
#add base class ItemRepository
class MongoRepository:
    def __init__(self, db_client: MongoClient):
        self.db_client = db_client
        self.index_db()

    def add_paste_bin_to_db(self, paste_bin)-> str:
        db = self.db_client["pasteBin_database"]
        collection = db["pasteBin_collection"]
        paste_bin_url = self.generate_url()

        while collection.find_one({paste_bin_url: {"$exists": True}}):
            paste_bin_url = self.generate_url()

        paste_bin.paste_bin_url = paste_bin_url
        collection.insert_one(paste_bin.__dict__)
        return paste_bin_url

    def get_paste_bin(self, url)-> Item|None:
        db = self.db_client["pasteBin_database"]
        collection = db["pasteBin_collection"]
        result = collection.find_one({"paste_bin_url": url})
        result.pop("_id", None)
        if result:
            return Item(**result)
        return None
                            
    def generate_url(self)-> str:
        characters = string.ascii_lowercase + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(5))
        return random_string
    
    #db setup dont implement in repository
    #changes in db are called miggration(initiation of db or chenges in db like new col etc...)
    #It's a proccess outside the app
    #most common - create a file miggration.py and run it seperetly from the app (scheduled run or before it starts)
    def index_db(self):
        db = self.db_client["pasteBin_database"]
        collection = db["pasteBin_collection"]
        collection.create_index([("paste_bin_url")])

    def delete_item(self, paste_bin_url: str):
        db = self.db_client["pasteBin_database"]
        collection = db["pasteBin_collection"]
        collection.delete_one({"paste_bin_url": paste_bin_url})
