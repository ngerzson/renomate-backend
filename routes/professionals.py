from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Professional, User
from schemas import ProfessionalCreate, ProfessionalResponse
from typing import List

router = APIRouter()

@router.get("/professionals", response_model=List[ProfessionalResponse])
def get_all_professionals(db: Session = Depends(get_db)):
    professionals = db.query(Professional).all()
    return [ProfessionalResponse.from_orm(prof) for prof in professionals]  # 📌 Professzionok string listává alakulnak

# 📌 POST /professionals - Új szakember regisztrálása
@router.post("/professionals", response_model=ProfessionalResponse)
def create_professional(professional: ProfessionalCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == professional.user_id, User.user_type == "professional").first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Felhasználó nem található vagy nem szakember.")

    new_professional = Professional(
        user_id=professional.user_id,
        experience_years=professional.experience_years,
        bio=professional.bio
    )

    db.add(new_professional)
    db.commit()
    db.refresh(new_professional)
    return new_professional

# 📌 DELETE /professionals/{id} - Szakember törlése
@router.delete("/professionals/{id}", response_model=dict)
def delete_professional(id: int, db: Session = Depends(get_db)):
    professional = db.query(Professional).filter(Professional.id == id).first()
    
    if not professional:
        raise HTTPException(status_code=404, detail="Szakember nem található.")

    db.delete(professional)
    db.commit()
    return {"message": f"Szakember ({id}) sikeresen törölve."}

# 📌 GET /professionals/search - Szakemberek keresése helyszín és szakma alapján
@router.get("/professionals/search", response_model=List[ProfessionalResponse])
def search_professionals(location: str, profession: str, db: Session = Depends(get_db)):
    results = (
        db.query(Professional)
        .join(User)
        .join(Professional.professions)
        .filter(User.location.has(city=location))
        .filter(Professional.professions.any(name=profession))
        .all()
    )

    if not results:
        raise HTTPException(status_code=404, detail="Nincs találat.")

    return results