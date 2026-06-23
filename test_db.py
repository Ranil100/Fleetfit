from app.database import SessionLocal
from app import models, security

db = SessionLocal()
try:
    # Try to create a test user
    hashed_pass = security.hash_password("testpass123")
    new_user = models.User(
        email="directtest@example.com",
        full_name="Direct Test",
        hashed_password=hashed_pass,
        role="member"
    )
    db.add(new_user)
    db.commit()
    print("User created successfully!")
    print("User ID:", new_user.id)
except Exception as e:
    print("Error:", type(e).__name__, "-", str(e))
    import traceback
    traceback.print_exc()
finally:
    db.close()
