from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

# .env fájl betöltése
load_dotenv()

# Adatbázis kapcsolat beállítása
DATABASE_URL = os.getenv("DATABASE_URL")

# Adatbázis motor létrehozása
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ez a rész hiányozhat!
Base = declarative_base()  # Ez kell a hibamentes működéshez

# Adatbázis kapcsolat létrehozása minden egyes kéréshez
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

