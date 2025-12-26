from src.database import engine, Base
from src.models.user import User

# Create all tables
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")

# Test creating a user instance
print("Testing User model...")
try:
    user = User(username="test", email="test@example.com", hashed_password="hashed_password")
    print(f"User model works: {user.username}, {user.email}")
except Exception as e:
    print(f"Error with User model: {e}")

print("Database test completed!")