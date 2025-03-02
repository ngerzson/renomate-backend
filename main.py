from fastapi import FastAPI
from routes import users, professionals, locations  # Eltávolítva az auth import

app = FastAPI()

# Végpontok regisztrálása
app.include_router(users.router)
app.include_router(professionals.router)
app.include_router(locations.router)

@app.get("/")
def home():
    return {"message": "RenoMate API is running! Authentication removed."}