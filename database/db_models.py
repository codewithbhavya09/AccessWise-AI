from datetime import datetime

class User:
    def __init__(self, id, email, password, full_name, profile_type, created_at):
        self.id = id
        self.email = email
        self.password = password
        self.full_name = full_name
        self.profile_type = profile_type
        self.created_at = created_at

class Route:
    def __init__(self, id, user_id, start_point, end_point, distance, 
                 accessibility_score, obstacles_detected, created_at):
        self.id = id
        self.user_id = user_id
        self.start_point = start_point
        self.end_point = end_point
        self.distance = distance
        self.accessibility_score = accessibility_score
        self.obstacles_detected = obstacles_detected
        self.created_at = created_at

class Obstacle:
    def __init__(self, id, route_id, obstacle_type, confidence, location_lat, 
                 location_lng, description, created_at):
        self.id = id
        self.route_id = route_id
        self.obstacle_type = obstacle_type
        self.confidence = confidence
        self.location_lat = location_lat
        self.location_lng = location_lng
        self.description = description
        self.created_at = created_at

class Feedback:
    def __init__(self, id, user_id, route_id, rating, comments, created_at):
        self.id = id
        self.user_id = user_id
        self.route_id = route_id
        self.rating = rating
        self.comments = comments
        self.created_at = created_at

class Facility:
    def __init__(self, id, name, facility_type, latitude, longitude, 
                 accessibility_score, contact):
        self.id = id
        self.name = name
        self.facility_type = facility_type
        self.latitude = latitude
        self.longitude = longitude
        self.accessibility_score = accessibility_score
        self.contact = contact