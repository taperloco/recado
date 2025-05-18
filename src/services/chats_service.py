from src.utils.adapter_db import MongoDBAdapter
import config
import datetime
from bson import ObjectId

class ChatsService():    
    def __init__(self):
        self.users_collection = MongoDBAdapter(config.mongo_URI, config.db_name, config.users_collection)
        self.chats_collection = MongoDBAdapter(config.mongo_URI, config.db_name, config.chats_collection)


    def new_chat_message(self, user_id: str, text: str, send_to: str) -> str:
        # Check if both users are registered
        user = self.users_collection.find_one({"user_id": user_id})
        recipient =  self.users_collection.find_one({"user_id": send_to})
        if not user or not recipient:
            return {"Error": "User not found"}, 400
        
        if user_id in recipient.get("blocked_users"):
            return {"Error": "User is blocked"}, 400

        chat_id = user.get("chats").get(send_to) 
        if chat_id is None:
            # Create new chat
            new_chat = {
                "creator_id": user_id,
                "reciever_id": send_to,
                "messages" : [],
                "next_turn": user_id
            }
            chat_id = self.chats_collection.insert_one(new_chat)
            # Add new chat to both users chat dictionaries
            self.users_collection.update_one(
                {"user_id": user_id},
                {"$set": {f"chats.{send_to}": chat_id}}
            )
            self.users_collection.update_one(
                {"user_id": send_to},
                {"$set": {f"chats.{user_id}": chat_id}}
            )
            
        """
        # Check if next turn corresponds to the sender 
        if user_id != self.chats_collection.find_one_projection(
            {"_id": ObjectId(chat_id)},
            {"next_turn": 1, "_id": 0})["next_turn"]:      
                return {"Error": "It is the turn of the other user of the chat"}, 400
        """
                

        #Add message to the chat and set next turn
        chat =  self.chats_collection.update_one(
            {"_id": ObjectId(chat_id)}, 
            {
                "$push": {
                    "messages": {
                        "Name": user.get("name"),
                        "Text": text,
                        "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                },
                "$set": {
                    "next_turn": send_to
                }
            }
        )
        # Add notifications
        return "Mensaje correctamente enviado"

    def get_chat_messages(self, user_id: str, send_to: str) -> str:
        # Check if user is registered
        user = self.users_collection.find_one({"user_id": user_id})
        if not user:
            return {"Error": "User not found"}, 400
        
        chat_id = user.get("chats").get(send_to)
        if chat_id is None:
            return "Empty"
        else:
            # Return last 20 messages of the chat
            return self.chats_collection.find_one({"_id": ObjectId(chat_id)}).get("messages")[-15:]
        