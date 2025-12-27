import os
from pymongo import MongoClient

client = MongoClient(os.environ["MONGO_URI"])
db = client["facesort"]
users = db["telegram_users"]
