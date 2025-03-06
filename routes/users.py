from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserResponse
from passlib.context import CryptContext
from datetime import datetime
from typing import List

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 📌 Jelszó titkosítása
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 📌 GET /users - Minden felhasználó listázása (limit és offset nélkül)
@router.get("/users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# 📌 POST /users - Új felhasználó létrehozása
@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Ez az e-mail már használatban van!")

    birth_date = None
    if user.birth_date:
        try:
            birth_date = datetime.strptime(user.birth_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="A születési dátum formátuma helytelen. Használj YYYY-MM-DD formátumot!")

    hashed_password = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        user_type=user.user_type,
        phone=user.phone,
        location_id=user.location_id,
        profile_picture=user.profile_picture,
        birth_date=birth_date
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserResponse.from_orm(new_user)

# 📌 DELETE /users/{user_id} - Felhasználó törlése
@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Felhasználó nem található.")

    db.delete(user)
    db.commit()
    return {"message": f"Felhasználó ({user_id}) sikeresen törölve."}