"""
Databashantering för det juridiska AI-systemet.
Hanterar lagring av användarinteraktioner, historik och statistik.
"""

import sqlite3
import json
import os
from datetime import datetime

# Sökväg till databasfilen
DATABASE_PATH = "juridisk_ai.db"

def get_db_connection():
    """
    Skapa en anslutning till databasen
    
    Returns:
        sqlite3.Connection: Databasanslutning
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with necessary tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Skapa tabeller om de inte finns
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        prompt TEXT NOT NULL,
        response TEXT NOT NULL,
        model TEXT NOT NULL,
        language TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        document_name TEXT NOT NULL,
        document_type TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS analytics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        event_data TEXT NOT NULL,
        username TEXT,
        timestamp TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

def save_interaction(username, prompt, response, model, language):
    """Save a user interaction to the database"""
    # Säkerställ att databasen är initierad
    init_db()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    
    cursor.execute(
        "INSERT INTO interactions (username, prompt, response, model, language, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (username, prompt, response, model, language, timestamp)
    )
    
    conn.commit()
    conn.close()

def get_user_history(username):
    """Get the history for a specific user"""
    init_db()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM interactions WHERE username = ? ORDER BY timestamp DESC",
        (username,)
    )
    
    # Konvertera till lista med dictionary
    rows = cursor.fetchall()
    history = []
    for row in rows:
        history.append({
            "id": row["id"],
            "username": row["username"],
            "prompt": row["prompt"],
            "response": row["response"],
            "model": row["model"],
            "language": row["language"],
            "timestamp": row["timestamp"]
        })
    
    conn.close()
    return history

def save_document(username, document_name, document_type, content):
    """Save a generated document to the database"""
    init_db()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    
    cursor.execute(
        "INSERT INTO documents (username, document_name, document_type, content, timestamp) VALUES (?, ?, ?, ?, ?)",
        (username, document_name, document_type, content, timestamp)
    )
    
    conn.commit()
    conn.close()

def get_user_documents(username):
    """Get all documents for a specific user"""
    init_db()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM documents WHERE username = ? ORDER BY timestamp DESC",
        (username,)
    )
    
    # Konvertera till lista med dictionary
    rows = cursor.fetchall()
    documents = []
    for row in rows:
        documents.append({
            "id": row["id"],
            "username": row["username"],
            "document_name": row["document_name"],
            "document_type": row["document_type"],
            "content": row["content"],
            "timestamp": row["timestamp"]
        })
    
    conn.close()
    return documents

def log_analytics_event(event_type, event_data, username=None):
    """Log an analytics event"""
    init_db()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    
    # Konvertera event_data till JSON om det är ett dictionary
    if isinstance(event_data, dict):
        event_data = json.dumps(event_data)
    
    cursor.execute(
        "INSERT INTO analytics (event_type, event_data, username, timestamp) VALUES (?, ?, ?, ?)",
        (event_type, event_data, username, timestamp)
    )
    
    conn.commit()
    conn.close()

def get_database_stats():
    """Get statistics about the database"""
    init_db()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Antal interaktioner
    cursor.execute("SELECT COUNT(*) as count FROM interactions")
    interactions_count = cursor.fetchone()["count"]
    
    # Antal dokument
    cursor.execute("SELECT COUNT(*) as count FROM documents")
    documents_count = cursor.fetchone()["count"]
    
    # Antal användare
    cursor.execute("SELECT COUNT(DISTINCT username) as count FROM interactions")
    users_count = cursor.fetchone()["count"]
    
    # Populära modeller
    cursor.execute("""
    SELECT model, COUNT(*) as count 
    FROM interactions 
    GROUP BY model 
    ORDER BY count DESC
    """)
    models = []
    for row in cursor.fetchall():
        models.append({
            "model": row["model"],
            "count": row["count"]
        })
    
    # Aktivitet över tid (senaste 7 dagarna)
    cursor.execute("""
    SELECT DATE(timestamp) as date, COUNT(*) as count 
    FROM interactions 
    GROUP BY DATE(timestamp) 
    ORDER BY date DESC 
    LIMIT 7
    """)
    activity = []
    for row in cursor.fetchall():
        activity.append({
            "date": row["date"],
            "count": row["count"]
        })
    
    conn.close()
    
    # Returnera statistik
    return {
        "total_interactions": interactions_count,
        "total_documents": documents_count,
        "unique_users": users_count,
        "popular_models": models,
        "recent_activity": activity,
        "database_size_bytes": os.path.getsize(DATABASE_PATH) if os.path.exists(DATABASE_PATH) else 0
    }

def export_history_to_json(username, filename):
    """Export a user's history to a JSON file"""
    history = get_user_history(username)
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)
    
    return filename

def reset_database():
    """Drop all tables and recreate them"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Ta bort befintliga tabeller
    cursor.execute("DROP TABLE IF EXISTS interactions")
    cursor.execute("DROP TABLE IF EXISTS documents")
    cursor.execute("DROP TABLE IF EXISTS analytics")
    
    conn.commit()
    conn.close()
    
    # Återskapa tabellerna
    init_db()
    
    return True

# Initialisera databasen när modulen laddas
init_db()