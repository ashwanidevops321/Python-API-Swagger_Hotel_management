from fastapi import APIRouter, HTTPException, status, Depends
import sqlite3
from utils import verify_token
from database import get_connection

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK, tags=["FAQ"])
def get_faq(token: str = Depends(verify_token)):
    try:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM faq")
        faq = cursor.fetchall()
        conn.close()
        return {"faq": [dict(faq) for faq in faq]}
    except sqlite3.DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )