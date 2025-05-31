from .db import mongo
from datetime import datetime

def insert_event(message, timestamp):
    print(f"🔄 Attempting to insert event: {message}")
    try:
        result = mongo.db.events.insert_one({
            "message": message,
            "timestamp": timestamp,
            "created_at": datetime.utcnow()  # Add extra timestamp for debugging
        })
        print(f"✅ Successfully inserted event with ID: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        print(f"❌ Error inserting event: {e}")
        raise e
    
def get_recent_events(limit=10):
    print(f"🔍 Fetching {limit} recent events from database")
    try:
        # Get total count first
        total_count = mongo.db.events.count_documents({})
        print(f"📊 Total events in database: {total_count}")
        
        # Get recent events
        events = list(mongo.db.events.find().sort("timestamp", -1).limit(limit))
        print(f"📋 Retrieved {len(events)} events")
        
        # Debug: print first event if exists
        if events:
            print(f"🔍 First event sample: {events[0]}")
        
        return events
    except Exception as e:
        print(f"❌ Error fetching events: {e}")
        return []

def get_event_stats():
    """Get database statistics for debugging"""
    try:
        total = mongo.db.events.count_documents({})
        recent = mongo.db.events.count_documents({
            "timestamp": {"$gte": datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)}
        })
        return {
            "total_events": total,
            "today_events": recent,
            "collections": mongo.db.list_collection_names()
        }
    except Exception as e:
        return {"error": str(e)}