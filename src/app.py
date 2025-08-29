"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from motor.motor_asyncio import AsyncIOMotorClient
import os
from pathlib import Path

# MongoDB connection
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client.mergington_high

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")




@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
async def get_activities():
    """Get all activities"""
    activities_list = await db.activities.find().to_list(length=None)
    # Convert to the format expected by the frontend
    return {activity["name"]: {
        "description": activity["description"],
        "schedule": activity["schedule"],
        "max_participants": activity["max_participants"],
        "participants": activity["participants"]
    } for activity in activities_list}


@app.post("/activities/{activity_name}/signup")
async def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    activity = await db.activities.find_one({"name": activity_name})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    
    # Add student using $addToSet to prevent duplicates
    update_result = await db.activities.update_one(
        {"name": activity_name},
        {"$addToSet": {"participants": email}}
    )
    
    if update_result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
        
    return {"message": f"Signed up {email} for {activity_name}"}


@app.post("/activities/{activity_name}/unregister")
async def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    activity = await db.activities.find_one({"name": activity_name})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is not registered for this activity")
    
    # Remove student
    await db.activities.update_one(
        {"name": activity_name},
        {"$pull": {"participants": email}}
    )
    return {"message": f"Removed {email} from {activity_name}"}
