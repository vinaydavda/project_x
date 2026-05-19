import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

DB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("MONGODB_NAME")
DB_COLLECTION = os.getenv("MONGODB_COLLECTION")

client = MongoClient(DB_URL)
mongo_db = client[DB_NAME]
products_collection = mongo_db[DB_COLLECTION]