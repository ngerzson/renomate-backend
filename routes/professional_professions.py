from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Professional, Profession, ProfessionalProfession
from schemas import ProfessionalProfessionCreate

router = APIRouter()

@router.post("/professional_professions")
def assign_profession(professional_profession: ProfessionalProfessionCreate, db: Session = Depends(get_db)):
    professional = db.query(Professional).filter(Professional.id == professional_profession.professional_id).first()
    profession = db.query(Profession).filter(Profession.id == professional_profession.profession_id).first()

    if not professional:
        raise HTTPException(status_code=404, detail="Szakember nem található.")
    if not profession:
        raise HTTPException(status_code=404, detail="Szakma nem található.")

    new_assignment = ProfessionalProfession(
        professional_id=professional_profession.professional_id,
        profession_id=professional_profession.profession_id
    )

    db.add(new_assignment)
    db.commit()
    return {"message": "Szakma sikeresen hozzárendelve a szakemberhez."}