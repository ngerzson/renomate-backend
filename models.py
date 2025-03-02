from sqlalchemy import Column, Integer, String, ForeignKey, Date, DECIMAL, Text, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base

# 📌 1️⃣ Felhasználók táblája
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    user_type = Column(Enum("customer", "professional", name="user_type"), nullable=False)
    profile_picture = Column(String(500), nullable=True)
    birth_date = Column(Date, nullable=True)
    phone = Column(String(20), nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)

    location = relationship("Location", back_populates="users")
    reviews = relationship("Review", back_populates="customer")

# 📌 2️⃣ Helyszínek táblája
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    longitude = Column(DECIMAL(10, 8), nullable=True)
    latitude = Column(DECIMAL(10, 8), nullable=True)

    users = relationship("User", back_populates="location")

# 📌 3️⃣ Szakemberek táblája
class Professional(Base):
    __tablename__ = "professionals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    experience_years = Column(Integer, nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)

    user = relationship("User", back_populates="professional")
    professions = relationship("ProfessionalProfession", back_populates="professional")

# 📌 4️⃣ Szakmák táblája
class Profession(Base):
    __tablename__ = "professions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)

# 📌 5️⃣ Kapcsolótábla: Szakemberek és szakmák összekapcsolása
class ProfessionalProfession(Base):
    __tablename__ = "professional_professions"

    professional_id = Column(Integer, ForeignKey("professionals.id"), primary_key=True)
    profession_id = Column(Integer, ForeignKey("professions.id"), primary_key=True)

    professional = relationship("Professional", back_populates="professions")
    profession = relationship("Profession")

# 📌 6️⃣ Időpontfoglalások táblája (Appointments)
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    professional_id = Column(Integer, ForeignKey("professionals.id"), nullable=False)
    appointment_date = Column(TIMESTAMP, nullable=False)
    status = Column(Enum("pending", "confirmed", "completed", "cancelled", name="appointment_status"), default="pending", nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)

    customer = relationship("User", foreign_keys=[customer_id])
    professional = relationship("Professional", foreign_keys=[professional_id])

# 📌 7️⃣ Kategóriák táblája
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)

    subcategories = relationship("SubCategory", back_populates="category")

# 📌 8️⃣ Alkategóriák táblája
class SubCategory(Base):
    __tablename__ = "subcategories"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(255), nullable=False, unique=True)

    category = relationship("Category", back_populates="subcategories")

# 📌 9️⃣ Értékelések táblája (Reviews)
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    professional_id = Column(Integer, ForeignKey("professionals.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)

    customer = relationship("User", foreign_keys=[customer_id], back_populates="reviews")
    professional = relationship("Professional", foreign_keys=[professional_id])