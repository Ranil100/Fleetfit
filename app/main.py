"""
FleetFit backend entrypoint.

Run locally with:
    uvicorn app.main:app --reload

Interactive API docs will be available at http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth, workouts, classes, bookings

# Auto-generate all tables from the ORM models on startup if they don't
# already exist (no manual SQL / migration tool needed to get started).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FleetFit API",
    description=(
        "Backend engine for a high-end gym: member accounts, workout "
        "tracking, and fitness class scheduling/booking."
    ),
    version="1.0.0",
)

# Each domain lives in its own router (APIRouter) to keep the codebase
# modular instead of one giant file of endpoints.
app.include_router(auth.router)
app.include_router(workouts.router)
app.include_router(classes.router)
app.include_router(bookings.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Welcome to the FleetFit API. See /docs for usage."}
