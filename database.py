from datetime import datetime, timedelta
from pymongo import MongoClient
import os
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.mongo_uri = os.getenv('MONGODB_URI')
        if not self.mongo_uri:
            raise ValueError("MONGODB_URI not found in environment variables")
        
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client.chibibot
        self.users = self.db.users
        self.raids = self.db.raids
        self.equipment = self.db.equipment
        self.resources = self.db.resources
        
        self._create_indexes()
        logger.info("Database initialized successfully")
    
    def _create_indexes(self):
        self.raids.create_index("expire_at", expireAfterSeconds=0)
        self.equipment.create_index("user_id")
        self.resources.create_index("user_id")
    
    def get_user(self, user_id):
        return self.users.find_one({"_id": user_id})
    
    def create_user(self, user_id, first_name, username):
        user = {
            "_id": user_id,
            "username": username,
            "first_name": first_name,
            "coins": 1000,
            "experience": 0,
            "level": 1,
            "chibis": [],
            "selected_collections": ["star_wars"],
            "chibi_last_claim": None,
            "created_at": datetime.utcnow(),
            "is_admin": False,
            "is_banned": False,
            "ban_until": None,
        }
        self.users.insert_one(user)
        return user
    
    def update_user(self, user_id, data):
        return self.users.update_one({"_id": user_id}, {"$set": data})
    
    def add_coins(self, user_id, amount):
        return self.users.update_one({"_id": user_id}, {"$inc": {"coins": amount}})
    
    def add_chibi(self, user_id, chibi_data):
        return self.users.update_one({"_id": user_id}, {"$push": {"chibis": chibi_data}})
    
    def create_raid(self, user_id, chibi_id, location, difficulty, return_time):
        raid = {
            "_id": f"{user_id}_{chibi_id}_{int(datetime.utcnow().timestamp())}",
            "user_id": user_id,
            "chibi_id": chibi_id,
            "location": location,
            "difficulty": difficulty,
            "started_at": datetime.utcnow(),
            "return_at": return_time,
            "expire_at": return_time + timedelta(seconds=60),
            "loot": None,
            "chibi_injured": False,
        }
        self.raids.insert_one(raid)
        return raid
    
    def get_active_raids(self, user_id):
        return list(self.raids.find({
            "user_id": user_id,
            "return_at": {"$gt": datetime.utcnow()}
        }))
    
    def get_raid(self, raid_id):
        return self.raids.find_one({"_id": raid_id})
    
    def complete_raid(self, raid_id, loot, is_injured):
        return self.raids.update_one(
            {"_id": raid_id},
            {"$set": {"loot": loot, "chibi_injured": is_injured}}
        )
    
    def add_equipment(self, user_id, chibi_id, equipment_data):
        eq = {
            "user_id": user_id,
            "chibi_id": chibi_id,
            "item_name": equipment_data['name'],
            "health_boost": equipment_data.get('health_boost', 0),
            "stamina_boost": equipment_data.get('stamina_boost', 0),
            "damage_boost": equipment_data.get('damage_boost', 0),
            "equipped_at": datetime.utcnow(),
        }
        return self.equipment.insert_one(eq)
    
    def get_chibi_equipment(self, user_id, chibi_id):
        return self.equipment.find_one({"user_id": user_id, "chibi_id": chibi_id})
    
    def add_resource(self, user_id, resource_name, amount):
        result = self.resources.update_one(
            {"user_id": user_id},
            {"$inc": {f"resources.{resource_name}": amount}},
            upsert=True
        )
        return result
    
    def get_resources(self, user_id):
        return self.resources.find_one({"user_id": user_id})
    
    def set_collections(self, user_id, collections):
        return self.users.update_one(
            {"_id": user_id},
            {"$set": {"selected_collections": collections}}
        )
