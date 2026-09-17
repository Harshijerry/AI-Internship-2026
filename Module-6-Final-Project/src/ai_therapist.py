"""
AI Therapist
Uses Google Gemini API for therapeutic responses
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class AITherapist:
    """AI-powered therapist using Google Gemini"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and api_key != "your_api_key_here":
            self.client = genai.Client(api_key=api_key)
            self.available = True
        else:
            self.available = False
        
        # System prompt for therapeutic responses
        self.system_prompt = """You are MoodMentor, a compassionate AI mental health companion. 
        Your role is to:
        1. Listen empathetically without judgment
        2. Validate the user's feelings
        3. Offer gentle, evidence-based coping strategies
        4. Ask thoughtful follow-up questions
        5. Encourage professional help when appropriate
        
        Guidelines:
        - Be warm, supportive, and non-clinical
        - Never diagnose or prescribe
        - For crisis situations, immediately suggest professional help
        - Use simple, clear language
        - Keep responses concise (100-200 words)
        - Focus on the user's strengths and resilience
        - Include one actionable suggestion per response
        """
    
    def get_response(self, user_message, emotion_data=None, conversation_history=None):
        """Get therapeutic response from AI"""
        if not self.available:
            return self._fallback_response(user_message, emotion_data)
        
        # Build context
        context = ""
        if emotion_data:
            context = f"""
            User's current emotional state: {emotion_data.get('emotion', 'neutral')}
            Sentiment score: {emotion_data.get('score', 0.0)}
            """
        
        # Build full prompt
        full_prompt = f"""
        {self.system_prompt}
        
        {context}
        
        User's message: "{user_message}"
        
        Provide a compassionate, supportive response:
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=full_prompt
            )
            return response.text
        except Exception as e:
            return self._fallback_response(user_message, emotion_data)
    
    def _fallback_response(self, user_message, emotion_data):
        """Fallback response when AI unavailable"""
        emotion = emotion_data.get('emotion', 'neutral') if emotion_data else 'neutral'
        
        responses = {
            'very happy': "I'm so glad you're feeling wonderful! 🌟 What's contributing to this happiness?",
            'happy': "It's great to hear you're in a good mood! 😊 What made your day good?",
            'neutral': "Thank you for sharing. How are you really feeling right now? 💭",
            'sad': "I hear that you're feeling down. 💙 That's completely valid. Would you like to talk about what's on your mind?",
            'very sad': "I'm here for you. 🤗 Your feelings matter. Please consider reaching out to someone you trust or a professional. Would you like to share more?",
            'anxious': "Anxiety can feel overwhelming. 🌊 Try taking 3 deep breaths with me. What's worrying you right now?",
            'angry': "It's okay to feel angry. 🔥 Your feelings are valid. What triggered this emotion?",
            'crisis': "🚨 Your safety is the most important thing right now. Please reach out immediately:\n\n**India Helplines:**\n- iCall: 9152987821\n- Vandrevala: 1860-2662-345\n- AASRA: 9820466726\n\nYou're not alone. Please contact someone now. 💙"
        }
        
        return responses.get(emotion, "I'm here to listen. Tell me more about how you're feeling. 💙")
    
    def get_coping_strategy(self, emotion):
        """Get specific coping strategy for emotion"""
        if not self.available:
            return self._fallback_coping(emotion)
        
        prompt = f"""
        The user is feeling {emotion}. Suggest one practical, evidence-based coping strategy 
        they can try right now. Keep it to 2-3 sentences with clear steps.
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            return response.text
        except:
            return self._fallback_coping(emotion)
    
    def _fallback_coping(self, emotion):
        """Fallback coping strategies"""
        strategies = {
            'anxious': "🫁 Try **Box Breathing**: Inhale 4s → Hold 4s → Exhale 4s → Hold 4s. Repeat 5 times.",
            'sad': "🌞 **Behavioral Activation**: Do one small pleasant activity (walk, music, tea). Small steps help.",
            'angry': "❄️ **Cool Down**: Splash cold water on face, walk away, or do 10 jumping jacks.",
            'stress': "📝 **Brain Dump**: Write down everything worrying you. Then circle what you can control.",
            'neutral': "🎯 **Gratitude**: Write down 3 things you're grateful for today.",
        }
        return strategies.get(emotion, "💙 Take 5 deep breaths and notice how you feel.")
    
    def get_affirmation(self, emotion):
        """Get positive affirmation for emotion"""
        if not self.available:
            return self._fallback_affirmation(emotion)
        
        prompt = f"Create one short, powerful positive affirmation (1 sentence) for someone feeling {emotion}. Make it personal and warm."
        
        try:
            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            return response.text.strip()
        except:
            return self._fallback_affirmation(emotion)
    
    def _fallback_affirmation(self, emotion):
        """Fallback affirmations"""
        affirmations = {
            'anxious': "You are safe. This feeling will pass. You've handled hard things before. 🌊",
            'sad': "Your feelings are valid. You are worthy of love and kindness. 💙",
            'angry': "Your emotions matter. You can express them in healthy ways. 🔥",
            'happy': "You deserve this joy. Let yourself fully enjoy this moment. ✨",
            'neutral': "You are enough exactly as you are right now. 🌸",
        }
        return affirmations.get(emotion, "You are doing your best, and that is enough. 💙")