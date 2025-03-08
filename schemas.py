from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum, IntEnum
from datetime import date, datetime


# 📌 1️⃣ Felhasználói típusa
class UserType(str, Enum):
    customer = "customer"
    professional = "professional"

# 📌 2️⃣ Felhasználó létrehozása (API bemenet)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    user_type: UserType
    phone: Optional[str] = None
    location_id: Optional[int] = None
    profile_picture: Optional[str] = None
    birth_date: Optional[str] = None

# 📌 3️⃣ Felhasználói válaszmodell (API válasz)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    user_type: UserType
    phone: Optional[str]
    location_id: Optional[int]
    profile_picture: Optional[str] = None
    birth_date: Optional[str] = None  # 📌 Most stringként adjuk vissza

    @classmethod
    def from_orm(cls, user):
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            user_type=user.user_type,
            phone=user.phone,
            location_id=user.location_id,
            profile_picture=user.profile_picture,
            birth_date=user.birth_date.strftime("%Y-%m-%d") if user.birth_date else None  # 📌 Dátum konvertálása
        )

    class Config:
        from_attributes = True

# 📌 4️⃣ Helyszínek modellje
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

# 📌 5️⃣ Szakemberek modellje
class ProfessionalCreate(BaseModel):
    user_id: int
    experience_years: Optional[int] = None
    bio: Optional[str] = None
    profession_ids: List[int] = []  # 📌 Hozzáadtam, hogy a szakemberekhez szakmákat is lehessen rendelni

# 📌 Szakemberek válaszmodellje
class ProfessionalResponse(BaseModel):
    id: int
    user_id: int
    experience_years: Optional[int] = None
    bio: Optional[str] = None
    created_at: Optional[datetime] = None
    professions: List[str]  # 📌 Professzionokat most string listaként adjuk vissza

    @classmethod
    def from_orm(cls, professional):
        return cls(
            id=professional.id,
            user_id=professional.user_id,
            experience_years=professional.experience_years,
            bio=professional.bio,
            created_at=professional.created_at,
            professions=[p.name for p in professional.professions]  # 📌 Konvertáljuk string listává
        )

    class Config:
        from_attributes = True

# 📌 6️⃣ Szakmák modellje
class ProfessionCreate(BaseModel):
    name: str

class ProfessionResponse(ProfessionCreate):
    id: int

    class Config:
        from_attributes = True

# 📌 7️⃣ Szakember és szakma kapcsolat modellje
class ProfessionalProfessionCreate(BaseModel):
    professional_id: int
    profession_id: int

class ProfessionalProfessionResponse(ProfessionalProfessionCreate):
    class Config:
        from_attributes = True

# 📌 8️⃣ Időpontfoglalások modellje
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

# 📌 9️⃣ Kategóriák modellje
class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(CategoryCreate):
    id: int

    class Config:
        from_attributes = True

# 📌 🔟 Alkategóriák modellje
class SubCategoryCreate(BaseModel):
    name: str
    category_id: int

class SubCategoryResponse(SubCategoryCreate):
    id: int

    class Config:
        from_attributes = True

# 📌 1️⃣1️⃣ Értékelések modellje
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