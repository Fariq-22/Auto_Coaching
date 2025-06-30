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
    Establishes a connection to the MongoDB database using the provided URI and database name from settings.
    If the connection is already established, it returns the existing client and db instance.
    :return: Tuple of (MongoClient, Database)
    :raises ConnectionFailure: If the connection to MongoDB fails.
    :raises Exception: For any other exceptions that may occur during connection.
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

