"""
Reset admin password script for the Juridiskt AI System
"""
import json
import bcrypt
import sys
from app.database.db import init_db, get_db, safe_db_operation
from app.database.models import User

def reset_passwords():
    """Reset passwords for all default users"""
    # Reset passwords in users.json file
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
        
        # Update passwords
        test123_hash = bcrypt.hashpw("test123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin_hash = bcrypt.hashpw("admin".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        users["domare01"]["password"] = test123_hash
        users["ombud01"]["password"] = test123_hash
        users["admin01"]["password"] = admin_hash
        
        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)
            
        print("Passwords reset in users.json")
    except Exception as e:
        print(f"Error updating users.json: {str(e)}")
    
    # Reset passwords in database
    try:
        # Initialize database
        init_db()
        
        def update_passwords(db):
            # Update user passwords
            domare = db.query(User).filter_by(username="domare01").first()
            if domare:
                domare.password = bcrypt.hashpw("test123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
            ombud = db.query(User).filter_by(username="ombud01").first()
            if ombud:
                ombud.password = bcrypt.hashpw("test123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
            admin = db.query(User).filter_by(username="admin01").first()
            if admin:
                admin.password = bcrypt.hashpw("admin".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Commit changes
            db.commit()
            return True
        
        # Use safe_db_operation to handle retries
        result = safe_db_operation(update_passwords)
        
        if result:
            print("Passwords reset in database")
        else:
            print("Failed to reset passwords in database")
    except Exception as e:
        print(f"Error updating database: {str(e)}")
        
    print("\nAll passwords have been reset:")
    print("domare01: test123")
    print("ombud01: test123")
    print("admin01: admin")

if __name__ == "__main__":
    reset_passwords()