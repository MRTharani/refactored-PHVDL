from pymongo import MongoClient
import logging
from config import *

logging.basicConfig(level=logging.INFO)




def connect_to_mongodb(uri, db_name):
    try:
        client = MongoClient(uri)
        db = client[db_name]
        return db
    except Exception as e:
        print(f"Error: Could not connect to MongoDB.\n{e}")
        return None

def insert_document(document):
    try:
        collection = db[collection_name]
        result = collection.insert_one(document)
        print(f"Inserted document with ID: {result.inserted_id}")
    except Exception as e:
        print(f"Error: Could not insert document.\n{e}")

def find_documents(query=None):
    try:
        collection = db[collection_name]
        if query:
            cursor = collection.find(query)
        else:
            cursor = collection.find()

        return list(cursor)
    except Exception as e:
        print(f"Error: Could not retrieve documents.\n{e}")
        return []


def get_raw_url():
    documents = find_documents()
    return [doc.get("URL") for doc in documents]




db = connect_to_mongodb(MONGODB_URI, "Spidydb")
collection_name = COLLECTION_NAME
if db is not None:
    logging.info("Connected to MongoDB")
