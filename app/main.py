from fastapi import FastAPI
from app.database import engine
from app import models

# 1. Tell SQLAlchemy to look at your models.py file and physically create 
# the database file and tables if they don't exist yet.
models.Base.metadata.create_all(bind=engine)

# 2. Initialize the core FastAPI application instance
app = FastAPI(
    title="FleetFit API",
    description="A robust backend engine for gym memberships, workouts, and scheduling.",
    version="1.0.0"
)

# 3. Create a temporary testing endpoint (Root Route)
@app.get("/")
def read_root():
    return {"message": "Welcome to FleetFit Gym Management API Engine v1.0"}