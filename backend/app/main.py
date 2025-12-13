from fastapi import FastAPI
from .database import engine
from . import models

app = FastAPI(title="Sweet Shop Management API")

# Create tables on startup
models.Base.metadata.create_all(bind=engine)


@app.get("/")
def health_check():
    return {"status": "Sweet Shop API is running"}
