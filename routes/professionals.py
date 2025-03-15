from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Professional, User
from schemas import ProfessionalResponse
from typing import List

router = APIRouter()

@router.get("/professionals", response_model=List[ProfessionalResponse])
def get_all_professionals(db: Session = Depends(get_db)):
    professionals = db.query(Professional).all()
    return [ProfessionalResponse.from_orm(professional) for professional in professionals]

@router.delete("/professionals/{id}", response_model=dict)
def delete_professional(id: int, db: Session = Depends(get_db)):
    professional = db.query(Professional).filter(Professional.id == id).first()

    if not professional:
        raise HTTPException(status_code=404, detail="Szakember nem található.")

    db.delete(professional)
    db.commit()
    return {"message": f"Szakember ({id}) sikeresen törölve."}