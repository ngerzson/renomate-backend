from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserResponse
from typing import List

router = APIRouter()

# 📌 GET /users - Minden felhasználó listázása
@router.get("/users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# 📌 POST /users - Új felhasználó létrehozása
@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Ez az e-mail már használatban van!")

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
