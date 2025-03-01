from fastapi import FastAPI
from routes import users, professionals, locations, auth  # Importáljuk a hitelesítési útvonalakat is

app = FastAPI()

# Végpontok regisztrálása
app.include_router(users.router)
app.include_router(professionals.router)
app.include_router(locations.router)
app.include_router(auth.router)  # Hozzáadjuk az auth route-ot

@app.get("/")
def home():
    return {"message": "RenoMate API is running!"}