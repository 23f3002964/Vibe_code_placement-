import sqlite3
from config import config

# Connect to the SQLite database
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

try:
    # Add the is_admin column to the users table if it doesn't exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'is_admin' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0")
        print("Added 'is_admin' column to users table")
    else:
        print("'is_admin' column already exists")
    
    # Commit the changes
    conn.commit()
    print("Database schema updated successfully!")
    
except sqlite3.Error as e:
    print(f"An error occurred: {e}")
    
finally:
    # Close the connection
    conn.close()