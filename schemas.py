from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum

# 🔹 Felhasználó típusa
class UserType(str, Enum):
    customer = "customer"
    professional = "professional"

# 📌 1️⃣ Felhasználó létrehozása
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    user_type: UserType
    phone: Optional[str] = None
    location_id: Optional[int] = None

# 📌 2️⃣ Felhasználói válaszmodell
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    user_type: UserType
    phone: Optional[str]

    class Config:
        from_attributes = True

# 📌 3️⃣ Lokáció modellje
class LocationResponse(BaseModel):
    id: int
    country_code: str
    city: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True

# 📌 4️⃣ Szakember létrehozása (most már több szakmával)
class ProfessionalCreate(BaseModel):
    user_id: int
    experience_years: Optional[int] = None
    bio: Optional[str] = None
    location_id: Optional[int] = None
    professions: List[int]  # Szakmák listája (profession_id-k)

# 📌 5️⃣ Szakember válaszmodell
class ProfessionalResponse(BaseModel):
    id: int
    user_id: int
    experience_years: Optional[int]
    bio: Optional[str]
    location_id: Optional[int]
    professions: List[int]  # Szakmák listája

    class Config:
        from_attributes = True
