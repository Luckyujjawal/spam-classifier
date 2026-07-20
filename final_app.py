import pandas as pd
import streamlit as st
import urllib.parse
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# --- WEB UI CONFIG ---
st.set_page_config(page_title="AI Cyber Shield Classifier", page_icon="🛡️", layout="centered")

# --- GENERATE HIGH-QUALITY MATRIX RAIN SVG ---
# Hum programmatically ek seamless matrix falling rain ka pattern generate kar rahe hain.
svg_cols = []
random.seed(101)  # Pattern ko hamesha consistent rakhne ke liye seed set kiya hai

for col in range(12):
    x = 15 + col * 25
    for y in range(30, 600, 45):
        char = random.choice(['0', '1'])
        opacity = round(random.uniform(0.15, 0.85), 2)
        weight = "bold" if opacity > 0.6 else "normal"
        svg_cols.append(f"<text x='{x}' y='{y}' fill='%2300ff66' opacity='{opacity}' font-family='monospace' font-size='13' font-weight='{weight}'>{char}</text>")

svg_content = f"""<svg xmlns='http://www.w3.org/2000/svg' width='300' height='600' viewBox='0 0 300 600'>
    {"".join(svg_cols)}
</svg>"""

# URL Encoding for CSS integration
encoded_svg = urllib.parse.quote(svg_content)

# --- GLOBAL STYLING & CORE CSS ---
# Pure CSS animation jo 100% background me smoothly binary rain chalayegi aur text saaf dikhayegi
global_css = f"""
<style>
    /* 1. Global background on root html tag to ensure it covers entire screen */
    html {{
        background-color: #030712 !important;
        background-image: url("data:image/svg+xml;utf8,{encoded_svg}") !important;
        background-repeat: repeat !important;
        background-size: 300px 600px !important;
        animation: matrixScroll 18s linear infinite !important;
    }}

    /* 2. Make all intermediate containers transparent so background shines through */
    body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background: transparent !important;
    }}

    /* 3. Style the main Streamlit container card (No empty box issue anymore!) */
    [data-testid="stAppViewBlockContainer"] {{
        background: rgba(10, 15, 30, 0.96) !important;
        border: 2px solid #00ff66 !important;
        border-radius: 16px !important;
        padding: 35px !important;
        box-shadow: 0 0 30px rgba(0, 255, 102, 0.2) !important;
        max-width: 650px !important;
        margin: 60px auto !important;
    }}

    /* 4. Text and Fonts improvements for High-Contrast visibility */
    h1 {{
        color: #00ff66 !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
        text-shadow: 0 0 8px rgba(0, 255, 102, 0.5) !important;
        text-align: center;
        margin-top: 10px !important;
    }}

    label, p, span, div {{
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif !important;
    }}

    /* 5. Custom Input Area Box Styling */
    .stTextArea textarea {{
        background-color: #0d1527 !important;
        color: #00ff66 !important;
        border: 1px solid rgba(0, 255, 102, 0.4) !important;
        font-family: 'Courier New', monospace !important;
        font-size: 16px !important;
        border-radius: 8px !important;
    }}

    .stTextArea textarea:focus {{
        border-color: #00ff66 !important;
        box-shadow: 0 0 12px rgba(0, 255, 102, 0.4) !important;
    }}

    /* 6. Scan Button design */
    div.stButton > button {{
        background-color: #00ff66 !important;
        color: #060814 !important;
        font-weight: bold !important;
        font-family: monospace !important;
        border: none !important;
        width: 100% !important;
        padding: 12px 20px !important;
        border-radius: 8px !important;
        letter-spacing: 2px !important;
        box-shadow: 0 4px 15px rgba(0, 255, 102, 0.3) !important;
    }}

    div.stButton > button:hover {{
        background-color: #ffffff !important;
        box-shadow: 0 0 25px rgba(0, 255, 102, 0.6) !important;
    }}

    /* 7. Keyframe animation for binary rain */
    @keyframes matrixScroll {{
        0% {{
            background-position: 0 0;
        }}
        100% {{
            background-position: 0 600px;
        }}
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

# Load machine learning files
model, cv, accuracy = load_and_train_model()

if model is None:
    st.error("Dataset load nahi ho paya!")
    st.stop()


# --- SPEECH SYNTHESIS ENGINE ---
# Audio works seamlessly on button trigger without being blocked by Chrome
def play_voice_alert(text):
    iframe_html = f"""
    <iframe srcdoc="
        <script>
            function speak() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    var msg = new SpeechSynthesisUtterance('{text}');
                    msg.lang = 'hi-IN';
                    msg.pitch = 1.0;
                    msg.rate = 1.0;
                    window.speechSynthesis.speak(msg);
                }}
            }}
            setTimeout(speak, 10);
        </script>
    " allow="autoplay" style="display:none; width:0; height:0; border:none; visibility:hidden;"></iframe>
    """
    st.markdown(iframe_html, unsafe_allow_html=True)


# --- MAIN INTERFACE CONTENT ---
st.title("🛡️ CYBER SPAM SHIELD")

# Accuracy badge
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

# User input text area
user_input = st.text_area("Hacker, enter SMS or Email message to scan:", placeholder="Type or paste your message here...")

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# Scan execution
if st.button("RUN SCANNING"):
    if user_input.strip() == "":
        st.warning("Pehle scan karne ke liye text enter karein!")
    else:
        # Custom Bypass Rules
        spam_keywords = ["won", "claim", "clam", "lottery", "prize", "crore", "lakh", "selected", "free gift", "rewarded"]
        is_spam_keyword = any(word in user_input.lower() for word in spam_keywords)

        safe_keywords = ["debited", "credited", "refno", "upi user", "a/c", "sbi"]
        is_bank_msg = any(word in user_input.lower() for word in safe_keywords)

        # ML prediction
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

        # Output blocks styled cleanly (High Contrast & 100% Readable)
        if is_spam:
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
            play_voice_alert("सावधान! यह एक फ्रॉड या स्पैम संदेश हो सकता है।")
        else:
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
            play_voice_alert("यह संदेश पूरी तरह सुरक्षित है।")
