from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Appointment, User, Professional
from schemas import AppointmentCreate, AppointmentResponse
from datetime import datetime
from typing import List

router = APIRouter()

# 📌 POST /appointments – Új időpontfoglalás létrehozása
@router.post("/appointments", response_model=AppointmentResponse)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    customer = db.query(User).filter(User.id == appointment.customer_id, User.user_type == "customer").first()
    professional = db.query(Professional).filter(Professional.id == appointment.professional_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Ügyfél nem található.")
    if not professional:
        raise HTTPException(status_code=404, detail="Szakember nem található.")

    new_appointment = Appointment(
        customer_id=appointment.customer_id,
        professional_id=appointment.professional_id,
        appointment_date=datetime.strptime(appointment.appointment_date, "%Y-%m-%d %H:%M:%S"),
        status=appointment.status
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

# 📌 GET /appointments – Összes időpont listázása
@router.get("/appointments", response_model=List[AppointmentResponse])
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()
