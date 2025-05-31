from .db import mongo

def insert_event(message, timestamp):
    mongo.db.events.insert_one({
        "message": message,
        "timestamp": timestamp
    })
    
def get_recent_events(limit=10):
    return list(mongo.db.events.find().sort("timestamp", -1).limit(limit))

