import datetime
from src.utils.adapter_db import MongoDBAdapter
import uuid
import config

class RecadosService():    
    def __init__(self):
        self.recados_collection = MongoDBAdapter(config.mongo_URI, config.db_name, config.recados_collection)
        self.users_collection = MongoDBAdapter(config.mongo_URI, config.db_name, config.users_collection)

    def new_recado(self, user_id: str, datos: dict) -> str:
        
        # Check user is active in database
        user = self.users_collection.find_one({"user_id":user_id})
        if not user:
            print(user_id)
            return {"Error": "User not found"}, 400
        # Add user_id to the data
        datos["creator_id"] = user_id
        datos["creator_name"] = user.get("name")
        # Create a UUID and add it to the new recado
        datos["recado_id"] = str(uuid.uuid4())
        datos["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        # Insert the new recado
        self.recados_collection.insert_one(datos)
        return "DONE"

    def get_available_recados(self, user_id, map_radio) -> str:
        # Check user is active in database
        user = self.users_collection.find_one({"user_id":user_id})
        if not user:
            return {"Error": "User not found"}, 400
    
        # Get available recados
        # Approximate distances from meters to latitud/longitud (distance / 111320)
        max_angle = map_radio/111320
        lat = user.get("latitude")
        lng = user.get("longitude")
        min_lat = lat - max_angle
        max_lat = lat + max_angle
        min_lng = lng - max_angle
        max_lng = lng + max_angle
        query = {
            "latitude": {"$gte": min_lat, "$lte": max_lat},
            "longitude": {"$gte": min_lng, "$lte": max_lng},
        }
        return self.recados_collection.find_many(query)   

'''
if __name__ == '__main__':
    print(RecadosService().get_available_recados("8d3a62eb-4962-4f44-b5c7-985c4d56e6ef"))
'''