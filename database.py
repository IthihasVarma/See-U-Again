import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_db():
    try:
        mongo_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_uri)
        db = client['person_search']
        logging.info("Connected to MongoDB")
        return db
    except PyMongoError as e:
        logging.error(f"Could not connect to MongoDB: {e}")
        return None

def insert_user(data):
    # Validate data here if necessary
    if not validate_user_data(data):
        logging.error("Invalid user data provided.")
        return
    db = connect_db()
    if db is not None:
        try:
            collection = db['users']
            # Validate data here if necessary
            collection.insert_one(data)
            logging.info("User data inserted successfully")
        except PyMongoError as e:
            logging.error(f"An error occurred while inserting user data: {e}")

def validate_user_data(data):
    """Validate user data before insertion."""
    if 'name' not in data or 'email' not in data:
        return False
    # Add more validation rules as needed
    return True
    db = connect_db()
    if db is not None:
        try:
            collection = db['users']
            user = collection.find_one({"_id": user_id})
            return user
        except PyMongoError as e:
            logging.error(f"An error occurred while retrieving user data: {e}")
            return None

if __name__ == "__main__":
    db = connect_db()
    if db:
        logging.info("MongoDB connection established.")
