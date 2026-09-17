"""
MoodMentor - AI Mental Health Companion
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from PIL import Image
import sys

sys.path.append('src')

from text_emotion import TextEmotionAnalyzer
from face_emotion import FaceEmotionDetector
from ai_therapist import AITherapist
from mood_tracker import MoodTracker

# Page config
st.set_page_config(
    page_title="MoodMentor - AI Mental Health Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .chat-user {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .chat-ai {
        background-color: #f3e5f5;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .crisis-box {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 15px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)


# Initialize components
@st.cache_resource
def init_components():
    return {
        'text_analyzer': TextEmotionAnalyzer(),
        'face_detector': FaceEmotionDetector(),
        'therapist': AITherapist(),
        'tracker': MoodTracker()
    }


def main():
    components = init_components()
    
    # Header
    st.markdown('<h1 class="main-header">🧠 MoodMentor</h1>', unsafe_allow_html=True)
    st.markdown("### Your AI-Powered Mental Health Companion 💙")
    
    # Sidebar
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.radio(
        "Choose a section:",
        ["🏠 Home", "💬 Chat with AI", "📸 Face Analysis", "📊 Mood Dashboard", "📖 About"]
    )
    
    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_emotion' not in st.session_state:
        st.session_state.current_emotion = None
    
    # ===== HOME PAGE =====
    if page == "🏠 Home":
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ## Welcome to MoodMentor 🌟
            
            MoodMentor is your personal AI companion for emotional wellness. 
            It uses advanced AI to understand your feelings and provide support.
            
            ### ✨ What You Can Do:
            - 💬 **Chat** with an empathetic AI therapist
            - 📸 **Analyze** your facial expressions
            - 📊 **Track** your mood patterns over time
            - 🧘 **Get** personalized coping strategies
            
            ### 🎯 How It Works:
            1. Share how you're feeling (text or photo)
            2. AI analyzes your emotion
            3. Get compassionate responses & suggestions
            4. Track your emotional journey
            
            ---
            
            ### 💡 Remember:
            **MoodMentor is a supportive tool, not a replacement for professional help.**
            If you're in crisis, please contact:
            - **iCall:** 9152987821
            - **Vandrevala:** 1860-2662-345
            - **AASRA:** 9820466726
            """)
        
        with col2:
            st.markdown("### 📊 Your Stats")
            stats = components['tracker'].get_statistics()
            
            st.metric("Total Entries", stats['total_entries'])
            st.metric("Average Mood", f"{stats['avg_mood']:.2f}")
            st.metric("Trend", stats['trend'])
            
            if st.button("🚀 Start Chatting", type="primary", use_container_width=True):
                st.info("👉 Go to 'Chat with AI' from the sidebar!")
    
    # ===== CHAT PAGE =====
    elif page == "💬 Chat with AI":
        st.header("💬 Talk to MoodMentor")
        st.markdown("_Share how you're feeling. I'm here to listen._ 💙")
        
        # Chat display
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.chat_history:
                if msg['role'] == 'user':
                    st.markdown(f'<div class="chat-user">👤 <b>You:</b> {msg["content"]}</div>', 
                              unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-ai">🧠 <b>MoodMentor:</b> {msg["content"]}</div>', 
                              unsafe_allow_html=True)
        
        # Input
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input("Type your message...", key="chat_input",
                                       placeholder="I'm feeling...")
        with col2:
            send = st.button("Send 📤", type="primary", use_container_width=True)
        
        if send and user_input:
            # Analyze emotion
            emotion_data = components['text_analyzer'].analyze(user_input)
            st.session_state.current_emotion = emotion_data
            
            # Log mood
            components['tracker'].log_mood(
                emotion_data['emotion'],
                emotion_data['score'],
                user_input,
                'text'
            )
            
            # Add user message
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input,
                'emotion': emotion_data
            })
            
            # Crisis check
            if emotion_data['emotion'] == 'crisis':
                crisis_msg = """🚨 **I'm very concerned about what you shared.**

Please reach out to a professional RIGHT NOW:

**India Helplines (24/7):**
- **iCall:** 9152987821
- **Vandrevala Foundation:** 1860-2662-345
- **AASRA:** 9820466726
- **Emergency:** 112

You matter. Your life has value. Please talk to someone. 💙"""
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': crisis_msg
                })
                st.markdown(f'<div class="crisis-box">{crisis_msg}</div>', unsafe_allow_html=True)
            else:
                # Get AI response
                with st.spinner("Thinking..."):
                    response = components['therapist'].get_response(
                        user_input,
                        emotion_data
                    )
                
                # Add AI response
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response
                })
            
            st.rerun()
        
        # Quick prompts
        st.markdown("---")
        st.markdown("### 💡 Quick Prompts")
        quick_prompts = [
            "I'm feeling anxious today",
            "I had a great day!",
            "I'm stressed about work",
            "I feel lonely",
            "I'm grateful for..."
        ]
        
        cols = st.columns(5)
        for i, prompt in enumerate(quick_prompts):
            with cols[i]:
                if st.button(prompt, key=f"qp_{i}", use_container_width=True):
                    # Analyze and respond
                    emotion_data = components['text_analyzer'].analyze(prompt)
                    response = components['therapist'].get_response(prompt, emotion_data)
                    
                    st.session_state.chat_history.append({'role': 'user', 'content': prompt})
                    st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                    
                    components['tracker'].log_mood(
                        emotion_data['emotion'],
                        emotion_data['score'],
                        prompt, 'text'
                    )
                    
                    st.rerun()
        
        # Clear chat
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    # ===== FACE ANALYSIS PAGE =====
    elif page == "📸 Face Analysis":
        st.header("📸 Facial Emotion Analysis")
        st.markdown("_Upload or take a photo to analyze your facial expression_")
        
        tab1, tab2 = st.tabs(["📁 Upload Photo", "📷 Take Photo"])
        
        image = None
        
        with tab1:
            uploaded = st.file_uploader("Upload a photo", type=['jpg', 'jpeg', 'png'])
            if uploaded:
                image = Image.open(uploaded)
        
        with tab2:
            camera = st.camera_input("Take a photo")
            if camera:
                image = Image.open(camera)
        
        if image is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(image, caption="Your Photo", use_column_width=True)
            
            with col2:
                with st.spinner("Analyzing facial expression..."):
                    result = components['face_detector'].analyze(image)
                
                if result['face_detected']:
                    emotion = result['emotion']
                    confidence = result['confidence']
                    
                    st.success(f"**Detected Emotion:** {emotion.title()}")
                    st.metric("Confidence", f"{confidence*100:.0f}%")
                    
                    # Get AI response for this emotion
                    emotion_map = {
                        'happy': 0.8,
                        'neutral': 0.0,
                        'surprised': 0.2
                    }
                    score = emotion_map.get(emotion, 0.0)
                    
                    # Log mood
                    components['tracker'].log_mood(
                        emotion, score,
                        'From face analysis',
                        'face'
                    )
                    
                    # Get coping strategy
                    strategy = components['therapist'].get_coping_strategy(emotion)
                    st.info(f"💡 **Suggestion:** {strategy}")
                    
                    # Affirmation
                    affirmation = components['therapist'].get_affirmation(emotion)
                    st.markdown(f"### ✨ *{affirmation}*")
                else:
                    st.warning(f"⚠️ {result['details']}")
                    st.info("Please ensure your face is clearly visible in the photo.")
    
    # ===== DASHBOARD PAGE =====
    elif page == "📊 Mood Dashboard":
        st.header("📊 Your Mood Dashboard")
        
        history = components['tracker'].history
        
        if history.empty:
            st.info("📭 No mood data yet. Start chatting or upload photos to track your mood!")
        else:
            # Statistics
            stats = components['tracker'].get_statistics()
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📝 Total Entries", stats['total_entries'])
            col2.metric("💙 Average Mood", f"{stats['avg_mood']:.2f}")
            col3.metric("🎯 Most Common", stats['most_common'].title())
            col4.metric("📈 Trend", stats['trend'])
            
            st.markdown("---")
            
            # Mood over time
            st.subheader("📈 Mood Trend Over Time")
            fig1 = px.line(
                history,
                x='timestamp',
                y='score',
                title='Your Mood Journey',
                labels={'score': 'Mood Score', 'timestamp': 'Date'},
                markers=True
            )
            fig1.update_traces(line_color='#667eea', line_width=3)
            fig1.add_hline(y=0, line_dash="dash", line_color="gray", 
                          annotation_text="Neutral")
            st.plotly_chart(fig1, use_container_width=True)
            
            # Emotion distribution
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎭 Emotion Distribution")
                emotion_dist = components['tracker'].get_emotion_distribution()
                if emotion_dist:
                    fig2 = px.pie(
                        values=list(emotion_dist.values()),
                        names=list(emotion_dist.keys()),
                        title='Emotions Breakdown',
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    st.plotly_chart(fig2, use_container_width=True)
            
            with col2:
                st.subheader("🔮 Next Mood Prediction")
                prediction = components['tracker'].predict_next_mood()
                if prediction is not None:
                    if prediction > 0.2:
                        st.success(f"🌟 Predicted mood: **Positive ({prediction})**")
                        st.markdown("Your mood trend suggests things are looking up!")
                    elif prediction < -0.2:
                        st.warning(f"⚠️ Predicted mood: **Low ({prediction})**")
                        st.markdown("Consider self-care activities today. 💙")
                    else:
                        st.info(f"😐 Predicted mood: **Neutral ({prediction})**")
                else:
                    st.info("Need more data to predict (minimum 5 entries)")
            
            # Recent entries table
            st.subheader("📋 Recent Mood Entries")
            recent = history.tail(10)[['timestamp', 'emotion', 'score', 'source']].copy()
            recent['timestamp'] = recent['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(recent, use_container_width=True)
            
            # Export
            csv = history.to_csv(index=False)
            st.download_button(
                "📥 Download Mood History (CSV)",
                csv,
                "mood_history.csv",
                "text/csv"
            )
    
    # ===== ABOUT PAGE =====
    elif page == "📖 About":
        st.header("📖 About MoodMentor")
        
        st.markdown("""
        ## 🧠 What is MoodMentor?
        
        MoodMentor is an AI-powered mental health companion that helps you:
        - Understand your emotions better
        - Track mood patterns over time
        - Get personalized support and coping strategies
        
        ## 🛠️ Technology Stack
        
        | Component | Technology |
        |-----------|-----------|
        | **AI Model** | Google Gemini 3.6 Flash |
        | **Text Emotion** | VADER + TextBlob |
        | **Face Detection** | OpenCV Haar Cascades |
        | **ML Prediction** | Scikit-learn Linear Regression |
        | **Visualization** | Plotly, Matplotlib |
        | **Web Framework** | Streamlit |
        
        ## ⚠️ Important Disclaimer
        
        **MoodMentor is NOT a replacement for professional mental health care.**
        
        If you're experiencing a mental health crisis:
        - **India:** iCall (9152987821), Vandrevala (1860-2662-345)
        - **Emergency:** 112
        
        ## 👨‍💻 Developer
        
        Built with 💙 by **Harshini**  
        Codomax AI Internship 2026
        """)


if __name__ == "__main__":
    main()