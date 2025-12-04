from database import SessionLocal
from models import User, UserRole
from auth import get_password_hash

db = SessionLocal()
admin = User(
    username="admin",
    email="admin@company.com",
    hashed_password=get_password_hash("secure_password"),
    role=UserRole.admin
)
db.add(admin)
db.commit()
print("Admin created successfully!")