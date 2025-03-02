from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Professional, ProfessionalProfession, Profession
from schemas import ProfessionalCreate, ProfessionalResponse
from typing import List

router = APIRouter()

# 📌 GET /professionals - Minden szakember listázása
@router.get("/professionals", response_model=List[ProfessionalResponse])
def get_all_professionals(db: Session = Depends(get_db)):
    return db.query(Professional).all()

# 📌 POST /professionals - Új szakember hozzáadása
@router.post("/professionals", response_model=ProfessionalResponse)
def create_professional(professional: ProfessionalCreate, db: Session = Depends(get_db)):
    # 📌 Ellenőrizzük, hogy a felhasználó már szakember-e
    if db.query(Professional).filter(Professional.user_id == professional.user_id).first():
        raise HTTPException(status_code=400, detail="Ez a felhasználó már szakember!")

    new_professional = Professional(**professional.dict(exclude={"professions"}))
    db.add(new_professional)
    db.commit()
    db.refresh(new_professional)

    # 📌 Hozzáadjuk a szakmákat
    for profession_id in professional.professions:
        profession = db.query(Profession).filter(Profession.id == profession_id).first()
        if not profession:
            raise HTTPException(status_code=400, detail=f"Szakma nem található: {profession_id}")
        
        db.add(ProfessionalProfession(professional_id=new_professional.id, profession_id=profession_id))

    db.commit()
    return new_professional
