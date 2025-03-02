from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Professional, ProfessionalProfession, Profession
from schemas import ProfessionalCreate, ProfessionalResponse

router = APIRouter()

@router.post("/professionals", response_model=ProfessionalResponse)
def create_professional(professional: ProfessionalCreate, db: Session = Depends(get_db)):
    # 📌 Ellenőrizzük, hogy a felhasználó már regisztrált-e szakemberként
    existing_professional = db.query(Professional).filter(Professional.user_id == professional.user_id).first()
    if existing_professional:
        raise HTTPException(status_code=400, detail="Ez a felhasználó már szakemberként regisztrált!")

    # 📌 Új szakember létrehozása
    new_professional = Professional(
        user_id=professional.user_id,
        experience_years=professional.experience_years,
        bio=professional.bio,
        location_id=professional.location_id
    )
    db.add(new_professional)
    db.commit()
    db.refresh(new_professional)

    # 📌 Hozzáadjuk a szakmákat
    for profession_id in professional.professions:
        # 📌 Ellenőrizzük, hogy a szakma létezik-e
        profession = db.query(Profession).filter(Profession.id == profession_id).first()
        if not profession:
            raise HTTPException(status_code=400, detail=f"Szakma nem található: {profession_id}")
        
        # 📌 Szakma és szakember összekapcsolása
        db.add(ProfessionalProfession(professional_id=new_professional.id, profession_id=profession_id))

    db.commit()
    return new_professional
