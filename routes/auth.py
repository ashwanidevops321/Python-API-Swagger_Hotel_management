from fastapi import APIRouter, HTTPException, Depends, status
from utils import authenticate_user

router = APIRouter()

@router.post("/login")
def login(username: str, password: str):
    token = authenticate_user(username, password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"token": token}