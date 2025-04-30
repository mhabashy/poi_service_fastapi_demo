from fastapi import FastAPI, Depends
from .database import engine, Base, get_db
from .routers import poi, moderation
from sqlalchemy.orm import Session
from .models import APIKey
from .auth import generate_api_key
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="POI Service API",
    description="A REST API for submitting and moderating Points of Interest",
    version="0.1.0"
)

app.include_router(poi.router)
app.include_router(moderation.router)

@app.on_event("startup")
async def startup_event():
    """Create default API key if none exists"""
    db = next(get_db())
    if db.query(APIKey).count() == 0:
        default_key = APIKey(
            key=generate_api_key(),
            name="Default API Key",
            is_active=True
        )
        db.add(default_key)
        db.commit()
        print(f"Created default API key: {default_key.key}")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the POI Service API - Michael Habashy"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)