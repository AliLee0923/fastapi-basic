from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user import UserCreate, Token
from services import auth
from db import get_db

router = APIRouter()

@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    auth.create_user(user, db)
    token = auth.authenticate_user(user.email, user.password, db)
    return {"access_token": token}

@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    token = auth.authenticate_user(user.email, user.password, db)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": token}