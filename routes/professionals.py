from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Professional, User
from schemas import ProfessionalCreate, ProfessionalResponse
from typing import List

router = APIRouter()

# 📌 1️⃣ GET /professionals - Összes szakember lekérdezése
@router.get("/professionals", response_model=List[ProfessionalResponse])
def get_professionals(db: Session = Depends(get_db)):
    return db.query(Professional).all()

# 📌 2️⃣ GET /professionals/{id} - Egy adott szakember lekérdezése ID alapján
@router.get("/professionals/{id}", response_model=ProfessionalResponse)
def get_professional(id: int, db: Session = Depends(get_db)):
    professional = db.query(Professional).filter(Professional.id == id).first()
    if not professional:
        raise HTTPException(status_code=404, detail="Szakember nem található")
    return professional
