from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

# 🔹 Felhasználó típusa (customer vagy professional)
class UserType(str, Enum):
    customer = "customer"
    professional = "professional"

# 📌 1️⃣ Felhasználó létrehozásához szükséges adatok
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    user_type: UserType
    phone: Optional[str] = None
    bio: Optional[str] = None
    location_id: Optional[int] = None

# 📌 2️⃣ Felhasználó válaszmodell
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    user_type: UserType
    phone: Optional[str]
    bio: Optional[str]

    class Config:
        from_attributes = True

# 📌 3️⃣ Szakember létrehozásához szükséges adatok
class ProfessionalCreate(BaseModel):
    user_id: int
    profession: str
    experience_years: Optional[int] = None
    phone: Optional[str] = None
    location_id: Optional[int] = None
    bio: Optional[str] = None

# 📌 4️⃣ Szakember válaszmodell
class ProfessionalResponse(BaseModel):
    id: int
    user_id: int
    profession: str
    experience_years: Optional[int]
    phone: Optional[str]
    bio: Optional[str]

    class Config:
        from_attributes = True

# 📌 5️⃣ Lokáció válaszmodell (Locations)
class LocationResponse(BaseModel):
    id: int
    country_code: str
    city: str

    class Config:
        from_attributes = True

# 📌 6️⃣ Bejelentkezési adatok sémája
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# 📌 7️⃣ Bejelentkezési adatok bemenete
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 📌 8️⃣ Felhasználó frissítéséhez szükséges adatok
class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None