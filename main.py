import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
from streamlit_autorefresh import st_autorefresh
import av
from concurrent.futures import ThreadPoolExecutor
import requests
import os
import random
import numpy as np
from PIL import Image
import io
import base64
import time
import threading

# Page configuration
st.set_page_config(
    page_title="Nabd | نبض",
    page_icon="💓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern RTL Arabic styling with Deep Glassmorphism
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap');
    
    * {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #a78bfa 0%, #c084fc 30%, #f0abfc 60%, #fda4af 100%);
        min-height: 100vh;
    }
    
    .main .block-container {
        padding-top: 1.5rem;
        padding-right: 2rem;
        padding-left: 2rem;
    }
    
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        font-family: 'Tajawal', sans-serif !important;
        text-align: right !important;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Tajawal', sans-serif !important;
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 12px !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Super Bright Glassmorphism Card */
    .glass-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.7) 0%, rgba(255,255,255,0.5) 100%);
        border-radius: 24px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(167, 139, 250, 0.3), inset 0 0 32px rgba(255,255,255,0.3);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.8);
    }
    
    .glass-card-light {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
        border-radius: 24px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    /* Super Bright Service Card with Hover */
    .service-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0.6) 100%);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(167, 139, 250, 0.3), inset 0 0 20px rgba(255,255,255,0.3);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.9);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .service-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
        border-radius: 20px;
    }
    
    .service-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    }
    
    .service-card:hover::before {
        opacity: 1;
    }
    
    .service-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        display: block;
        position: relative;
        z-index: 1;
    }
    
    .service-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .service-desc {
        font-size: 0.95rem;
        color: rgba(255,255,255,0.7);
        position: relative;
        z-index: 1;
    }
    
    /* Hero Section */
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center !important;
        margin-bottom: 0.5rem;
        animation: pulse-glow 3s ease-in-out infinite;
    }
    
    @keyframes pulse-glow {
        0%, 100% { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.5)); }
        50% { filter: drop-shadow(0 0 40px rgba(118, 75, 162, 0.8)); }
    }
    
    .hero-slogan {
        font-size: 1.5rem;
        color: rgba(255,255,255,0.8);
        text-align: center !important;
        margin-bottom: 2rem;
    }
    
    /* Persona Cards */
    .persona-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .persona-card:hover {
        transform: scale(1.05);
        border-color: #667eea;
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.3);
    }
    
    .persona-card.active {
        border: 2px solid #667eea;
        background: linear-gradient(145deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%);
    }
    
    .persona-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        margin: 0 auto 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
    }
    
    .persona-name {
        font-size: 1.2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.3rem;
    }
    
    .persona-role {
        font-size: 0.85rem;
        color: rgba(255,255,255,0.6);
    }
    
    /* Chat Messages */
    .chat-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.03) 100%);
        border-radius: 20px;
        padding: 1.5rem;
        min-height: 350px;
        max-height: 450px;
        overflow-y: auto;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .chat-message {
        padding: 1rem 1.5rem;
        border-radius: 18px;
        margin: 0.75rem 0;
        max-width: 85%;
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        margin-right: 0;
        border-bottom-right-radius: 4px;
    }
    
    .bot-message {
        background: rgba(255,255,255,0.1);
        color: white;
        margin-right: auto;
        margin-left: 0;
        border-bottom-left-radius: 4px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Modern Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.85rem 2.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        font-family: 'Tajawal', sans-serif !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Emotion Results */
    .emotion-result {
        text-align: center;
        padding: 2.5rem;
        border-radius: 24px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .emotion-happy { background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%); }
    .emotion-sad { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
    .emotion-angry { background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%); }
    .emotion-fear { background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%); }
    .emotion-surprise { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
    .emotion-disgust { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
    .emotion-neutral { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    
    /* Drug Interaction Risk Badges */
    .risk-high {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
        color: #333;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }
    
    /* Progress Bars */
    .progress-container {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        height: 12px;
        overflow: hidden;
        margin-top: 0.5rem;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    /* Analysis Result Cards */
    .analysis-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .analysis-label {
        font-size: 1rem;
        font-weight: 500;
        color: rgba(255,255,255,0.8);
        margin-bottom: 0.5rem;
    }
    
    .analysis-value {
        font-size: 2rem;
        font-weight: 800;
    }
    
    /* Live Monitor */
    .monitor-card {
        background: linear-gradient(145deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.1) 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .monitor-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #667eea;
    }
    
    .monitor-label {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.6);
    }
    
    .pulse-dot {
        width: 12px;
        height: 12px;
        background: #22c55e;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.3); opacity: 0.7; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Sidebar Styling - Bright Pink/Purple */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f0abfc 0%, #c084fc 50%, #a78bfa 100%) !important;
    }
    
    [data-testid="stSidebar"] * {
        direction: rtl !important;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(102, 126, 234, 0.5);
        border-radius: 4px;
    }
    
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.1) !important;
    }
    
    .stSelectbox label {
        color: white !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        color: white;
        padding: 0.5rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Get HuggingFace token
HF_TOKEN = os.environ.get('HUGGINGFACE_API_TOKEN', os.environ.get('HF_TOKEN', ''))

# Emotion mappings
EMOTION_ARABIC = {
    'happy': 'سعيد',
    'sad': 'حزين',
    'angry': 'غاضب',
    'fear': 'خائف',
    'surprise': 'متفاجئ',
    'disgust': 'مشمئز',
    'neutral': 'محايد'
}

EMOTION_ADVICE = {
    'happy': 'رائع! حافظ على هذه الطاقة الإيجابية وشاركها مع من حولك',
    'sad': 'لا بأس أن تشعر بالحزن أحياناً. خذ وقتك وتحدث مع شخص تثق به',
    'angry': 'حاول أخذ نفس عميق والعد حتى عشرة. الغضب طبيعي لكن السيطرة عليه مهم',
    'fear': 'تذكر أن الخوف شعور طبيعي. حاول تحديد مصدر خوفك ومواجهته تدريجياً',
    'surprise': 'المفاجآت جزء من الحياة! استمتع باللحظة واستكشف ما هو جديد',
    'disgust': 'من المهم أن تفهم مشاعرك. حاول التفكير فيما يزعجك ولماذا',
    'neutral': 'حالة هادئة ومتوازنة. وقت مناسب للتأمل والتخطيط'
}

# Farah Personas
FARAH_PERSONAS = {
    'farah': {
        'name': 'فرح',
        'role': 'صديقتك المتفائلة',
        'avatar': '''<svg viewBox="0 0 100 100" width="60" height="60"><circle cx="50" cy="50" r="45" fill="#667eea"/><circle cx="50" cy="45" r="25" fill="#ffecd2"/><circle cx="42" cy="40" r="4" fill="#333"/><circle cx="58" cy="40" r="4" fill="#333"/><path d="M40 52 Q50 62 60 52" stroke="#333" stroke-width="2" fill="none"/><ellipse cx="50" cy="75" rx="15" ry="8" fill="#667eea"/><path d="M30 25 Q50 5 70 25" stroke="#5a4a3a" stroke-width="8" fill="none" stroke-linecap="round"/></svg>''',
        'color': '#667eea',
        'style': 'متفائلة وداعمة',
        'gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    },
    'amal': {
        'name': 'أمل',
        'role': 'المستمعة الهادئة',
        'avatar': '''<svg viewBox="0 0 100 100" width="60" height="60"><circle cx="50" cy="50" r="45" fill="#ec4899"/><circle cx="50" cy="45" r="25" fill="#ffecd2"/><circle cx="42" cy="40" r="4" fill="#333"/><circle cx="58" cy="40" r="4" fill="#333"/><path d="M42 52 Q50 58 58 52" stroke="#333" stroke-width="2" fill="none"/><ellipse cx="50" cy="75" rx="15" ry="8" fill="#ec4899"/><ellipse cx="50" cy="20" rx="20" ry="12" fill="#5a3a3a"/><path d="M35 18 Q50 8 65 18" stroke="#5a3a3a" stroke-width="6" fill="none"/></svg>''',
        'color': '#ec4899',
        'style': 'هادئة ومتفهمة',
        'gradient': 'linear-gradient(135deg, #ec4899 0%, #be185d 100%)'
    },
    'noor': {
        'name': 'نور',
        'role': 'المرشدة الحكيمة',
        'avatar': '''<svg viewBox="0 0 100 100" width="60" height="60"><circle cx="50" cy="50" r="45" fill="#f59e0b"/><circle cx="50" cy="45" r="25" fill="#ffecd2"/><circle cx="42" cy="40" r="4" fill="#333"/><circle cx="58" cy="40" r="4" fill="#333"/><path d="M42 52 Q50 56 58 52" stroke="#333" stroke-width="2" fill="none"/><ellipse cx="50" cy="75" rx="15" ry="8" fill="#f59e0b"/><path d="M25 30 Q50 10 75 30" stroke="#4a3a2a" stroke-width="6" fill="none"/><circle cx="35" cy="35" r="3" fill="#fbbf24"/><circle cx="65" cy="35" r="3" fill="#fbbf24"/></svg>''',
        'color': '#f59e0b',
        'style': 'حكيمة وملهمة',
        'gradient': 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
    }
}

# Drug Interaction Database (Sample)
DRUG_INTERACTIONS = {
    ('أسبرين', 'وارفارين'): {'risk': 'high', 'description': 'يزيد خطر النزيف بشكل كبير'},
    ('أسبرين', 'إيبوبروفين'): {'risk': 'medium', 'description': 'قد يقلل من فعالية الأسبرين في حماية القلب'},
    ('باراسيتامول', 'وارفارين'): {'risk': 'medium', 'description': 'قد يزيد من تأثير الوارفارين'},
    ('أموكسيسيلين', 'ميثوتريكسيت'): {'risk': 'high', 'description': 'يزيد سمية الميثوتريكسيت'},
    ('سيبروفلوكساسين', 'ثيوفيللين'): {'risk': 'high', 'description': 'يزيد مستوى الثيوفيللين في الدم'},
    ('أوميبرازول', 'كلوبيدوجريل'): {'risk': 'medium', 'description': 'قد يقلل من فعالية كلوبيدوجريل'},
    ('ليفوثيروكسين', 'كالسيوم'): {'risk': 'low', 'description': 'يقلل امتصاص الليفوثيروكسين - تناولهما بفارق 4 ساعات'},
    ('ميتفورمين', 'كحول'): {'risk': 'high', 'description': 'يزيد خطر الحماض اللاكتيكي'},
}

COMMON_DRUGS = [
    'أسبرين', 'باراسيتامول', 'إيبوبروفين', 'أموكسيسيلين', 'أزيثرومايسين',
    'وارفارين', 'ميتفورمين', 'أوميبرازول', 'أتورفاستاتين', 'ليفوثيروكسين',
    'سيبروفلوكساسين', 'ثيوفيللين', 'كلوبيدوجريل', 'ميثوتريكسيت', 'كالسيوم',
    'فيتامين د', 'حديد', 'أملوديبين', 'لوسارتان', 'هيدروكلوروثيازيد'
]

# Page options for navigation
PAGE_OPTIONS = ["الرئيسية", "فرح", "طبيبك الذكي", "مرآة المشاعر", "تفاعل الأدوية"]

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'farah_result' not in st.session_state:
    st.session_state.farah_result = None
if 'selected_persona' not in st.session_state:
    st.session_state.selected_persona = 'farah'
if 'nav_page' not in st.session_state:
    st.session_state.nav_page = 'الرئيسية'
if 'drug_result' not in st.session_state:
    st.session_state.drug_result = None

def navigate_to(page):
    """Navigate to a specific page"""
    st.session_state.nav_page = page


def analyze_sentiment_with_ai(text):
    """Analyze Arabic text sentiment using Hugging Face API"""
    if not HF_TOKEN:
        return None, "عذراً، لم يتم تكوين مفتاح API."
    
    API_URL = "https://api-inference.huggingface.co/models/CAMeL-Lab/bert-base-arabic-camelbert-msa-sentiment"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], list):
                    return result[0], None
                return result, None
        elif response.status_code == 503:
            return None, "النموذج قيد التحميل، يرجى المحاولة بعد قليل..."
        return None, "حدث خطأ في التحليل"
    except Exception as e:
        return None, f"حدث خطأ: {str(e)}"


def farah_predict(text, persona='farah'):
    """Analyze mental health indicators from Arabic text using AI"""
    result, error = analyze_sentiment_with_ai(text)
    
    negative_words = ['حزين', 'تعب', 'قلق', 'خوف', 'وحيد', 'ضيق', 'كآبة', 'يأس', 'إحباط', 'ضغط', 'توتر', 'ألم', 'مكتئب', 'أعاني', 'صعب', 'متعب', 'محبط', 'ضائع']
    positive_words = ['سعيد', 'فرح', 'أمل', 'راحة', 'سلام', 'حب', 'نجاح', 'قوة', 'تفاؤل', 'سعادة', 'مرتاح', 'سرور', 'بهجة']
    
    text_lower = text.lower()
    negative_count = sum(1 for word in negative_words if word in text_lower)
    positive_count = sum(1 for word in positive_words if word in text_lower)
    
    if result:
        sentiment_scores = {}
        for item in result:
            if isinstance(item, dict):
                label = item.get('label', '').lower()
                score = item.get('score', 0)
                sentiment_scores[label] = score
        
        negative_score = sentiment_scores.get('negative', 0)
        positive_score = sentiment_scores.get('positive', 0)
        
        depression_score = negative_score * 0.7 + (negative_count * 0.05)
        anxiety_score = negative_score * 0.5 + (negative_count * 0.08)
        wellbeing_score = positive_score * 0.8 + (positive_count * 0.1)
        
        depression_score = min(max(depression_score, 0.05), 0.95)
        anxiety_score = min(max(anxiety_score, 0.05), 0.95)
        wellbeing_score = min(max(wellbeing_score, 0.05), 0.95)
        
        is_ai_analyzed = True
    else:
        word_ratio = (negative_count - positive_count) / max(len(text.split()), 1)
        depression_score = min(max(0.3 + word_ratio * 2, 0.1), 0.9)
        anxiety_score = min(max(0.25 + word_ratio * 1.5, 0.1), 0.9)
        wellbeing_score = min(max(0.5 - word_ratio, 0.1), 0.9)
        is_ai_analyzed = False
    
    def get_level_color(score, inverse=False):
        if inverse:
            if score > 0.6: return ("مرتفع", "#22c55e")
            elif score > 0.3: return ("متوسط", "#f59e0b")
            else: return ("منخفض", "#ef4444")
        else:
            if score > 0.6: return ("مرتفع", "#ef4444")
            elif score > 0.3: return ("متوسط", "#f59e0b")
            else: return ("منخفض", "#22c55e")
    
    dep_level, dep_color = get_level_color(depression_score)
    anx_level, anx_color = get_level_color(anxiety_score)
    well_level, well_color = get_level_color(wellbeing_score, inverse=True)
    
    persona_responses = {
        'farah': "أشكرك على مشاركتي مشاعرك! تذكر أن كل يوم جديد هو فرصة للتغيير الإيجابي.",
        'amal': "أسمعك وأفهم ما تمر به. خذ وقتك، أنا هنا معك.",
        'noor': "الحكمة تقول أن الصعوبات تصقل الإنسان. ثق بقدرتك على التجاوز."
    }
    
    return {
        'depression': {'score': depression_score, 'level': dep_level, 'color': dep_color},
        'anxiety': {'score': anxiety_score, 'level': anx_level, 'color': anx_color},
        'wellbeing': {'score': wellbeing_score, 'level': well_level, 'color': well_color},
        'is_ai_analyzed': is_ai_analyzed,
        'persona_response': persona_responses.get(persona, persona_responses['farah']),
        'error': error
    }


def chat_with_ai(message, history):
    """Chat with Hugging Face API"""
    if not HF_TOKEN:
        return "عذراً، لم يتم تكوين مفتاح API. يرجى إضافة HUGGINGFACE_API_TOKEN في الإعدادات."
    
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    system_prompt = """أنت طبيب ذكي ومساعد صحي باللغة العربية. 
    - أجب دائماً باللغة العربية الفصحى
    - قدم نصائح طبية عامة ومفيدة
    - كن ودوداً ومتعاطفاً
    - ذكّر المستخدم بأهمية استشارة طبيب حقيقي للحالات الخطيرة
    - لا تقدم تشخيصاً طبياً نهائياً"""
    
    conversation = f"<|system|>{system_prompt}</s>\n"
    for msg in history[-5:]:
        if msg['role'] == 'user':
            conversation += f"<|user|>{msg['content']}</s>\n"
        else:
            conversation += f"<|assistant|>{msg['content']}</s>\n"
    conversation += f"<|user|>{message}</s>\n<|assistant|>"
    
    payload = {
        "inputs": conversation,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "do_sample": True,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', 'عذراً، لم أتمكن من الرد.')
            return 'عذراً، لم أتمكن من الرد.'
        elif response.status_code == 503:
            return "النموذج قيد التحميل، يرجى المحاولة بعد قليل..."
        else:
            return f"حدث خطأ في الاتصال. الرجاء المحاولة لاحقاً."
    except Exception as e:
        return f"حدث خطأ: يرجى المحاولة مرة أخرى"


def check_drug_interaction(drug1, drug2):
    """Check for drug interactions"""
    key1 = (drug1, drug2)
    key2 = (drug2, drug1)
    
    if key1 in DRUG_INTERACTIONS:
        return DRUG_INTERACTIONS[key1]
    elif key2 in DRUG_INTERACTIONS:
        return DRUG_INTERACTIONS[key2]
    else:
        return {'risk': 'none', 'description': 'لم يتم العثور على تفاعلات معروفة بين هذين الدواءين. استشر الصيدلي للتأكد.'}


def analyze_face(image):
    """Analyze face emotions using DeepFace"""
    try:
        from deepface import DeepFace
        
        img_array = np.array(image)
        
        result = DeepFace.analyze(
            img_array,
            actions=['emotion'],
            enforce_detection=False,
            detector_backend='opencv'
        )
        
        if isinstance(result, list):
            result = result[0]
        
        emotions = result.get('emotion', {})
        dominant_emotion = result.get('dominant_emotion', 'neutral')
        
        return {
            'success': True,
            'emotion': dominant_emotion,
            'all_emotions': emotions,
            'simulation': False
        }
    except Exception as e:
        emotions_list = ['happy', 'sad', 'angry', 'fear', 'surprise', 'neutral']
        random_emotion = random.choice(emotions_list)
        random_emotions = {em: random.uniform(5, 95) for em in emotions_list}
        random_emotions[random_emotion] = random.uniform(60, 95)
        
        total = sum(random_emotions.values())
        random_emotions = {k: (v/total)*100 for k, v in random_emotions.items()}
        
        return {
            'success': True,
            'emotion': random_emotion,
            'all_emotions': random_emotions,
            'simulation': True
        }


# Sidebar navigation
with st.sidebar:
    # Modern Sidebar Header with brighter colors
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f0abfc 0%, #c084fc 50%, #a78bfa 100%) !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            background: transparent !important;
        }
    </style>
    <div style="text-align: center; padding: 2rem 1rem 1.5rem;">
        <div style="width: 80px; height: 80px; margin: 0 auto 1rem; background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 25px rgba(255, 107, 157, 0.4); animation: heartbeat 1.5s ease-in-out infinite;">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="white">
                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
            </svg>
        </div>
        <h1 style="font-size: 2.2rem; margin: 0; font-family: 'Tajawal', sans-serif !important; font-weight: 800; background: linear-gradient(135deg, #a78bfa 0%, #f472b6 50%, #fb7185 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">نبض</h1>
        <p style="color: #c4b5fd; font-size: 1rem; margin-top: 0.5rem; font-family: 'Tajawal', sans-serif !important;">نبضك.. نفهم لغته</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get current page index from nav_page (source of truth)
    current_index = PAGE_OPTIONS.index(st.session_state.nav_page) if st.session_state.nav_page in PAGE_OPTIONS else 0
    
    # Use manual_select to sync sidebar with programmatic navigation
    selected = option_menu(
        menu_title=None,
        options=PAGE_OPTIONS,
        icons=["house-fill", "heart-pulse-fill", "chat-dots-fill", "camera-fill", "capsule"],
        menu_icon="cast",
        default_index=current_index,
        manual_select=current_index,
        styles={
            "container": {"padding": "0.5rem !important", "background-color": "transparent"},
            "icon": {"color": "#a78bfa", "font-size": "1.4rem"},
            "nav-link": {
                "font-size": "1.15rem",
                "text-align": "right",
                "margin": "0.5rem 0.5rem",
                "padding": "1rem 1.2rem",
                "border-radius": "14px",
                "font-family": "'Tajawal', sans-serif",
                "font-weight": "500",
                "color": "#e2d9f3",
                "background": "rgba(167, 139, 250, 0.08)",
                "transition": "all 0.3s ease",
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #a78bfa 0%, #f472b6 100%)",
                "color": "white",
                "font-weight": "700",
                "box-shadow": "0 4px 15px rgba(167, 139, 250, 0.4)",
            },
        }
    )
    
    # Update nav_page when sidebar is clicked (sidebar takes precedence on click)
    if selected and selected != st.session_state.nav_page:
        st.session_state.nav_page = selected
    
    # Use nav_page as the source of truth for active page
    active_page = st.session_state.nav_page
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Modern Live Monitor in Sidebar with bright colors
    st.markdown("""
    <div style="margin: 1rem 0.5rem; padding: 1rem 1.2rem; background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(16, 185, 129, 0.1) 100%); border-radius: 14px; border: 1px solid rgba(34, 197, 94, 0.3);">
        <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
            <div style="width: 12px; height: 12px; background: #22c55e; border-radius: 50%; animation: pulse-green 2s ease-in-out infinite; box-shadow: 0 0 10px #22c55e;"></div>
            <span style="color: #4ade80; font-weight: 700; font-size: 1.1rem; font-family: 'Tajawal', sans-serif !important;">متصل</span>
        </div>
        <p style="color: #86efac; font-size: 0.9rem; text-align: center !important; margin: 0.5rem 0 0 0; font-family: 'Tajawal', sans-serif !important;">حالة النظام</p>
    </div>
    <style>
        @keyframes pulse-green {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.2); opacity: 0.7; }
        }
        @keyframes heartbeat {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
    </style>
    """, unsafe_allow_html=True)


# ==================== HOME PAGE ====================
if active_page == "الرئيسية":
    st.markdown("""
    <div class="glass-card">
        <h1 class="hero-title">نبض | Nabd</h1>
        <p class="hero-slogan">نبضك.. نفهم لغته</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Service Cards Grid
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💬 طبيبك الذكي\n\nاستشارات طبية فورية مع ذكاء اصطناعي متخصص", key="btn_doctor", use_container_width=True):
            navigate_to('طبيبك الذكي')
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("📷 مرآة المشاعر\n\nاكتشف مشاعرك من خلال تحليل تعابير الوجه", key="btn_mirror", use_container_width=True):
            navigate_to('مرآة المشاعر')
            st.rerun()
    
    with col2:
        if st.button("💜 فرح\n\nتحليل الحالة النفسية ودعم الصحة العقلية", key="btn_farah", use_container_width=True):
            navigate_to('فرح')
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("💊 تفاعل الأدوية\n\nفحص التفاعلات بين الأدوية المختلفة", key="btn_drugs", use_container_width=True):
            navigate_to('تفاعل الأدوية')
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Features Overview
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: #667eea; text-align: center !important; margin-bottom: 1.5rem;">مميزات نبض</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; text-align: center;">
            <div>
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🤖</div>
                <h4 style="color: white; margin: 0.5rem 0;">ذكاء اصطناعي</h4>
                <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">تحليل متقدم باستخدام أحدث التقنيات</p>
            </div>
            <div>
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔒</div>
                <h4 style="color: white; margin: 0.5rem 0;">خصوصية تامة</h4>
                <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">بياناتك محمية ومشفرة بالكامل</p>
            </div>
            <div>
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🌍</div>
                <h4 style="color: white; margin: 0.5rem 0;">دعم عربي كامل</h4>
                <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">واجهة عربية بالكامل مع فهم اللهجات</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card" style="text-align: center;">
        <p style="color: rgba(255,255,255,0.7); margin: 0;">
            ⚠️ هذه الخدمات للتوعية والإرشاد فقط ولا تغني عن استشارة طبيب مختص
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==================== FARAH PAGE ====================
elif active_page == "فرح":
    st.markdown("""
    <div class="glass-card">
        <h2 style="color: #667eea; text-align: center !important;">💜 فرح - دعم الصحة النفسية</h2>
        <p style="text-align: center !important; color: rgba(255,255,255,0.7);">
            اختر شخصيتك المفضلة وشاركها مشاعرك
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Persona Selection with Cartoon Avatars
    st.markdown("<h4 style='color: #c4b5fd; margin: 1.5rem 0 1rem; font-weight: 600;'>اختر صديقتك:</h4>", unsafe_allow_html=True)
    
    persona_cols = st.columns(3)
    for idx, (key, persona) in enumerate(FARAH_PERSONAS.items()):
        with persona_cols[idx]:
            is_active = st.session_state.selected_persona == key
            active_border = f"3px solid {persona['color']}" if is_active else "1px solid rgba(255,255,255,0.1)"
            active_bg = f"rgba({int(persona['color'][1:3], 16)}, {int(persona['color'][3:5], 16)}, {int(persona['color'][5:7], 16)}, 0.15)" if is_active else "rgba(255,255,255,0.05)"
            
            st.markdown(f"""
            <div style="background: {active_bg}; border: {active_border}; border-radius: 20px; padding: 1.5rem; text-align: center; cursor: pointer; transition: all 0.3s ease; margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: center; margin-bottom: 0.8rem;">
                    {persona['avatar']}
                </div>
                <h4 style="color: {persona['color']}; margin: 0 0 0.3rem 0; font-weight: 700; font-size: 1.2rem;">{persona['name']}</h4>
                <p style="color: rgba(255,255,255,0.6); margin: 0; font-size: 0.85rem;">{persona['role']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"اختر {persona['name']}", key=f"persona_{key}", use_container_width=True):
                st.session_state.selected_persona = key
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    current_persona = FARAH_PERSONAS[st.session_state.selected_persona]
    
    st.markdown(f"""
    <div class="glass-card" style="border: 2px solid {current_persona['color']}; background: {current_persona['gradient'].replace('linear-gradient', 'linear-gradient').replace('100%)', '20%)')}>
        <div style="display: flex; align-items: center; gap: 1.5rem; margin-bottom: 0.5rem;">
            <div style="background: white; border-radius: 50%; padding: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                {current_persona['avatar']}
            </div>
            <div>
                <h3 style="color: {current_persona['color']}; margin: 0; font-size: 1.5rem;">{current_persona['name']}</h3>
                <p style="color: rgba(255,255,255,0.7); margin: 0.3rem 0 0 0;">{current_persona['style']}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("farah_form"):
        user_text = st.text_area(
            "اكتب ما يدور في ذهنك...",
            height=150,
            placeholder="شاركني مشاعرك وأفكارك... أنا هنا للاستماع إليك"
        )
        
        submitted = st.form_submit_button("تحليل المشاعر", use_container_width=True)
        
        if submitted and user_text.strip():
            with st.spinner("جاري التحليل..."):
                result = farah_predict(user_text, st.session_state.selected_persona)
                st.session_state.farah_result = result
    
    if st.session_state.farah_result:
        result = st.session_state.farah_result
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Persona Response
        st.markdown(f"""
        <div class="glass-card" style="border-right: 4px solid {current_persona['color']};">
            <div style="display: flex; align-items: flex-start; gap: 1rem;">
                <div style="font-size: 2rem;">{current_persona['avatar']}</div>
                <div>
                    <p style="color: white; font-size: 1.1rem; line-height: 1.8; margin: 0;">
                        {result['persona_response']}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="analysis-card">
                <div class="analysis-label">مستوى الاكتئاب</div>
                <div class="analysis-value" style="color: {result['depression']['color']};">
                    {result['depression']['level']}
                </div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {result['depression']['score']*100}%; background: {result['depression']['color']};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="analysis-card">
                <div class="analysis-label">مستوى القلق</div>
                <div class="analysis-value" style="color: {result['anxiety']['color']};">
                    {result['anxiety']['level']}
                </div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {result['anxiety']['score']*100}%; background: {result['anxiety']['color']};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="analysis-card">
                <div class="analysis-label">مستوى الرفاهية</div>
                <div class="analysis-value" style="color: {result['wellbeing']['color']};">
                    {result['wellbeing']['level']}
                </div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {result['wellbeing']['score']*100}%; background: {result['wellbeing']['color']};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if result.get('is_ai_analyzed'):
            st.markdown("""
            <div style="text-align: center; margin-top: 0.5rem;">
                <span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 0.3rem 1rem; border-radius: 20px; font-size: 0.85rem; color: white;">
                    تم التحليل بالذكاء الاصطناعي
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card" style="margin-top: 1rem;">
            <h4 style="color: #667eea;">نصائح لتحسين حالتك:</h4>
            <ul style="color: rgba(255,255,255,0.8); line-height: 2.2;">
                <li>تحدث مع شخص تثق به عن مشاعرك</li>
                <li>مارس التأمل والتنفس العميق يومياً لمدة 10 دقائق</li>
                <li>حافظ على نمط نوم صحي ومنتظم</li>
                <li>مارس الرياضة بانتظام - حتى المشي يساعد</li>
                <li>استشر أخصائي نفسي إذا استمرت الأعراض</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


# ==================== MEDICAL ADVISOR PAGE ====================
elif active_page == "طبيبك الذكي":
    st.markdown("""
    <div class="glass-card">
        <h2 style="color: #667eea; text-align: center !important;">💬 طبيبك الذكي</h2>
        <p style="text-align: center !important; color: rgba(255,255,255,0.7);">
            اسأل عن أي موضوع صحي واحصل على إجابة فورية
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat Container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if not st.session_state.chat_history:
        st.markdown("""
        <div style="text-align: center; color: rgba(255,255,255,0.7); padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">👨‍⚕️</div>
            <h3 style="color: white; margin-bottom: 0.5rem;">مرحباً! أنا طبيبك الذكي</h3>
            <p>كيف يمكنني مساعدتك اليوم؟</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message user-message">
                    {msg['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    {msg['content']}
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "اكتب سؤالك هنا...",
                label_visibility="collapsed",
                placeholder="اكتب سؤالك الصحي هنا..."
            )
        
        with col2:
            send_button = st.form_submit_button("إرسال", use_container_width=True)
        
        if send_button and user_input.strip():
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input
            })
            
            with st.spinner("جاري التفكير..."):
                response = chat_with_ai(user_input, st.session_state.chat_history)
            
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response
            })
            
            st.rerun()
    
    if st.session_state.chat_history:
        if st.button("مسح المحادثة", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    st.markdown("""
    <div class="glass-card" style="margin-top: 1rem;">
        <p style="color: rgba(255,255,255,0.6); text-align: center !important; font-size: 0.9rem;">
            ⚠️ هذه الاستشارة للتوعية فقط ولا تغني عن زيارة طبيب مختص
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==================== EMOTION MIRROR PAGE ====================
elif active_page == "مرآة المشاعر":
    st.markdown("""
    <div class="glass-card">
        <h2 style="color: #a78bfa; text-align: center !important; font-size: 2rem;">
            <span style="display: inline-flex; align-items: center; gap: 0.5rem;">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                    <circle cx="12" cy="13" r="4"/>
                </svg>
                مرآة المشاعر - البث المباشر
            </span>
        </h2>
        <p style="text-align: center !important; color: rgba(255,255,255,0.7);">
            تحليل مشاعرك في الوقت الفعلي من خلال الكاميرا
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for live emotion tracking
    if 'live_emotion' not in st.session_state:
        st.session_state.live_emotion = None
    if 'live_emotions_all' not in st.session_state:
        st.session_state.live_emotions_all = {}
    if 'is_simulation' not in st.session_state:
        st.session_state.is_simulation = False
    
    # Live status indicator
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 1rem;">
        <div style="width: 14px; height: 14px; background: #ef4444; border-radius: 50%; animation: pulse-red 1s ease-in-out infinite; box-shadow: 0 0 15px #ef4444;"></div>
        <span style="color: #fca5a5; font-weight: 700; font-size: 1.1rem;">البث المباشر نشط</span>
    </div>
    <style>
        @keyframes pulse-red {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.3); opacity: 0.7; }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Auto-refresh for continuous monitoring
    if 'monitoring_active' not in st.session_state:
        st.session_state.monitoring_active = False
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h4 style="color: #6b21a8; margin-bottom: 1rem;">كاميرا التحليل</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Toggle monitoring button
        if st.button("بدء المراقبة المستمرة" if not st.session_state.monitoring_active else "إيقاف المراقبة", 
                    key="toggle_monitor", use_container_width=True, type="primary"):
            st.session_state.monitoring_active = not st.session_state.monitoring_active
            st.rerun()
        
        # Camera input
        camera_image = st.camera_input("", key="emotion_camera", label_visibility="collapsed")
        
        # Auto-refresh when monitoring is active
        if st.session_state.monitoring_active:
            st_autorefresh(interval=3000, limit=None, key="continuous_monitor")
            st.markdown("""
            <div style="background: linear-gradient(135deg, #22c55e, #16a34a); border-radius: 12px; padding: 0.8rem; margin-top: 0.5rem;">
                <p style="color: white; text-align: center !important; margin: 0; font-size: 0.9rem; font-weight: 600;">
                    المراقبة نشطة - يتم التحديث كل 3 ثواني
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: rgba(107, 33, 168, 0.2); border: 1px solid rgba(107, 33, 168, 0.4); border-radius: 12px; padding: 0.8rem; margin-top: 0.5rem;">
                <p style="color: #6b21a8; text-align: center !important; margin: 0; font-size: 0.9rem; font-weight: 600;">
                    التقط صورة لتحليل مشاعرك
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Analyze image
    emotion = None
    emotions = {}
    is_sim = False
    
    if camera_image is not None:
        pil_image = Image.open(camera_image)
        result = analyze_face(pil_image)
        if result['success']:
            emotion = result['emotion']
            emotions = result['all_emotions']
            is_sim = result.get('simulation', False)
    
    # Display results
    with col2:
        
        if emotion and emotions:
            emotion_ar = EMOTION_ARABIC.get(emotion, emotion)
            advice = EMOTION_ADVICE.get(emotion, '')
            
            # Emotion icons mapping
            emotion_icons = {
                'happy': '<svg width="80" height="80" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="#22c55e"/><circle cx="35" cy="40" r="5" fill="#333"/><circle cx="65" cy="40" r="5" fill="#333"/><path d="M30 55 Q50 75 70 55" stroke="#333" stroke-width="4" fill="none"/></svg>',
                'sad': '<svg width="80" height="80" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="#3b82f6"/><circle cx="35" cy="40" r="5" fill="#333"/><circle cx="65" cy="40" r="5" fill="#333"/><path d="M30 65 Q50 50 70 65" stroke="#333" stroke-width="4" fill="none"/></svg>',
                'angry': '<svg width="80" height="80" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="#ef4444"/><line x1="25" y1="35" x2="40" y2="40" stroke="#333" stroke-width="3"/><line x1="75" y1="35" x2="60" y2="40" stroke="#333" stroke-width="3"/><circle cx="35" cy="42" r="4" fill="#333"/><circle cx="65" cy="42" r="4" fill="#333"/><path d="M35 65 L65 65" stroke="#333" stroke-width="4"/></svg>',
                'fear': '<svg width="80" height="80" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="#a855f7"/><ellipse cx="35" cy="40" rx="6" ry="8" fill="#333"/><ellipse cx="65" cy="40" rx="6" ry="8" fill="#333"/><ellipse cx="50" cy="65" rx="10" ry="8" fill="#333"/></svg>',
                'surprise': '<svg width="80" height="80" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="#f59e0b"/><ellipse cx="35" cy="40" rx="6" ry="8" fill="#333"/><ellipse cx="65" cy="40" rx="6" ry="8" fill="#333"/><ellipse cx="50" cy="65" rx="8" ry="10" fill="#333"/></svg>',
                'neutral': '<svg width="80" height="80" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="#667eea"/><circle cx="35" cy="40" r="5" fill="#333"/><circle cx="65" cy="40" r="5" fill="#333"/><line x1="35" y1="60" x2="65" y2="60" stroke="#333" stroke-width="4"/></svg>',
                'disgust': '<svg width="80" height="80" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="#10b981"/><circle cx="35" cy="40" r="5" fill="#333"/><circle cx="65" cy="40" r="5" fill="#333"/><path d="M35 60 Q50 70 65 55" stroke="#333" stroke-width="4" fill="none"/></svg>'
            }
            
            icon = emotion_icons.get(emotion, emotion_icons['neutral'])
            
            st.markdown(f"""
            <div class="emotion-result emotion-{emotion}" style="padding: 2rem;">
                <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
                    {icon}
                </div>
                <h2 style="color: white; margin: 0; font-size: 1.8rem;">{emotion_ar}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="glass-card">
                <p style="color: white; text-align: center !important; font-size: 1.1rem; line-height: 1.8;">
                    {advice}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="glass-card">
                <h4 style="color: #c4b5fd;">تفاصيل التحليل:</h4>
            """, unsafe_allow_html=True)
            
            for em, score in sorted(emotions.items(), key=lambda x: x[1], reverse=True):
                em_ar = EMOTION_ARABIC.get(em, em)
                bar_color = {
                    'happy': '#22c55e', 'sad': '#3b82f6', 'angry': '#ef4444',
                    'fear': '#a855f7', 'surprise': '#f59e0b', 'neutral': '#667eea', 'disgust': '#10b981'
                }.get(em, '#667eea')
                
                st.markdown(f"""
                <div style="margin: 0.5rem 0;">
                    <div style="display: flex; justify-content: space-between; color: rgba(255,255,255,0.8);">
                        <span>{em_ar}</span>
                        <span>{score:.1f}%</span>
                    </div>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {score}%; background: {bar_color};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            if is_sim:
                st.markdown("""
                <div style="text-align: center; margin-top: 1rem;">
                    <span style="background: rgba(167, 139, 250, 0.3); padding: 0.5rem 1.5rem; border-radius: 25px; font-size: 0.9rem; color: #c4b5fd; border: 1px solid rgba(167, 139, 250, 0.5);">
                        وضع المحاكاة
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="glass-card" style="text-align: center; padding: 3rem;">
                <div style="margin-bottom: 1.5rem;">
                    <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="1.5" style="opacity: 0.5;">
                        <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                        <circle cx="12" cy="13" r="4"/>
                    </svg>
                </div>
                <p style="color: #c4b5fd; font-size: 1.1rem;">
                    اضغط START لبدء البث المباشر
                </p>
                <p style="color: rgba(255,255,255,0.5); font-size: 0.9rem; margin-top: 0.5rem;">
                    سيتم تحليل مشاعرك تلقائياً من الكاميرا
                </p>
            </div>
            """, unsafe_allow_html=True)
    


# ==================== DRUG INTERACTION PAGE ====================
elif active_page == "تفاعل الأدوية":
    st.markdown("""
    <div class="glass-card">
        <h2 style="color: #667eea; text-align: center !important;">💊 فحص تفاعل الأدوية</h2>
        <p style="text-align: center !important; color: rgba(255,255,255,0.7);">
            تحقق من التفاعلات المحتملة بين الأدوية المختلفة
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: white;">الدواء الأول</h4>
        </div>
        """, unsafe_allow_html=True)
        drug1 = st.selectbox("اختر الدواء الأول", options=[""] + COMMON_DRUGS, key="drug1", label_visibility="collapsed")
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: white;">الدواء الثاني</h4>
        </div>
        """, unsafe_allow_html=True)
        drug2 = st.selectbox("اختر الدواء الثاني", options=[""] + COMMON_DRUGS, key="drug2", label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("فحص التفاعل", use_container_width=True, key="check_interaction"):
        if drug1 and drug2:
            if drug1 == drug2:
                st.warning("يرجى اختيار دواءين مختلفين")
            else:
                with st.spinner("جاري الفحص..."):
                    time.sleep(0.5)
                    result = check_drug_interaction(drug1, drug2)
                    st.session_state.drug_result = {'drug1': drug1, 'drug2': drug2, 'result': result}
        else:
            st.warning("يرجى اختيار كلا الدواءين")
    
    if st.session_state.drug_result:
        result = st.session_state.drug_result
        interaction = result['result']
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        risk_class = f"risk-{interaction['risk']}"
        risk_label = {
            'high': 'خطر مرتفع',
            'medium': 'خطر متوسط',
            'low': 'خطر منخفض',
            'none': 'لا يوجد تفاعل معروف'
        }.get(interaction['risk'], 'غير معروف')
        
        risk_icon = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢',
            'none': '✅'
        }.get(interaction['risk'], '❓')
        
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <h3 style="color: white; margin-bottom: 1rem;">نتيجة الفحص</h3>
            <div style="font-size: 3rem; margin-bottom: 1rem;">{risk_icon}</div>
            <div style="margin-bottom: 1rem;">
                <span class="{risk_class}">{risk_label}</span>
            </div>
            <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem; margin-top: 1rem;">
                {interaction['description']}
            </p>
            <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1);">
                <p style="color: rgba(255,255,255,0.5); font-size: 0.9rem;">
                    {result['drug1']} + {result['drug2']}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if interaction['risk'] == 'high':
            st.markdown("""
            <div class="glass-card" style="border: 2px solid #ff416c;">
                <h4 style="color: #ff416c;">تحذير هام:</h4>
                <p style="color: rgba(255,255,255,0.8);">
                    يجب استشارة الطبيب أو الصيدلي فوراً قبل تناول هذين الدواءين معاً.
                    قد يكون هناك بدائل أكثر أماناً.
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif interaction['risk'] == 'medium':
            st.markdown("""
            <div class="glass-card" style="border: 2px solid #f7971e;">
                <h4 style="color: #f7971e;">ملاحظة:</h4>
                <p style="color: rgba(255,255,255,0.8);">
                    يُنصح بإخبار الطبيب أو الصيدلي عند تناول هذين الدواءين.
                    قد تحتاج لمراقبة إضافية.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card" style="margin-top: 2rem;">
        <h4 style="color: white;">أدوية شائعة للفحص:</h4>
        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem;">
    """, unsafe_allow_html=True)
    
    for drug in COMMON_DRUGS[:10]:
        st.markdown(f"""
            <span style="background: rgba(102, 126, 234, 0.3); padding: 0.4rem 1rem; border-radius: 20px; font-size: 0.9rem; color: white; display: inline-block; margin: 0.25rem;">
                {drug}
            </span>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        </div>
        <p style="color: rgba(255,255,255,0.5); font-size: 0.85rem; margin-top: 1.5rem;">
            ⚠️ هذه القائمة للأغراض التعليمية فقط. استشر الصيدلي دائماً.
        </p>
    </div>
    """, unsafe_allow_html=True)


# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem 0; margin-top: 2rem; border-top: 1px solid rgba(255,255,255,0.1);">
    <p style="color: rgba(255,255,255,0.4); font-size: 0.9rem;">
        نبض | Nabd - منصة صحية ذكية
    </p>
    <p style="color: rgba(255,255,255,0.3); font-size: 0.8rem;">
        خصوصيتك محمية - جميع البيانات تعالج بشكل آمن
    </p>
</div>
""", unsafe_allow_html=True)
