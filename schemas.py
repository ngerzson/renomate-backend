from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

# 📌 Felhasználói típusa
class UserType(str, Enum):
    customer = "customer"
    professional = "professional"

# 📌 1️⃣ Felhasználó létrehozása (API bemenet)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    user_type: UserType
    phone: Optional[str] = None
    location_id: Optional[int] = None
    profile_picture: Optional[str] = None  # 📌 Hozzáadva
    birth_date: Optional[str] = None  # 📌 Hozzáadva (ISO formátumban)

# 📌 2️⃣ Felhasználói válaszmodell (API válasz)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    user_type: UserType
    phone: Optional[str]
    location_id: Optional[int]
    profile_picture: Optional[str] = None  # 📌 Hozzáadva
    birth_date: Optional[str] = None  # 📌 Hozzáadva

    class Config:
        from_attributes = True
        
# 📌 3️⃣ Helyszínek modellje
class LocationCreate(BaseModel):
    country: str
    city: str
    postal_code: Optional[str] = None
    address: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None

class LocationResponse(LocationCreate):
    id: int

    class Config:
        from_attributes = True

# 📌 4️⃣ Szakemberek modellje
class ProfessionalCreate(BaseModel):
    user_id: int
    experience_years: Optional[int] = None
    bio: Optional[str] = None

class ProfessionalResponse(ProfessionalCreate):
    id: int

    class Config:
        from_attributes = True

# 📌 5️⃣ Szakmák modellje
class ProfessionCreate(BaseModel):
    name: str

class ProfessionResponse(ProfessionCreate):
    id: int

    class Config:
        from_attributes = True

# 📌 6️⃣ Időpontfoglalások modellje
class AppointmentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"

class AppointmentCreate(BaseModel):
    customer_id: int
    professional_id: int
    appointment_date: str
    status: Optional[AppointmentStatus] = AppointmentStatus.pending

class AppointmentResponse(AppointmentCreate):
    id: int
    created_at: Optional[str]

    class Config:
        from_attributes = True

# 📌 7️⃣ Kategóriák modellje
class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(CategoryCreate):
    id: int

    class Config:
        from_attributes = True

# 📌 8️⃣ Alkategóriák modellje
class SubCategoryCreate(BaseModel):
    name: str
    category_id: int

class SubCategoryResponse(SubCategoryCreate):
    id: int

    class Config:
        from_attributes = True

# 📌 9️⃣ Értékelések modellje
class ReviewCreate(BaseModel):
    customer_id: int
    professional_id: int
    rating: int
    comment: Optional[str] = None

class ReviewResponse(ReviewCreate):
    id: int
    created_at: Optional[str]

    class Config:
        from_attributes = True