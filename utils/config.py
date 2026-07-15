import os
from dotenv import load_dotenv

load_dotenv()

# App Configuration
APP_NAME = "AccessWise AI"
APP_ICON = "♿"
APP_DESCRIPTION = "AI-powered accessibility navigation system"

# Database Configuration
DB_PATH = "database/accesswise.db"
DB_INIT_SCRIPT = "database/db_init.py"

# Model Paths
OBSTACLE_DETECTOR_MODEL = "models/obstacle_detector.pkl"
ACCESSIBILITY_SCORER_MODEL = "models/accessibility_scorer.pkl"
ROUTE_RECOMMENDER_MODEL = "models/route_recommender.pkl"

# Image Processing
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_TYPES = ['jpg', 'jpeg', 'png', 'gif']

# Map Configuration
DEFAULT_LAT = 40.7128
DEFAULT_LNG = -74.0060
DEFAULT_ZOOM = 13

# Accessibility Profiles
ACCESSIBILITY_PROFILES = {
    'Wheelchair User': {
        'avoid_stairs': True,
        'require_ramp': True,
        'require_elevator': True,
        'avoid_curbs': True,
        'smooth_surface': True
    },
    'Visually Impaired': {
        'prefer_lit_areas': True,
        'avoid_obstacles': True,
        'clear_sidewalk': True,
        'guide_rails': True
    },
    'Senior Citizen': {
        'avoid_stairs': True,
        'prefer_smooth': True,
        'regular_rest_areas': True,
        'good_lighting': True
    },
    'Temporary Mobility': {
        'avoid_stairs': True,
        'shorter_distances': True,
        'avoid_curbs': True
    }
}

# Obstacle Types
OBSTACLE_TYPES = [
    'stairs', 'ramp', 'pothole', 'broken_sidewalk', 
    'curb', 'construction', 'water', 'debris'
]

# Facility Types
FACILITY_TYPES = [
    'Hospital', 'Pharmacy', 'Toilet', 'Restaurant',
    'Bank', 'Library', 'Police Station', 'Fire Station'
]
