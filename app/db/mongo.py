from pymongo import MongoClient
from app.core.config import settings

class MongoDB:
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]

mongodb = MongoDB()