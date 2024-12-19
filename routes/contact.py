from fastapi import APIRouter, HTTPException, status, Depends
import sqlite3
from utils import verify_token
from database import get_connection

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK, tags=["Contact"])
def get_contact(token: str = Depends(verify_token)):
    try:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM our_location")
        location = cursor.fetchone()

        if location is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Location data not found"
            )

        return {"location": dict(location)}  # Convert row to dictionary

    except sqlite3.DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()