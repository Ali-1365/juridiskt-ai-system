import bcrypt
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URI from environment
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost/postgres")

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a session
db = SessionLocal()

try:
    # Reset all user passwords directly in the database
    print("Resetting user passwords...")
    
    # New password for all users
    new_password = "test123"
    password_bytes = new_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    # Execute update query to set password for all users
    result = db.execute(
        text("UPDATE users SET password_hash = :password_hash"),
        {"password_hash": hashed_password}
    )
    
    db.commit()
    print(f"Done. All users now have password: {new_password}")

except Exception as e:
    print(f"An error occurred: {e}")
    db.rollback()

finally:
    db.close()