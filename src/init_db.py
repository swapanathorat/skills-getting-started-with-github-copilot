"""
Initialize MongoDB with the default activities data
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Initial activities data
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu", "lucas@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Practice basketball skills and play friendly games",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["mia@mergington.edu", "noah@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Explore painting, drawing, and sculpture techniques",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["ava@mergington.edu", "liam@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce school plays and performances",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "jack@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Prepare for math competitions and solve challenging problems",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["ethan@mergington.edu", "grace@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["chloe@mergington.edu", "ben@mergington.edu"]
    }
}

async def init_db():
    # Connect to MongoDB
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.mergington_high
    
    # Drop existing activities collection to start fresh
    await db.activities.drop()
    
    # Insert activities
    for name, details in activities.items():
        await db.activities.insert_one({
            "name": name,
            **details
        })
    
    print("Database initialized successfully!")
    
    # List all activities to verify
    async for activity in db.activities.find():
        print(f"Added: {activity['name']}")
    
    await client.close()

if __name__ == "__main__":
    asyncio.run(init_db())
