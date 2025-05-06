"""
Script för att rensa och återskapa databastabeller
"""
import os
from sqlalchemy import create_engine, text

# Hämta PostgreSQL-inloggningsuppgifter från miljövariabler
DATABASE_URL = os.environ.get("DATABASE_URL")

def reset_database():
    """Drop all tables and recreate them"""
    engine = create_engine(DATABASE_URL)
    
    try:
        # Drop tables
        with engine.connect() as conn:
            print("Dropping tables...")
            conn.execute(text("DROP TABLE IF EXISTS document_extractions CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS ai_interaction_logs CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS documents CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
            
            # Commit changes
            conn.commit()
            
        print("All tables dropped. Please restart the application.")
        print("After restarting, the tables will be recreated with default users.")
        
    except Exception as e:
        print(f"Error resetting database: {str(e)}")

if __name__ == "__main__":
    reset_database()