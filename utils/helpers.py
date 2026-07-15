import os
import numpy as np
from PIL import Image
import streamlit as st
from datetime import datetime
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    return hash_password(password) == hashed_password

def load_image(image_file):
    """Load and return PIL Image"""
    return Image.open(image_file)

def resize_image(image, size=(224, 224)):
    """Resize image to specified dimensions"""
    return image.resize(size)

def image_to_array(image):
    """Convert PIL Image to numpy array"""
    return np.array(image)

def get_coordinates_from_address(address):
    """Mock function - returns sample coordinates"""
    coordinates = {
        'New York': (40.7128, -74.0060),
        'San Francisco': (37.7749, -122.4194),
        'Chicago': (41.8781, -87.6298),
        'Los Angeles': (34.0522, -118.2437),
        'Boston': (42.3601, -71.0589),
    }
    return coordinates.get(address, (40.7128, -74.0060))

def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two coordinates in km"""
    from math import radians, cos, sin, asin, sqrt
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

def get_timestamp():
    """Return current timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_score(score):
    """Format accessibility score as percentage"""
    return f"{score*100:.1f}%"

def set_page_config():
    """Set Streamlit page configuration"""
    st.set_page_config(
        page_title="AccessWise AI",
        page_icon="♿",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def add_custom_css():
    """Add custom CSS styling"""
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .success-message {
            background-color: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .error-message {
            background-color: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .info-message {
            background-color: #d1ecf1;
            color: #0c5460;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .header {
            color: #1f2937;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

def display_success(message):
    st.markdown(f'<div class="success-message">{message}</div>', unsafe_allow_html=True)

def display_error(message):
    st.markdown(f'<div class="error-message">{message}</div>', unsafe_allow_html=True)

def display_info(message):
    st.markdown(f'<div class="info-message">{message}</div>', unsafe_allow_html=True)

def get_obstacle_emoji(obstacle_type):
    """Return emoji for obstacle type"""
    emojis = {
        'stairs': '🪜',
        'ramp': '📐',
        'pothole': '🕳️',
        'broken_sidewalk': '🚫',
        'curb': '⬆️',
        'construction': '🚧',
        'water': '💧',
        'debris': '🗑️'
    }
    return emojis.get(obstacle_type, '⚠️')

def get_facility_emoji(facility_type):
    """Return emoji for facility type"""
    emojis = {
        'Hospital': '🏥',
        'Pharmacy': '💊',
        'Toilet': '🚻',
        'Restaurant': '🍽️',
        'Bank': '🏦',
        'Library': '📚',
        'Police Station': '🚔',
        'Fire Station': '🚒'
    }
    return emojis.get(facility_type, '🏢')
