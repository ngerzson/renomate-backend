from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Location
from schemas import LocationResponse
from typing import List

router = APIRouter()

# 📌 GET /locations - Minden lokáció listázása
@router.get("/locations", response_model=List[LocationResponse])
def get_all_locations(db: Session = Depends(get_db)):
    locations = db.query(Location).all()
    if not locations:
        raise HTTPException(status_code=404, detail="Nincs elérhető lokáció.")
    return locations
