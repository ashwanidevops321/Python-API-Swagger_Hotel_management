from fastapi import APIRouter, HTTPException, status, Depends
import sqlite3
from utils import verify_token
from database import get_connection

router = APIRouter()
router.get("/", status_code=status.HTTP_200_OK, tags=["Testimonials"])
def get_testimonials(token: str = Depends(verify_token)):
    try:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM testimonials")
        testimonials = cursor.fetchall()
        conn.close()
        return {"testimonials": [dict(testimonial) for testimonial in testimonials]}
    except sqlite3.DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
    )