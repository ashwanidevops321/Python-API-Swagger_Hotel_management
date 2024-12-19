from fastapi import APIRouter, HTTPException, Depends, status
import mysql.connector
from mysql.connector import Error
from utils import verify_token
from database import get_connection

router = APIRouter()

def get_current_user(token: str):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return user

def get_mysql_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password@123",
            database="hotel_management_db"
        )
        if conn.is_connected():
            return conn
    except Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database connection error: {e}")

# //Add a new room//
@router.post("/", status_code=status.HTTP_201_CREATED, tags=["Rooms"])
def add_room(room_number: str, type: str, price_per_night: float, is_availability: bool, token: str = Depends(get_current_user)):
    conn = get_mysql_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO rooms (room_number, type, price_per_night, is_availability) 
            VALUES (%s, %s, %s, %s)
        """, (room_number, type, price_per_night, is_availability))
        conn.commit()
    except mysql.connector.IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room number already exists")
    finally:
        cursor.close()
        conn.close()
    
    return {"message": "Room added successfully"}

# //Get all rooms//
@router.get("/", status_code=status.HTTP_200_OK, tags=["Rooms"])
def get_rooms(token: str = Depends(verify_token)):
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"rooms": rooms}

# //Get room by ID//
@router.get("/{room_id}", status_code=status.HTTP_200_OK, tags=["Rooms"])
def get_room(room_id: int, token: str = Depends(verify_token)):
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM rooms WHERE id = %s", (room_id,))
    room = cursor.fetchone()
    cursor.close()
    conn.close()
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return {"room": room}

# //Update room by ID//
@router.put("/{room_id}", status_code=status.HTTP_200_OK, tags=["Rooms"])
def update_room(room_id: int, room_number: str, type: str, price_per_night: float, is_availability: bool, token: str = Depends(verify_token)):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE rooms 
        SET room_number = %s, type = %s, price_per_night = %s, is_availability = %s 
        WHERE id = %s
    """, (room_number, type, price_per_night, is_availability, room_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Room updated successfully"}

# //Delete room by ID//
@router.delete("/{room_id}", status_code=status.HTTP_200_OK, tags=["Rooms"])
def delete_room(room_id: int, token: str = Depends(verify_token)):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rooms WHERE id = %s", (room_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Room deleted successfully"}

# //Patch room by ID (update specific fields)//
@router.patch("/{room_id}", status_code=status.HTTP_200_OK, tags=["Rooms"])
def patch_room(room_id: int, room_number: str, type: str, price_per_night: float, is_availability: bool, token: str = Depends(verify_token)):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE rooms 
        SET room_number = %s, type = %s, price_per_night = %s, is_availability = %s 
        WHERE id = %s
    """, (room_number, type, price_per_night, is_availability, room_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Room updated successfully"}
