import sqlite3
from database.db_models import User, Route, Obstacle, Feedback, Facility
from utils.helpers import get_timestamp

DB_PATH = "database/accesswise.db"

def get_connection():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)

# User Operations
def create_user(email, password, full_name, profile_type='General'):
    """Create new user"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (email, password, full_name, profile_type)
            VALUES (?, ?, ?, ?)
        ''', (email, password, full_name, profile_type))
        conn.commit()
        user_id = cursor.lastrowid
        
        # Create default accessibility profile
        cursor.execute('''
            INSERT INTO accessibility_profiles (user_id)
            VALUES (?)
        ''', (user_id,))
        conn.commit()
        
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_by_email(email):
    """Get user by email"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_user_profile(user_id, full_name, profile_type):
    """Update user profile"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET full_name = ?, profile_type = ?
        WHERE id = ?
    ''', (full_name, profile_type, user_id))
    conn.commit()
    conn.close()

# Route Operations
def create_route(user_id, start_point, end_point, start_lat, start_lng, 
                 end_lat, end_lng, distance, accessibility_score, obstacles_detected):
    """Create new route"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO routes (user_id, start_point, end_point, start_lat, start_lng,
                           end_lat, end_lng, distance, accessibility_score, obstacles_detected)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, start_point, end_point, start_lat, start_lng, end_lat, 
          end_lng, distance, accessibility_score, obstacles_detected))
    conn.commit()
    route_id = cursor.lastrowid
    conn.close()
    return route_id

def get_user_routes(user_id, limit=10):
    """Get user's routes"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM routes WHERE user_id = ?
        ORDER BY created_at DESC LIMIT ?
    ''', (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_route_by_id(route_id):
    """Get route by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM routes WHERE id = ?', (route_id,))
    row = cursor.fetchone()
    conn.close()
    return row

# Obstacle Operations
def add_obstacle(route_id, obstacle_type, confidence, lat, lng, description):
    """Add obstacle to route"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO obstacles (route_id, obstacle_type, confidence, location_lat, location_lng, description)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (route_id, obstacle_type, confidence, lat, lng, description))
    conn.commit()
    conn.close()

def get_route_obstacles(route_id):
    """Get obstacles for a route"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM obstacles WHERE route_id = ?', (route_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Feedback Operations
def add_feedback(user_id, route_id, rating, comments):
    """Add user feedback"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (user_id, route_id, rating, comments)
        VALUES (?, ?, ?, ?)
    ''', (user_id, route_id, rating, comments))
    conn.commit()
    conn.close()

def get_all_feedback(limit=100):
    """Get all feedback"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM feedback
        ORDER BY created_at DESC LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_feedback_for_route(route_id):
    """Get feedback for specific route"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM feedback WHERE route_id = ?', (route_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Facility Operations
def add_facility(name, facility_type, latitude, longitude, accessibility_score, contact):
    """Add facility"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO facilities (name, facility_type, latitude, longitude, accessibility_score, contact)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, facility_type, latitude, longitude, accessibility_score, contact))
    conn.commit()
    conn.close()

def get_nearby_facilities(lat, lng, radius_km=2, limit=10):
    """Get nearby facilities"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT *, 
        SQRT(POW(latitude - ?, 2) + POW(longitude - ?, 2)) as distance
        FROM facilities
        HAVING distance < ?
        ORDER BY distance ASC
        LIMIT ?
    ''', (lat, lng, radius_km, limit))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_facilities():
    """Get all facilities"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM facilities')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Accessibility Profile Operations
def get_accessibility_profile(user_id):
    """Get user's accessibility profile"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accessibility_profiles WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_accessibility_profile(user_id, **kwargs):
    """Update accessibility profile"""
    conn = get_connection()
    cursor = conn.cursor()
    
    set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
    values = list(kwargs.values()) + [user_id]
    
    cursor.execute(f'''
        UPDATE accessibility_profiles
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
    ''', values)
    conn.commit()
    conn.close()

# Statistics
def get_user_statistics(user_id):
    """Get user statistics"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM routes WHERE user_id = ?', (user_id,))
    total_routes = cursor.fetchone()[0]
    
    cursor.execute('SELECT AVG(distance) FROM routes WHERE user_id = ?', (user_id,))
    avg_distance = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT AVG(accessibility_score) FROM routes WHERE user_id = ?', (user_id,))
    avg_score = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT COUNT(*) FROM feedback WHERE user_id = ?', (user_id,))
    total_feedback = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_routes': total_routes,
        'avg_distance': avg_distance,
        'avg_accessibility_score': avg_score,
        'total_feedback': total_feedback
    }

def get_system_statistics():
    """Get system-wide statistics"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM routes')
    total_routes = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM obstacles')
    total_obstacles = cursor.fetchone()[0]
    
    cursor.execute('SELECT AVG(accessibility_score) FROM routes')
    avg_accessibility = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT AVG(rating) FROM feedback WHERE rating IS NOT NULL')
    avg_feedback = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return {
        'total_users': total_users,
        'total_routes': total_routes,
        'total_obstacles': total_obstacles,
        'avg_accessibility_score': avg_accessibility,
        'avg_feedback_rating': avg_feedback
    }