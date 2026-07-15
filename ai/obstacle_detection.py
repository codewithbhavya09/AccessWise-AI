import cv2
import numpy as np
from PIL import Image
import pickle
import os

class ObstacleDetector:
    def __init__(self):
        self.obstacle_types = [
            'stairs', 'ramp', 'pothole', 'broken_sidewalk',
            'curb', 'construction', 'water', 'debris'
        ]
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load pre-trained obstacle detection model"""
        model_path = "models/obstacle_detector.pkl"
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
    
    def detect_obstacles(self, image):
        """Detect obstacles in image"""
        # Convert PIL image to cv2 format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Preprocess image
        processed = self._preprocess_image(cv_image)
        
        # Extract features
        features = self._extract_features(processed)
        
        # Detect obstacles
        obstacles = self._detect_with_features(cv_image, features)
        
        return obstacles
    
    def _preprocess_image(self, image):
        """Preprocess image for detection"""
        # Resize image
        resized = cv2.resize(image, (640, 480))
        
        # Convert to grayscale
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        
        # Apply CLAHE for better contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        return enhanced
    
    def _extract_features(self, image):
        """Extract features from image"""
        features = {}
        
        # Edge detection
        edges = cv2.Canny(image, 100, 200)
        features['edges'] = edges
        
        # Contours
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        features['contours'] = contours
        
        # Corners
        corners = cv2.goodFeaturesToTrack(image, 100, 0.01, 10)
        features['corners'] = corners
        
        return features
    
    def _detect_with_features(self, image, features):
        """Detect obstacles using extracted features"""
        obstacles = []
        
        edges = features['edges']
        contours = features['contours']
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Minimum area threshold
                x, y, w, h = cv2.boundingRect(contour)
                
                # Classify obstacle
                obstacle_type, confidence = self._classify_obstacle(image[y:y+h, x:x+w])
                
                obstacles.append({
                    'type': obstacle_type,
                    'confidence': confidence,
                    'x': x,
                    'y': y,
                    'width': w,
                    'height': h,
                    'area': area
                })
        
        return sorted(obstacles, key=lambda x: x['confidence'], reverse=True)
    
    def _classify_obstacle(self, region):
        """Classify obstacle type"""
        # Simple classification based on shape and texture
        
        if len(region) == 0:
            return 'unknown', 0.0
        
        # Calculate shape features
        mean_intensity = np.mean(region)
        std_intensity = np.std(region)
        
        # Simple heuristic classification
        if std_intensity < 20:
            if mean_intensity > 150:
                return 'pothole', 0.75
            else:
                return 'construction', 0.70
        elif std_intensity < 50:
            if mean_intensity > 120:
                return 'water', 0.65
            else:
                return 'debris', 0.60
        else:
            return 'stairs', 0.80
    
    def draw_obstacles(self, image, obstacles):
        """Draw obstacles on image"""
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        for obstacle in obstacles:
            x, y, w, h = obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']
            
            # Draw rectangle
            cv2.rectangle(cv_image, (x, y), (x+w, y+h), (0, 0, 255), 2)
            
            # Put text label
            label = f"{obstacle['type']} ({obstacle['confidence']:.2f})"
            cv2.putText(cv_image, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        return cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

# Initialize global detector
detector = ObstacleDetector()

def detect_obstacles_in_image(image):
    """Public function to detect obstacles"""
    return detector.detect_obstacles(image)

def draw_detected_obstacles(image, obstacles):
    """Public function to draw obstacles"""
    return detector.draw_obstacles(image, obstacles)