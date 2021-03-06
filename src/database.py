# Imports MongoClient for base level access to the local MongoDB
from pymongo import MongoClient


class Database:
    # Class static variables used for database host ip and port information, database name
    # Static variables are referred to by using <class_name>.<variable_name>
    HOST = '127.0.0.1'
    PORT = '27017'
    DB_NAME = 'weather_db'

    def __init__(self):
        self._db_conn = MongoClient(f'mongodb://{Database.HOST}:{Database.PORT}')
        self._db = self._db_conn[Database.DB_NAME]
    
    # This method finds a single document using field information provided in the key parameter
    # It assumes that the key returns a unique document. It returns None if no document is found
    def get_single_data(self, collection, key):
        db_collection = self._db[collection]
        document = db_collection.find_one(key)
        return document
    
    # This method finds multple documents based on the key provided
    def get_multiple_data(self, collection, key):
        db_collection = self._db[collection]
        documents = db_collection.find(key)
        return documents
    
    # This method inserts the data in a new document. It assumes that any uniqueness check is done by the caller
    def insert_single_data(self, collection, data):
        db_collection = self._db[collection]
        document = db_collection.insert_one(data)
        return document.inserted_id
    
    # This method inserts muliple documents. data should be a list of multiple dicts with keys already set as attributes
    def insert_multiple_data(self, collection, data):
        db_collection = self._db[collection]
        result = db_collection.insert_many(data)
        return result.inserted_ids
    
    # This method runs the aggregate pipeline functionality on mongo db and returns the result set
    def aggregate(self, collection, pipeline):
        db_collection = self._db[collection]
        documents = db_collection.aggregate(pipeline)
        return documents
    