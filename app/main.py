from fastapi import FastAPI
from app.database import engine
from app import models
# 1. Import your brand new members router module
from app.routers import members_router

# Tell SQLAlchemy to physically create tables if they don't exist yet
models.Base.metadata.create_all(bind=engine)

# Initialize the core FastAPI application instance
app = FastAPI(
    title="FleetFit API",
    description="A robust backend engine for gym memberships, workouts, and scheduling.",
    version="1.0.0"
)

# 2. Include the members router into the application engine hierarchy
app.include_router(members_router)

# Temporary testing endpoint (Root Route)
@app.get("/")
def read_root():
    return {"message": "Welcome to FleetFit Gym Management API Engine v1.0"}