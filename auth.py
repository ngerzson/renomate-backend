from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import User
import os
from dotenv import load_dotenv

# 🔒 .env fájl betöltése
load_dotenv()

# 🔑 Környezeti változók beállítása
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# 🔒 Jelszó titkosítás beállítása
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 📌 Token kezelése az OAuth2-vel
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# 📌 1️⃣ Jelszó ellenőrzése
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 📌 2️⃣ Jelszó hashelése
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 📌 3️⃣ JWT Token generálás
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "sub": data.get("sub")})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 📌 4️⃣ Felhasználó azonosítása token alapján
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Érvénytelen hitelesítési adatok.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# 📌 5️⃣ Csak szakemberek számára engedélyezett műveletek
def professional_only(current_user: User = Depends(get_current_user)) -> User:
    if current_user.user_type != "professional":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ez a művelet csak szakemberek számára elérhető!"
        )
    return current_user

# 📌 6️⃣ Csak ügyfelek számára engedélyezett műveletek
def customer_only(current_user: User = Depends(get_current_user)) -> User:
    if current_user.user_type != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ez a művelet csak ügyfelek számára elérhető!"
        )
    return current_user