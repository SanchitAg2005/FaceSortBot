import os
from pymongo import MongoClient

client = MongoClient(os.environ["mongodb+srv://agarwalsanchit2005:SanchitDB2025_@facesortercluster.upc5259.mongodb.net/?appName=faceSorterCluster"])
db = client["facesort"]
users = db["telegram_users"]

