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
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()

@router.get("/{faq_id}", status_code=status.HTTP_200_OK, tags=["FAQ"])
def get_faq(faq_id: int, token: str = Depends(verify_token)):
    try:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM faq WHERE id = ?", (faq_id,))
        faq = cursor.fetchone()
        conn.close()
        if faq is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FAQ not found")
        return {"faq": dict(faq)}
    except sqlite3.DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()
# Post API to add a new FAQ
@router.post("/", status_code=status.HTTP_201_CREATED, tags=["FAQ"])
def add_faq(question: str, answer: str, token: str = Depends(verify_token)):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO faq (question, answer) VALUES (?, ?)", (question, answer))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "FAQ added successfully"}
    except sqlite3.DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()

