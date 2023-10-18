import pymongo

MONGO_URI = "mongodb://localhost:27017/moviebackend"

mongo_client = pymongo.MongoClient(MONGO_URI)
mongo_db = mongo_client["moviebackend"]
