from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserResponse, UserUpdate
from auth import get_password_hash, get_current_user, professional_only, customer_only
from typing import List

router = APIRouter()

# 📌 1️⃣ GET /users/me - Saját adatok lekérdezése (védett végpont)
@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# 📌 2️⃣ PATCH /users/me - Saját adatok frissítése
@router.patch("/users/me", response_model=UserResponse)
def update_user_me(user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user

# 📌 3️⃣ DELETE /users/me - Saját fiók törlése
@router.delete("/users/me")
def delete_user_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.delete(current_user)
    db.commit()
    return {"message": "A fiók sikeresen törölve lett"}

# 📌 4️⃣ GET /users/{id} - Egy adott felhasználó lekérdezése (admin vagy saját fiók esetén engedélyezett)
@router.get("/users/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nem férhetsz hozzá ehhez az adathoz!")
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Felhasználó nem található")
    return user

# 📌 5️⃣ POST /users - Új felhasználó létrehozása hash-elt jelszóval
@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Ez az e-mail cím már használatban van!")

    new_user = User(
        name=user.name,
        email=user.email,
        password=get_password_hash(user.password),  # 🔒 Jelszó titkosítása
        user_type=user.user_type,
        phone=user.phone,
        bio=user.bio,
        location_id=user.location_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 📌 6️⃣ GET /professionals/only - Csak szakembereknek
@router.get("/professionals/only")
def professional_area(current_user: User = Depends(professional_only)):
    return {"message": "Sikeres hozzáférés! Ez a szakemberek területe."}

# 📌 7️⃣ GET /customers/only - Csak ügyfeleknek
@router.get("/customers/only")
def customer_area(current_user: User = Depends(customer_only)):
    return {"message": "Sikeres hozzáférés! Ez az ügyfelek területe."}


