from fastapi import APIRouter, HTTPException, Depends, status
from sqlite3 import Connection
from database import get_connection
from utils import verify_token
from pydantic import BaseModel
import mysql.connector

router = APIRouter()

# Dependency to get the database connection
def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()

# Pydantic models for input validation
class Location(BaseModel):
    hotel_name: str
    address: str
    city: str
    state: str
    zip_code: str
    latitude: float
    longitude: float

class UpdateLocation(Location):
    location_id: int

# GET endpoint to fetch hotel locations
@router.get("/", status_code=status.HTTP_200_OK, tags=["Location"])
def get_location(
    city: str = None,
    state: str = None,
    token: str = Depends(verify_token),
    db: Connection = Depends(get_db)
):
    """
    Fetches hotel locations from the database with optional filters like city and state.
    """
    try:
        cursor = db.cursor()
        query = "SELECT id, hotel_name, address, city, state, zip_code, latitude, longitude FROM location"
        filters = []

        if city:
            filters.append("city = ?")
        if state:
            filters.append("state = ?")

        if filters:
            query += " WHERE " + " AND ".join(filters)

        params = [param for param in [city, state] if param is not None]
        cursor.execute(query, params)
        locations = cursor.fetchall()

        if not locations:
            raise HTTPException(status_code=404, detail="No hotel locations found.")

        keys = ["id", "hotel_name", "address", "city", "state", "zip_code", "latitude", "longitude"]
        return {"locations": [dict(zip(keys, location)) for location in locations]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching locations: {str(e)}")

# POST endpoint to add a new hotel location
@router.post("/", status_code=status.HTTP_201_CREATED, tags=["Location"])
def add_location(
    location: Location,
    token: str = Depends(verify_token),
    db: Connection = Depends(get_db)
):
    """
    Adds a new hotel location to the database.
    """
    try:
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO location (hotel_name, address, city, state, zip_code, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (location.hotel_name, location.address, location.city, location.state,
             location.zip_code, location.latitude, location.longitude)
        )
        db.commit()
        return {"detail": "Location added successfully."}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Location already exists.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding location: {str(e)}")

# PUT endpoint to update a hotel location
@router.put("/", status_code=status.HTTP_200_OK, tags=["Location"])
def update_location(
    location: UpdateLocation,
    token: str = Depends(verify_token),
    db: Connection = Depends(get_db)
):
    """
    Updates an existing hotel location in the database.
    """
    try:
        cursor = db.cursor()
        cursor.execute(
            """
            UPDATE location
            SET hotel_name = ?, address = ?, city = ?, state = ?, zip_code = ?, latitude = ?, longitude = ?
            WHERE id = ?
            """,
            (location.hotel_name, location.address, location.city, location.state,
             location.zip_code, location.latitude, location.longitude, location.location_id)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Location not found.")
        db.commit()
        return {"detail": "Location updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating location: {str(e)}")

# DELETE endpoint to delete a hotel location
@router.delete("/", status_code=status.HTTP_200_OK, tags=["Location"])
def delete_location(
    location_id: int,
    token: str = Depends(verify_token),
    db: Connection = Depends(get_db)
):
    """
    Deletes a hotel location from the database.
    """
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM location WHERE id = ?", (location_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Location not found.")
        db.commit()
        return {"detail": "Location deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting location: {str(e)}"
                            )
        
# Patch endpoint to update a hotel location
@router.patch("/", status_code=status.HTTP_200_OK, tags=["Location"])
def patch_location(
    location_id: int,
    location: UpdateLocation,
    token: str = Depends(verify_token),
    db: Connection = Depends(get_db)
):
    """
    Updates an existing hotel location in the database.
    """
    try:
        cursor = db.cursor()
        cursor.execute(
            """
            UPDATE location
            SET hotel_name = ?, address = ?, city = ?, state = ?, zip_code = ?, latitude = ?, longitude = ?
            WHERE id = ?
            """,
            (location.hotel_name, location.address, location.city, location.state,
             location.zip_code, location.latitude, location.longitude, location_id)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Location not found.")
        db.commit()
        return {"detail": "Location updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating location: {str(e)}"
)
