from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from typing import Optional, List, Dict, Any

class MongoDBAdapter:
    def __init__(self, mongo_URI, db_name, collection_name):
        self.uri = mongo_URI
        self.db_name = db_name
        self.collection_name = collection_name
        self._connect()

    def _connect(self):
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            self.client.server_info()  # Trigger exception if cannot connect
            db = self.client[self.db_name]
            self.collection = db[self.collection_name]
        except ConnectionFailure as e:
            raise

    def insert_one(self, data: Dict[str, Any]) -> str:
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.collection.find_one(query)
    
    def find_one_projection(self, query: Dict[str, Any], projection: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.collection.find_one(query, projection)
    

    def find_many(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        if(self.collection_name == "Users_collection"):
            # Eliminate fields that are not needed in the client
            return list(self.collection
                        .find(query, {"_id": 0, "email":0, "password":0, "blocked_users":0, "chats":0, "last_connection":0})
                        .limit(20))
        else:
            # Eliminate mongoID
            return list(self.collection
                        .find(query, {"_id": 0, "active":0})
                        .limit(20))

    def update_one(self, query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        result = self.collection.update_one(query, update_data)
        return result.modified_count

    def delete_one(self, query: Dict[str, Any]) -> int:
        result = self.collection.delete_one(query)
        return result.deleted_count
    