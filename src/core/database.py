import sqlite3
from datetime import datetime
import os

class DatabaseManager:
    """
    Handles SQLite database operations for logging inspection results.
    """
    def __init__(self, db_name="qualiem_logs.db"):
        # Create database file in the current working directory
        self.db_path = os.path.join(os.getcwd(), db_name)
        self.create_table()

    def connect(self):
        """Establishes a connection to the SQLite database."""
        return sqlite3.connect(self.db_path)

    def create_table(self):
        """Creates the logs table if it does not exist."""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Schema: ID, Timestamp, Filename, Defect Count, Status (PASS/FAIL)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                filename TEXT,
                defect_count INTEGER,
                status TEXT
            )
        """)
        conn.commit()
        conn.close()

    def add_log(self, filename, defect_count):
        """
        Inserts a new inspection record into the database.
        
        Args:
            filename (str): Name of the tested image file.
            defect_count (int): Number of defects found.
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        # Get current date and time
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Determine status
        status = "PASS" if defect_count == 0 else "FAIL"

        # Insert record
        cursor.execute("INSERT INTO logs (timestamp, filename, defect_count, status) VALUES (?, ?, ?, ?)",
                       (date_str, filename, defect_count, status))
        
        conn.commit()
        conn.close()
        print(f"[DB] Record added: {filename} -> {status}")

    def get_all_logs(self):
        """Fetches all records from the database, sorted by newest first."""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM logs ORDER BY id DESC")
        data = cursor.fetchall()
        
        conn.close()
        return data