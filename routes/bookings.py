from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from utils import authenticate_user, verify_token, token_store
import sqlite3

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return user

def get_connection():
    conn = sqlite3.connect('hotel_management.db')
    conn.row_factory = sqlite3.Row
    return conn

@router.post("/")   
def create_booking(
    room_id: int, 
    customer_name: str, 
    check_in_date: str, 
    check_out_date: str, 
    token: str = Depends(get_current_user)
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT is_available FROM rooms WHERE id = ?", (room_id,))
    room = cursor.fetchone()
    
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    if room["is_available"] == 0:
        raise HTTPException(status_code=400, detail="Room is not available")
    
    cursor.execute("""INSERT INTO bookings(room_id, customer_name, check_in_date, check_out_date)
                      VALUES (?, ?, ?, ?)""", (room_id, customer_name, check_in_date, check_out_date))
    
    # Mark the room as unavailable
    cursor.execute("UPDATE rooms SET is_available = 0 WHERE id = ?", (room_id,))
    
    conn.commit()
    conn.close()
    
    return {"message": "Booking created successfully"}
