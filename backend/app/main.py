from fastapi import FastAPI
from .database import engine
from . import models
from .routers import auth

app = FastAPI(title="Sweet Shop Management API")

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)


@app.get("/")
def health_check():
    return {"status": "Sweet Shop API is running"}
