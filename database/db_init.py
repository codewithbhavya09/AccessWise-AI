import sqlite3
import os
from datetime import datetime

DB_PATH = "database/accesswise.db"

def init_database():
    """Initialize database with all tables"""
    os.makedirs("database", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            profile_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Routes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            start_point TEXT NOT NULL,
            end_point TEXT NOT NULL,
            start_lat REAL,
            start_lng REAL,
            end_lat REAL,
            end_lng REAL,
            distance REAL,
            accessibility_score REAL,
            obstacles_detected INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Obstacles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS obstacles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route_id INTEGER NOT NULL,
            obstacle_type TEXT NOT NULL,
            confidence REAL,
            location_lat REAL,
            location_lng REAL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (route_id) REFERENCES routes(id)
        )
    ''')
    
    # Feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            route_id INTEGER NOT NULL,
            rating INTEGER,
            comments TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (route_id) REFERENCES routes(id)
        )
    ''')
    
    # Facilities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            facility_type TEXT,
            latitude REAL,
            longitude REAL,
            accessibility_score REAL,
            contact TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Accessibility profiles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accessibility_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            wheelchair_accessible BOOLEAN DEFAULT 0,
            avoid_stairs BOOLEAN DEFAULT 1,
            require_ramp BOOLEAN DEFAULT 0,
            require_elevator BOOLEAN DEFAULT 0,
            avoid_curbs BOOLEAN DEFAULT 0,
            smooth_surface BOOLEAN DEFAULT 1,
            prefer_lit_areas BOOLEAN DEFAULT 0,
            regular_rest_areas BOOLEAN DEFAULT 0,
            good_lighting BOOLEAN DEFAULT 0,
            clear_sidewalk BOOLEAN DEFAULT 1,
            guide_rails BOOLEAN DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()
    print("Database initialized successfully!")