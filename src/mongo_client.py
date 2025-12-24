from pymongo import MongoClient, errors
from utils import get_logger

logger = get_logger("mongodb")

class MongoDBClient:
    def __init__(self):
        try:
            self.client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
            self.client.server_info()
            self.db = self.client["real_estate_db"]
            self.col = self.db["posts"]
            self.col.create_index("post_id", unique=True)
            logger.info("MongoDB connected successfully.")
        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            raise

    def insert_post(self, data: dict) -> bool:
        if not data: return False
        try:
            self.col.insert_one(data)
            return True
        except errors.DuplicateKeyError:
            return False
        except Exception as e:
            logger.error(f"Insert error: {e}")
            return False


    def insert_many_posts(self, data_list: list) -> bool:
        if not data_list: return False
        try:
            self.col.insert_many(data_list, ordered=False)
            return True
        except (errors.BulkWriteError, errors.DuplicateKeyError):
            return True
        except Exception as e:
            logger.error(f"Insert many error: {e}")
            return False

    def close(self):
        if hasattr(self, 'client'):
            self.client.close()
            logger.info("MongoDB connection closed.")