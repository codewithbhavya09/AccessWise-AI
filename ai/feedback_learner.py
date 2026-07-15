import numpy as np
import pickle
import os
from collections import defaultdict

class FeedbackLearner:
    def __init__(self):
        self.feedback_data = defaultdict(list)
        self.obstacle_improvements = {}
        self.route_ratings = defaultdict(list)
        self.load_feedback()
    
    def load_feedback(self):
        """Load feedback from file"""
        feedback_path = "models/feedback_data.pkl"
        if os.path.exists(feedback_path):
            with open(feedback_path, 'rb') as f:
                data = pickle.load(f)
                self.feedback_data = data.get('feedback_data', defaultdict(list))
                self.obstacle_improvements = data.get('obstacle_improvements', {})
                self.route_ratings = data.get('route_ratings', defaultdict(list))
    
    def save_feedback(self):
        """Save feedback to file"""
        os.makedirs("models", exist_ok=True)
        with open("models/feedback_data.pkl", 'wb') as f:
            pickle.dump({
                'feedback_data': self.feedback_data,
                'obstacle_improvements': self.obstacle_improvements,
                'route_ratings': self.route_ratings
            }, f)
    
    def add_feedback(self, route_id, user_id, rating, comments, obstacles_reported=None):
        """Add user feedback for learning"""
        
        feedback_entry = {
            'route_id': route_id,
            'user_id': user_id,
            'rating': rating,
            'comments': comments,
            'obstacles': obstacles_reported or []
        }
        
        self.feedback_data[route_id].append(feedback_entry)
        self.route_ratings[route_id].append(rating)
        
        # Process obstacles mentioned in feedback
        if obstacles_reported:
            for obs_type in obstacles_reported:
                if obs_type not in self.obstacle_improvements:
                    self.obstacle_improvements[obs_type] = {
                        'count': 0,
                        'positive_feedback': 0,
                        'negative_feedback': 0
                    }
                
                self.obstacle_improvements[obs_type]['count'] += 1
                
                if rating >= 4:
                    self.obstacle_improvements[obs_type]['positive_feedback'] += 1
                elif rating <= 2:
                    self.obstacle_improvements[obs_type]['negative_feedback'] += 1
        
        self.save_feedback()
    
    def get_obstacle_insights(self):
        """Get insights about obstacles from feedback"""
        
        insights = {}
        
        for obs_type, data in self.obstacle_improvements.items():
            total = data['count']
            positive = data['positive_feedback']
            negative = data['negative_feedback']
            
            if total > 0:
                positive_ratio = positive / total
                negative_ratio = negative / total
                
                insights[obs_type] = {
                    'total_reports': total,
                    'positive_feedback_ratio': positive_ratio,
                    'negative_feedback_ratio': negative_ratio,
                    'severity': negative_ratio  # Higher negative ratio = more severe
                }
        
        return insights
    
    def get_route_recommendations_improvement(self):
        """Get improvement suggestions based on feedback"""
        
        improvements = []
        
        for route_id, ratings in self.route_ratings.items():
            if len(ratings) >= 2:
                avg_rating = np.mean(ratings)
                
                if avg_rating < 3:
                    improvements.append({
                        'route_id': route_id,
                        'current_rating': avg_rating,
                        'suggestion': 'Consider alternative routes or improvements to accessibility'
                    })
        
        return improvements
    
    def predict_obstacle_probability(self, obstacle_type):
        """Predict probability of an obstacle being problematic"""
        
        if obstacle_type not in self.obstacle_improvements:
            return 0.5  # Default neutral probability
        
        data = self.obstacle_improvements[obstacle_type]
        total = data['count']
        negative = data['negative_feedback']
        
        if total == 0:
            return 0.5
        
        return negative / total
    
    def get_most_problematic_obstacles(self, top_n=5):
        """Get most problematic obstacles based on feedback"""
        
        sorted_obstacles = sorted(
            self.obstacle_improvements.items(),
            key=lambda x: x[1]['negative_feedback'],
            reverse=True
        )
        
        return sorted_obstacles[:top_n]
    
    def get_improvement_metrics(self):
        """Get overall improvement metrics"""
        
        if not self.route_ratings:
            return {
                'avg_route_rating': 0,
                'improved_routes': 0,
                'problem_routes': 0
            }
        
        all_ratings = []
        for ratings in self.route_ratings.values():
            all_ratings.extend(ratings)
        
        avg_rating = np.mean(all_ratings) if all_ratings else 0
        
        improved = sum(1 for ratings in self.route_ratings.values() if np.mean(ratings) >= 4)
        problem = sum(1 for ratings in self.route_ratings.values() if np.mean(ratings) < 3)
        
        return {
            'avg_route_rating': avg_rating,
            'improved_routes': improved,
            'problem_routes': problem,
            'total_feedback_entries': len(all_ratings)
        }

# Initialize global feedback learner
feedback_learner = FeedbackLearner()

def add_feedback(route_id, user_id, rating, comments, obstacles=None):
    """Public function to add feedback"""
    feedback_learner.add_feedback(route_id, user_id, rating, comments, obstacles)

def get_obstacle_insights():
    """Public function to get obstacle insights"""
    return feedback_learner.get_obstacle_insights()

def get_improvement_metrics():
    """Public function to get improvement metrics"""
    return feedback_learner.get_improvement_metrics()

def get_most_problematic_obstacles(top_n=5):
    """Public function to get problematic obstacles"""
    return feedback_learner.get_most_problematic_obstacles(top_n)