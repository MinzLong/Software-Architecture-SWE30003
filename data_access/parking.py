import random
import string
from bson import ObjectId
from data_access.database import get_database

class ParkingSlot:
    @staticmethod
    def generate_short_id():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    @staticmethod
    def create_slots():
        db = get_database()
        parking_spaces = db.parking_spaces.find()
        
        for space in parking_spaces:
            existing_slots = list(db.parking_slots.find({"space_id": space["_id"]}))
            slots_to_create = 5 - len(existing_slots)
            for _ in range(slots_to_create):
                short_id = ParkingSlot.generate_short_id()
                slot = {
                    "short_id": short_id,
                    "space_id": space["_id"],
                    "is_occupied": False
                }
                db.parking_slots.insert_one(slot)

    @staticmethod
    def view_slots(space_id):
        db = get_database()
        return list(db.parking_slots.find({"space_id": ObjectId(space_id)}))

    @staticmethod
    def get_slot_id_by_short_id(short_id):
        db = get_database()
        slot = db.parking_slots.find_one({"short_id": short_id})
        return slot["_id"] if slot else None

class ParkingSpace:
    @staticmethod
    def create_spaces():
        db = get_database()
        existing_spaces = list(db.parking_spaces.find())
        if not existing_spaces:
            spaces = [
                {"short_id": ''.join(random.choices(string.ascii_letters + string.digits, k=6)), "name": "Space 1"},
                {"short_id": ''.join(random.choices(string.ascii_letters + string.digits, k=6)), "name": "Space 2"},
                {"short_id": ''.join(random.choices(string.ascii_letters + string.digits, k=6)), "name": "Space 3"},
                {"short_id": ''.join(random.choices(string.ascii_letters + string.digits, k=6)), "name": "Space 4"},
                {"short_id": ''.join(random.choices(string.ascii_letters + string.digits, k=6)), "name": "Space 5"}
            ]
            db.parking_spaces.insert_many(spaces)

    @staticmethod
    def view_spaces():
        db = get_database()
        return list(db.parking_spaces.find())

    @staticmethod
    def get_space_id_by_short_id(short_id):
        db = get_database()
        space = db.parking_spaces.find_one({"short_id": short_id})
        return space["_id"] if space else None
