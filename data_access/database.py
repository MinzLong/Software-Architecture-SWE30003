from pymongo import MongoClient

def get_database():
    client = MongoClient('mongodb://localhost:27017/')
    return client.smart_parking_system

def create_collections():
    db = get_database()
    
    if "users" not in db.list_collection_names():
        db.create_collection("users")
    
    if "bookings" not in db.list_collection_names():
        db.create_collection("bookings")
    
    if "parking_slots" not in db.list_collection_names():
        db.create_collection("parking_slots")
    
    if "parking_spaces" not in db.list_collection_names():
        db.create_collection("parking_spaces")
    
    if "invoices" not in db.list_collection_names():
        db.create_collection("invoices")
