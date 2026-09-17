"""
Mood Tracker
Tracks mood history and analyzes patterns using ML
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


class MoodTracker:
    """Track and analyze mood patterns"""
    
    def __init__(self, filepath='data/mood_history.csv'):
        self.filepath = filepath
        os.makedirs('data', exist_ok=True)
        self.load_history()
    
    def load_history(self):
        """Load mood history from CSV"""
        if os.path.exists(self.filepath):
            self.history = pd.read_csv(self.filepath)
            self.history['timestamp'] = pd.to_datetime(self.history['timestamp'])
        else:
            self.history = pd.DataFrame(columns=[
                'timestamp', 'emotion', 'score', 'text', 'source'
            ])
    
    def save_history(self):
        """Save mood history to CSV"""
        self.history.to_csv(self.filepath, index=False)
    
    def log_mood(self, emotion, score, text='', source='text'):
        """Log a mood entry"""
        new_entry = pd.DataFrame([{
            'timestamp': datetime.now(),
            'emotion': emotion,
            'score': score,
            'text': text[:200],  # Limit text length
            'source': source
        }])
        self.history = pd.concat([self.history, new_entry], ignore_index=True)
        self.save_history()
    
    def get_recent(self, days=7):
        """Get recent mood entries"""
        if self.history.empty:
            return self.history
        cutoff = datetime.now() - timedelta(days=days)
        return self.history[self.history['timestamp'] >= cutoff]
    
    def get_statistics(self):
        """Get mood statistics"""
        if self.history.empty:
            return {
                'total_entries': 0,
                'avg_mood': 0,
                'most_common': 'N/A',
                'trend': 'No data'
            }
        
        return {
            'total_entries': len(self.history),
            'avg_mood': round(self.history['score'].mean(), 2),
            'most_common': self.history['emotion'].mode().iloc[0] if not self.history.empty else 'N/A',
            'trend': self._calculate_trend()
        }
    
    def _calculate_trend(self):
        """Calculate mood trend"""
        if len(self.history) < 2:
            return 'Not enough data'
        
        recent = self.history.tail(5)['score'].mean()
        older = self.history.head(5)['score'].mean() if len(self.history) >= 10 else self.history['score'].mean()
        
        diff = recent - older
        
        if diff > 0.2:
            return '📈 Improving'
        elif diff < -0.2:
            return '📉 Declining'
        else:
            return '➡️ Stable'
    
    def get_emotion_distribution(self):
        """Get distribution of emotions"""
        if self.history.empty:
            return {}
        return self.history['emotion'].value_counts().to_dict()
    
    def predict_next_mood(self):
        """Simple mood prediction using Linear Regression"""
        if len(self.history) < 5:
            return None
        
        # Prepare data
        df = self.history.copy()
        df['timestamp_num'] = (df['timestamp'] - df['timestamp'].min()).dt.total_seconds()
        
        X = df[['timestamp_num']].values
        y = df['score'].values
        
        # Train model
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict next 24 hours
        next_time = df['timestamp_num'].max() + 86400  # +1 day
        prediction = model.predict([[next_time]])[0]
        
        # Clamp between -1 and 1
        prediction = max(-1, min(1, prediction))
        
        return round(prediction, 2)