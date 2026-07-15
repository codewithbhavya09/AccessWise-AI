import numpy as np
import pickle
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import os
from utils.helpers import calculate_distance

class RouteRecommender:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_model()
    
    def load_model(self):
        """Load pre-trained route recommendation model"""
        model_path = "models/route_recommender.pkl"
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.scaler = data['scaler']
        else:
            self.train_model()
    
    def train_model(self):
        """Train route recommendation model"""
        # Sample training data
        X = np.array([
            [5.2, 0.85, 1, 1, 0],      # distance, accessibility_score, wheelchair, stairs_avoid, has_obstacles
            [3.8, 0.92, 1, 1, 0],
            [7.1, 0.65, 1, 1, 1],
            [2.5, 0.95, 0, 0, 0],
            [6.3, 0.78, 0, 1, 0],
            [4.2, 0.88, 1, 0, 0],
        ])
        
        y = np.array([0.8, 0.95, 0.6, 0.98, 0.75, 0.85])
        
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        self.model = GradientBoostingRegressor(n_estimators=100, random_state=42, max_depth=5)
        self.model.fit(X_scaled, y)
        
        # Save model
        os.makedirs("models", exist_ok=True)
        with open("models/route_recommender.pkl", 'wb') as f:
            pickle.dump({'model': self.model, 'scaler': self.scaler}, f)
    
    def recommend_route(self, routes, user_profile):
        """Recommend best route based on user profile"""
        
        scored_routes = []
        
        for route in routes:
            score = self._score_route(route, user_profile)
            scored_routes.append({
                'route': route,
                'score': score
            })
        
        # Sort by score (descending)
        scored_routes.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_routes[0] if scored_routes else None
    
    def _score_route(self, route, user_profile):
        """Score a single route based on user profile"""
        
        distance = route.get('distance', 5)
        accessibility_score = route.get('accessibility_score', 0.7)
        obstacles = route.get('obstacles', [])
        
        # Extract user preferences
        wheelchair_accessible = user_profile.get('wheelchair_accessible', 0)
        avoid_stairs = user_profile.get('avoid_stairs', 1)
        avoid_uneven = user_profile.get('avoid_uneven_terrain', 1)
        prefer_elevators = user_profile.get('prefer_elevators', 0)
        
        # Build feature vector
        has_obstacles = 1 if obstacles else 0
        
        features = [
            distance,
            accessibility_score,
            wheelchair_accessible,
            avoid_stairs,
            has_obstacles
        ]
        
        # Scale features
        features_scaled = self.scaler.transform([features])
        
        # Predict score
        score = self.model.predict(features_scaled)[0]
        
        # Apply user-specific penalties
        if avoid_stairs and 'stairs' in [obs['type'] for obs in obstacles]:
            score *= 0.5
        
        if wheelchair_accessible and not route.get('wheelchair_accessible', False):
            score *= 0.7
        
        # Distance preference - prefer shorter routes
        if distance > 10:
            score *= 0.8
        
        return max(0, min(1, score))
    
    def get_alternative_routes(self, routes, user_profile, top_n=3):
        """Get top N alternative routes"""
        
        scored_routes = []
        
        for route in routes:
            score = self._score_route(route, user_profile)
            scored_routes.append({
                'route': route,
                'score': score
            })
        
        scored_routes.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_routes[:top_n]

# Initialize global recommender
recommender = RouteRecommender()

def recommend_route(routes, user_profile):
    """Public function to recommend route"""
    return recommender.recommend_route(routes, user_profile)

def get_alternative_routes(routes, user_profile, top_n=3):
    """Public function to get alternatives"""
    return recommender.get_alternative_routes(routes, user_profile, top_n)