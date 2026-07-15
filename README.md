# AccessWise-AI
AccessWise AI is an AI-powered accessibility navigation system that helps wheelchair users, visually impaired people, senior citizens, and people with temporary mobility challenges find the safest and most accessible route.

# AccessWise AI

An AI-powered accessibility navigation system helping wheelchair users, visually impaired people, senior citizens, and others find the safest and most accessible routes.

## Features

- **AI-Powered Route Recommendation**: Machine learning algorithms recommend the most accessible routes based on user profiles
- **Obstacle Detection**: Advanced computer vision using OpenCV to detect stairs, ramps, potholes, and other obstacles from images
- **Accessibility Scoring**: Scikit-learn models predict accessibility scores for routes
- **User Profiles**: Customizable accessibility profiles for different mobility challenges
- **Interactive Maps**: Beautiful maps with Folium showing accessible routes and nearby facilities
- **Feedback Learning**: System learns from user feedback to continuously improve recommendations
- **Emergency SOS**: Quick access to emergency services
- **Admin Dashboard**: Monitor system performance and user feedback

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **ML/AI**: Scikit-learn, OpenCV
- **Database**: SQLite
- **Maps**: Folium, OpenStreetMap
- **Data Analysis**: Pandas, NumPy, Plotly

## Installation

1. Clone the repository
```bash
git clone https://github.com/codewithbhavya09/accesswise-ai.git
cd accesswise-ai


2.create virtual environment 

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3.install dependencies 
pip install -r requirements.txt

4.run the application

streamlit run app.py

PROJECT STRUCTURE

accesswise-ai/
├── app.py                 # Main Streamlit application
├── pages/                 # Streamlit pages
│   ├── dashboard.py
│   ├── accessibility_profile.py
│   ├── map_navigator.py
│   ├── image_upload.py
│   ├── nearby_places.py
│   ├── feedback.py
│   └── admin_dashboard.py
├── ai/                    # AI/ML modules
│   ├── obstacle_detection.py
│   ├── accessibility_scorer.py
│   ├── route_recommender.py
│   └── feedback_learner.py
├── database/              # Database operations
│   ├── db_init.py
│   ├── db_queries.py
│   └── db_models.py
├── dataset/               # Sample datasets
│   ├── obstacles_data.csv
│   ├── routes_data.csv
│   └── facilities_data.csv
├── models/                # Trained ML models
│   ├── obstacle_detector.pkl
│   ├── accessibility_scorer.pkl
│   └── route_recommender.pkl
├── assets/                # Images and static files
│   ├── logo.png
│   └── sample_images/
├── utils/                 # Utility functions
│   ├── helpers.py
│   ├── validators.py
│   └── config.py
├── requirements.txt       # Python dependencies
├── README.md
└── .gitignore


Usage
For Users
Sign up with your email and accessibility needs
Set your accessibility profile (wheelchair accessible, avoid stairs, etc.)
Use the map navigator to find routes
Upload images to detect obstacles
Provide feedback to improve recommendations
For Admins
Access admin dashboard to view system statistics
Monitor user feedback and patterns
Manage system models and settings
Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
License
MIT License
Support
For support, email support@accesswise-ai.com
Code
pycache/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.venv/
venv/
ENV/
env/
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
*.db
*.sqlite
*.sqlite3
.env
.env.local
logs/
*.log
.coverage
.pytest_cache/
.streamlit/secrets.toml
*.pkl








### File: utils/config.py
```python
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


