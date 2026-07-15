import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import os

class AccessibilityScorer:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_model()
    
    def load_model(self):
        """Load pre-trained accessibility scoring model"""
        model_path = "models/accessibility_scorer.pkl"
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.scaler = data['scaler']
        else:
            # Create a new model if doesn't exist
            self.train_model()
    
    def train_model(self):
        """Train accessibility scorer model"""
        # Sample training data
        X = np.array([
            [0.2, 1, 0, 0, 1, 0.8],  # features: stairs_score, ramps_score, potholes_score, curbs_score, smoothness_score, lighting_score
            [0.5, 0.8, 0.3, 0.2, 0.9, 0.7],
            [0.9, 0.2, 0.1, 0.15, 0.85, 0.9],
            [0.1, 0.9, 0.05, 0, 0.95, 0.8],
            [0.3, 0.7, 0.2, 0.1, 0.88, 0.85],
            [0.8, 0.1, 0.4, 0.3, 0.7, 0.6],
        ])
        
        y = np.array([0.85, 0.75, 0.95, 0.92, 0.88, 0.65])
        
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        self.model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
        self.model.fit(X_scaled, y)
        
        # Save model
        os.makedirs("models", exist_ok=True)
        with open("models/accessibility_scorer.pkl", 'wb') as f:
            pickle.dump({'model': self.model, 'scaler': self.scaler}, f)
    
    def calculate_accessibility_score(self, route_data):
        """Calculate accessibility score for a route"""
        
        # Extract features from route data
        features = self._extract_features(route_data)
        
        # Scale features
        features_scaled = self.scaler.transform([features])
        
        # Predict score
        score = self.model.predict(features_scaled)[0]
        
        # Clip score between 0 and 1
        return max(0, min(1, score))
    
    def _extract_features(self, route_data):
        """Extract features from route data"""
        
        stairs_score = route_data.get('stairs_score', 0.5)
        ramps_score = route_data.get('ramps_score', 0.5)
        potholes_score = route_data.get('potholes_score', 0.5)
        curbs_score = route_data.get('curbs_score', 0.5)
        smoothness_score = route_data.get('smoothness_score', 0.5)
        lighting_score = route_data.get('lighting_score', 0.5)
        
        # Build feature vector
        features = [
            1 - stairs_score,  # Lower is better for obstacles
            ramps_score,        # Higher is better for ramps
            1 - potholes_score, # Lower is better for obstacles
            1 - curbs_score,    # Lower is better for obstacles
            smoothness_score,   # Higher is better
            lighting_score      # Higher is better
        ]
        
        return features
    
    def score_from_obstacles(self, obstacles):
        """Calculate score based on detected obstacles"""
        
        if not obstacles:
            return 0.95  # Nearly perfect if no obstacles
        
        # Count obstacles by type
        obstacle_counts = {}
        for obs in obstacles:
            obs_type = obs.get('type', 'unknown')
            obstacle_counts[obs_type] = obstacle_counts.get(obs_type, 0) + 1
        
        # Calculate penalty based on obstacles
        penalty = 0
        
        # Different penalties for different obstacles
        penalties = {
            'stairs': 0.25,
            'curb': 0.20,
            'pothole': 0.15,
            'broken_sidewalk': 0.15,
            'construction': 0.10,
            'water': 0.10,
            'debris': 0.05,
            'ramp': -0.05  # Positive contribution
        }
        
        for obs_type, count in obstacle_counts.items():
            penalty += penalties.get(obs_type, 0.10) * count
        
        score = max(0.1, 1 - penalty)
        return score
    
    def score_from_user_feedback(self, feedback_list):
        """Calculate score from user feedback"""
        
        if not feedback_list:
            return 0.7
        
        ratings = [f.get('rating', 3) for f in feedback_list if f.get('rating')]
        
        if not ratings:
            return 0.7
        
        avg_rating = sum(ratings) / len(ratings)
        # Convert 1-5 rating to 0-1 scale
        score = avg_rating / 5.0
        
        return score

# Initialize global scorer
scorer = AccessibilityScorer()

def calculate_accessibility_score(route_data):
    """Public function to calculate accessibility score"""
    return scorer.calculate_accessibility_score(route_data)

def score_from_obstacles(obstacles):
    """Public function to score based on obstacles"""
    return scorer.score_from_obstacles(obstacles)

def score_from_feedback(feedback_list):
    """Public function to score based on feedback"""
    return scorer.score_from_user_feedback(feedback_list)