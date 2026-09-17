"""
Text Emotion Analysis
Uses VADER + TextBlob for sentiment analysis
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob


class TextEmotionAnalyzer:
    """Analyze emotions from text"""
    
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
    
    def analyze(self, text):
        """Analyze emotion from text"""
        if not text or not text.strip():
            return {
                'emotion': 'neutral',
                'score': 0.0,
                'confidence': 0.0,
                'details': {}
            }
        
        # VADER analysis
        vader_scores = self.vader.polarity_scores(text)
        compound = vader_scores['compound']
        
        # TextBlob analysis
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Combine scores
        avg_score = (compound + polarity) / 2
        
        # Determine emotion
        if avg_score >= 0.5:
            emotion = 'very happy'
        elif avg_score >= 0.15:
            emotion = 'happy'
        elif avg_score > -0.15:
            emotion = 'neutral'
        elif avg_score > -0.5:
            emotion = 'sad'
        else:
            emotion = 'very sad'
        
        # Detect specific emotions from keywords
        text_lower = text.lower()
        
        # Anxiety detection
        anxiety_keywords = ['anxious', 'worried', 'nervous', 'scared', 'fear', 
                           'panic', 'stress', 'overwhelmed', 'tense']
        if any(word in text_lower for word in anxiety_keywords):
            emotion = 'anxious'
        
        # Anger detection
        anger_keywords = ['angry', 'mad', 'furious', 'hate', 'annoyed', 
                         'frustrated', 'irritated']
        if any(word in text_lower for word in anger_keywords):
            emotion = 'angry'
        
        # Crisis detection
        crisis_keywords = ['suicide', 'kill myself', 'end my life', 'want to die',
                          'no reason to live', 'better off dead', 'self harm',
                          'hurt myself', 'give up on life']
        if any(word in text_lower for word in crisis_keywords):
            emotion = 'crisis'
        
        return {
            'emotion': emotion,
            'score': round(avg_score, 3),
            'confidence': round(abs(avg_score), 3),
            'details': {
                'vader_compound': round(compound, 3),
                'vader_pos': round(vader_scores['pos'], 3),
                'vader_neg': round(vader_scores['neg'], 3),
                'vader_neu': round(vader_scores['neu'], 3),
                'textblob_polarity': round(polarity, 3),
                'subjectivity': round(subjectivity, 3)
            }
        }