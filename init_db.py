from sqlalchemy.orm import Session
from models import User, UserRole
from auth import get_password_hash
from database import SessionLocal, engine, Base

def init_db():
    """Initialize database and create admin user if not exists"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            # Create admin user
            admin = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                role=UserRole.admin
            )
            db.add(admin)
            db.commit()
            print("✅ Admin user created successfully!")
            print("   Username: admin")
            print("   Password: admin123")
            print("   Email: admin@example.com")
        else:
            print("ℹ️  Admin user already exists")
            
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Done!")
