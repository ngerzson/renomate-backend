from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserResponse, UserUpdate
from auth import get_password_hash, get_current_user, professional_only, customer_only
from typing import List

router = APIRouter()

# 📌 GET /users/me - Saját adatok lekérdezése
@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# 📌 PATCH /users/me - Saját adatok frissítése
@router.patch("/users/me", response_model=UserResponse)
def update_user_me(user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user

# 📌 DELETE /users/me - Saját fiók törlése
@router.delete("/users/me")
def delete_user_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.delete(current_user)
    db.commit()
    return {"message": "A fiók sikeresen törölve lett"}

# 📌 GET /users/{id} - Egy adott felhasználó lekérdezése (most admin is kereshet)
@router.get("/users/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Felhasználó nem található")
    return user

# 📌 POST /users - Új felhasználó létrehozása
@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Ez az e-mail cím már használatban van!")

    new_user = User(
        name=user.name,
        email=user.email,
        password=get_password_hash(user.password),  
        user_type=user.user_type,
        phone=user.phone,
        location_id=user.location_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user