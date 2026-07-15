import re
from utils.config import ALLOWED_IMAGE_TYPES, MAX_IMAGE_SIZE

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, "Password is valid"

def validate_image(uploaded_file):
    """Validate uploaded image"""
    if uploaded_file is None:
        return False, "No file uploaded"
    
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension not in ALLOWED_IMAGE_TYPES:
        return False, f"Invalid file type. Allowed types: {', '.join(ALLOWED_IMAGE_TYPES)}"
    
    if uploaded_file.size > MAX_IMAGE_SIZE:
        return False, f"File size exceeds {MAX_IMAGE_SIZE / (1024*1024)}MB limit"
    
    return True, "Image is valid"

def validate_coordinates(lat, lng):
    """Validate latitude and longitude"""
    if not (-90 <= lat <= 90):
        return False, "Invalid latitude. Must be between -90 and 90"
    if not (-180 <= lng <= 180):
        return False, "Invalid longitude. Must be between -180 and 180"
    return True, "Coordinates are valid"

def validate_name(name):
    """Validate user name"""
    if len(name) < 2:
        return False, "Name must be at least 2 characters"
    if len(name) > 100:
        return False, "Name must be less than 100 characters"
    return True, "Name is valid"