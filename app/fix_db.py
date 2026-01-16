import sqlite3
import os

DB_NAME = "support_tickets.db"

def migrate():
    print(f"Checking {DB_NAME} for missing columns...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Check if columns exist
        cursor.execute("PRAGMA table_info(tickets)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'priority' not in columns:
            print("Adding 'priority' column...")
            cursor.execute("ALTER TABLE tickets ADD COLUMN priority TEXT")
            
        if 'user_id' not in columns:
            print("Adding 'user_id' column...")
            cursor.execute("ALTER TABLE tickets ADD COLUMN user_id TEXT REFERENCES users(username)")
            
        conn.commit()
        print("Migration successful.")
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
