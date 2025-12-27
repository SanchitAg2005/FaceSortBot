import os
from pymongo import MongoClient

MONGO_URI = os.environ.get("mongodb+srv://agarwalsanchit2005:SanchitDB2025_@facesortercluster.upc5259.mongodb.net/?appName=faceSorterCluster")

if not MONGO_URI:
    raise Exception("❌ MONGO_URI environment variable is missing!")

client = MongoClient(MONGO_URI)
db = client["facesort"]
users = db["telegram_users"]


