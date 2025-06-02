import os
import logging
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings
# Global references to the client & DB
mongo_client = None
mongo_db = None

def get_mongodb_connection():
    """
    Returns an async Motor client and db instance.
    """
    global mongo_client, mongo_db

    if mongo_client and mongo_db is not None:
        return mongo_client, mongo_db

    try:
        mongo_client = AsyncIOMotorClient(settings.MONGODB_URI)
        mongo_db = mongo_client[settings.MONGODB_NAME]
        logging.info("Async MongoDB connection established successfully.")
        return mongo_client, mongo_db
    except Exception as e:
        logging.critical(f"Error establishing MongoDB connection: {e}")
        mongo_client, mongo_db = None, None
        return mongo_client, mongo_db

