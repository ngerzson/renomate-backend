from fastapi import FastAPI # Importáljuk a FastAPI-t
from routes import users, professionals, locations # Importáljuk a végpontokat

app = FastAPI() # Alkalmazás létrehozása

# Végpontok regisztrálása
app.include_router(users.router)    
app.include_router(professionals.router)
app.include_router(locations.router)

@app.get("/")   # Alapértelmezett végpont
def home():
    return {"message": "RenoMate API is running! Authentication removed."}