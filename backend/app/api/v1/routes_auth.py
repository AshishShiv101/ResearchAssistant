from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.auth import create_access_token, get_password_hash, verify_password, decode_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])

# In-memory users (replace with DB in production)
fake_users_db = {}

class User(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    fake_users_db[user.username] = get_password_hash(user.password)
    return {"msg": "User registered successfully"}

@router.post("/login")
def login(user: User):
    if user.username not in fake_users_db:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(user.password, fake_users_db[user.username]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=60)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def get_current_user(username: str = Depends(decode_access_token)):
    return {"username": username}
