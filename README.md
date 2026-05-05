# FleetFit Backend

A FastAPI backend engine for a gym: member accounts, secure auth, workout
tracking, and fitness class scheduling/booking. Pure backend — no frontend
included.

## Features

- **User Registration & Login** — bcrypt password hashing, JWT access tokens (30-min expiry)
- **Workout Logging** — record exercise/sets/reps/weight, fetch personal history
- **Fitness Classes** — trainers/admins create classes; anyone can browse them
- **Booking** — members reserve a class slot; overbooking and duplicate bookings are blocked
- **SQLAlchemy ORM** — models with foreign keys / one-to-many relationships
- **Pydantic validation** — strict input/output schemas, passwords never serialized out
- **Modular routers** — `auth`, `workouts`, `classes`, `bookings`

## Project Structure

```
fleetfit/
├── app/
│   ├── main.py          # FastAPI app, includes all routers, creates DB tables
│   ├── config.py        # Settings loaded from .env
│   ├── database.py      # SQLAlchemy engine/session
│   ├── models.py        # ORM models: User, WorkoutLog, FitnessClass, Booking
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── security.py      # Password hashing + JWT create/decode
│   ├── deps.py           # get_current_user / require_staff dependencies
│   └── routers/
│       ├── auth.py       # /auth/register, /auth/login, /auth/me
│       ├── workouts.py   # /workouts
│       ├── classes.py    # /classes
│       └── bookings.py   # /bookings
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env if you want to point at PostgreSQL instead of the default SQLite,
# and change SECRET_KEY to a real random value.

# 4. Run the server
uvicorn app.main:app --reload
```

Visit **http://127.0.0.1:8000/docs** for interactive Swagger docs — you can
register, log in, click "Authorize" with the returned token, and try every
endpoint from the browser.

## Switching to PostgreSQL

Install PostgreSQL locally (or use a hosted instance), create a database,
then set in `.env`:

```
DATABASE_URL=postgresql://username:password@localhost:5432/fleetfit
```

No code changes needed — SQLAlchemy handles both databases through the same
models.

## Example Usage Flow

1. `POST /auth/register` — create an account (role: `member`, `trainer`, or `admin`)
2. `POST /auth/login` — get a JWT `access_token`
3. Use the token as a `Bearer` header on subsequent requests
4. `POST /workouts` — log a workout; `GET /workouts` — view your history
5. A trainer/admin: `POST /classes` — schedule a class
6. Any member: `GET /classes` — browse classes (shows spots remaining)
7. `POST /bookings` — reserve a spot (blocked if full or already booked)
8. `GET /bookings/me` — see your upcoming bookings

## Notes

- Tables are created automatically on first run (`Base.metadata.create_all`).
  For production schema changes, consider adding Alembic migrations.
- The default `SECRET_KEY` in `.env.example` **must** be changed before any
  real deployment.
