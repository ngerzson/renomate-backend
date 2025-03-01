from sqlalchemy import Column, Integer, String, ForeignKey, Date, DECIMAL, Text, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base

# 📌 Felhasználók táblája
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
    bio = Column(Text, nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)

    location = relationship("Location", back_populates="users")
    professional = relationship("Professional", back_populates="user", uselist=False)

# 📌 Helyszínek táblája
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String(5), nullable=False)
    city = Column(String(255), nullable=False)
    address = Column(String(255), nullable=True)
    latitude = Column(DECIMAL(10, 8), nullable=True)
    longitude = Column(DECIMAL(11, 8), nullable=True)

    users = relationship("User", back_populates="location")
    professionals = relationship("Professional", back_populates="location")

# 📌 Szakemberek táblája
class Professional(Base):
    __tablename__ = "professionals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    experience_years = Column(Integer, nullable=True)
    bio = Column(Text, nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)

    user = relationship("User", back_populates="professional")
    location = relationship("Location", back_populates="professionals")
    professions = relationship("ProfessionalProfession", back_populates="professional")

# 📌 Szakmák táblája
class Profession(Base):
    __tablename__ = "professions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)

# 📌 Kapcsolótábla: Szakemberek és szakmák összekapcsolása
class ProfessionalProfession(Base):
    __tablename__ = "professional_professions"

    id = Column(Integer, primary_key=True, index=True)
    professional_id = Column(Integer, ForeignKey("professionals.id"), nullable=False)
    profession_id = Column(Integer, ForeignKey("professions.id"), nullable=False)

    professional = relationship("Professional", back_populates="professions")