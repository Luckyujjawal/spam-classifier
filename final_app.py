import pandas as pd
import streamlit as st
import base64
import random
import io
from gtts import gTTS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# --- WEB UI CONFIG ---
st.set_page_config(page_title="AI Cyber Shield Classifier", page_icon="🛡️", layout="centered")

# --- LIGHTWEIGHT BRIGHT NEON GREEN MATRIX SVG ---
svg_cols = []
random.seed(101)

for col in range(20):
    x = col * 22 + 10
    for row in range(18):
        y = row * 40 + random.randint(0, 15)
        char = random.choice(['0', '1'])
        
        rand_val = random.random()
        if rand_val > 0.7:
            color = "%2300ff66"
            opacity = 1.0
            font_size = 18
            font_weight = "900"
        else:
            color = "%2300cc52"
            opacity = 0.8
            font_size = 14
            font_weight = "bold"

        svg_cols.append(
            f"<text x='{x}' y='{y}' fill='{color}' opacity='{opacity}' "
            f"font-family='monospace' font-size='{font_size}' font-weight='{font_weight}'>{char}</text>"
        )

svg_content = f"""<svg xmlns='http://www.w3.org/2000/svg' width='450' height='720' viewBox='0 0 450 720'>
    <rect width='100%25' height='100%25' fill='%23121624'/>
    {"".join(svg_cols)}
</svg>"""

encoded_svg = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
bg_image_url = f"data:image/svg+xml;base64,{encoded_svg}"

# --- CSS STYLING ---
global_css = f"""
<style>
    [data-testid="stAppViewContainer"] {{
        background-color: #121624 !important;
        background-image: url("{bg_image_url}") !important;
        background-repeat: repeat !important;
        background-size: 450px 720px !important;
        animation: matrixScroll 15s linear infinite !important;
    }}

    section.main, .stApp, [data-testid="stHeader"], [data-testid="stSidebar"] {{
        background: transparent !important;
    }}

    [data-testid="stAppViewBlockContainer"] {{
        background-color: #080b11 !important;
        border: 2px solid #00ff66 !important;
        border-radius: 16px !important;
        box-shadow: 0 0 30px rgba(0, 255, 102, 0.3) !important;
        max-width: 600px !important;
        margin: 40px auto !important;
        padding: 35px !important;
    }}

    h1 {{
        color: #00ff66 !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
        text-shadow: 0 0 10px rgba(0, 255, 102, 0.6) !important;
        text-align: center;
    }}

    label, p, span, div {{
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif !important;
    }}

    .stTextArea textarea {{
        background-color: #0c0f17 !important;
        color: #00ff66 !important;
        border: 1px solid rgba(0, 255, 102, 0.5) !important;
        font-family: 'Courier New', monospace !important;
        font-size: 16px !important;
        border-radius: 8px !important;
    }}

    div.stButton > button {{
        background-color: #00ff66 !important;
        color: #121624 !important;
        font-weight: bold !important;
        font-family: monospace !important;
        border: none !important;
        width: 100% !important;
        padding: 12px 20px !important;
        border-radius: 8px !important;
        letter-spacing: 2px !important;
        box-shadow: 0 4px 15px rgba(0, 255, 102, 0.4) !important;
    }}

    @keyframes matrixScroll {{
        0% {{ background-position: 0 0; }}
        100% {{ background-position: 0 720px; }}
    }}
</style>
"""
st.markdown(global_css, unsafe_allow_html=True)

# --- CACHED MODEL TRAINING ---
@st.cache_resource
def load_and_train_model():
    try:
        df = pd.read_csv("spam (1).csv", encoding="latin-1")
        df = df.dropna(how="any", axis=1)
        df.columns = ["label", "message"]
    except Exception as e:
        return None, None, 0.0

    df["label_num"] = df["label"].map({"ham": 0, "spam": 1})
    X = df["message"]
    y = df["label_num"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    cv = CountVectorizer()
    X_train_vectorized = cv.fit_transform(X_train)
    X_test_vectorized = cv.transform(X_test)

    model = MultinomialNB()
    model.fit(X_train_vectorized, y_train)
    accuracy = model.score(X_test_vectorized, y_test)
    
    return model, cv, accuracy

model, cv, accuracy = load_and_train_model()

if model is None:
    st.error("Dataset load nahi ho paya!")
    st.stop()

# --- NATIVE MP3 AUDIO PLAYER (Instant Playback) ---
def play_voice_alert(text):
    tts = gTTS(text=text, lang='hi')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    st.audio(fp, format="audio/mp3", autoplay=True)

# --- UI LAYOUT ---
st.title("🛡️ CYBER SPAM SHIELD")

st.markdown(
    f"""
    <div style="text-align: center; margin-bottom: 25px;">
        <span style="
            background: rgba(0, 255, 102, 0.1);
            border: 1px solid #00ff66;
            color: #00ff66;
            padding: 6px 16px;
            border-radius: 50px;
            font-size: 13px;
            font-family: monospace;
            letter-spacing: 1px;
        ">
            SYSTEM ACTIVE | MODEL ACCURACY: {accuracy*100:.2f}%
        </span>
    </div>
    """, 
    unsafe_allow_html=True
)

user_input = st.text_area("Hacker, enter SMS or Email message to scan:", placeholder="Type or paste your message here...")

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

if st.button("RUN SCANNING"):
    if user_input.strip() == "":
        st.warning("Pehle scan karne ke liye text enter karein!")
    else:
        spam_keywords = ["won", "claim", "clam", "lottery", "prize", "crore", "lakh", "selected", "free gift", "rewarded"]
        is_spam_keyword = any(word in user_input.lower() for word in spam_keywords)

        safe_keywords = ["debited", "credited", "refno", "upi user", "a/c", "sbi"]
        is_bank_msg = any(word in user_input.lower() for word in safe_keywords)

        vect = cv.transform([user_input])
        prediction = model.predict(vect)
        
        if is_bank_msg:
            is_spam = False
        elif is_spam_keyword:
            is_spam = True
        elif prediction[0] == 1:
            is_spam = True
        else:
            is_spam = False

        st.markdown("<hr style='border: 1px solid rgba(0, 255, 102, 0.15);'>", unsafe_allow_html=True)

        if is_spam:
            play_voice_alert("सावधान! यह एक फ्रॉड या स्पैम संदेश हो सकता है।")
            st.markdown(
                """
                <div style="
                    background: #21070c !important;
                    border: 2px solid #ff003c !important;
                    border-radius: 8px !important;
                    padding: 15px !important;
                    text-align: center !important;
                    box-shadow: 0 0 15px rgba(255, 0, 60, 0.25) !important;
                ">
                    <h3 style="color: #ff3366 !important; font-family: monospace; font-weight: bold; margin: 0; font-size: 18px;">🚨 THREAT DETECTED: SPAM</h3>
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            play_voice_alert("यह संदेश पूरी तरह सुरक्षित है।")
            st.markdown(
                """
                <div style="
                    background: #041f10 !important;
                    border: 2px solid #00ff66 !important;
                    border-radius: 8px !important;
                    padding: 15px !important;
                    text-align: center !important;
                    box-shadow: 0 0 15px rgba(0, 255, 102, 0.2) !important;
                ">
                    <h3 style="color: #33ff99 !important; font-family: monospace; font-weight: bold; margin: 0; font-size: 18px;">✅ THREAT SCAN: SECURE (HAM)</h3>
                </div>
                """, 
                unsafe_allow_html=True
            )
