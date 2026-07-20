import pandas as pd
import streamlit as st
import urllib.parse
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# --- WEB UI CONFIG ---
st.set_page_config(page_title="AI Cyber Shield Classifier", page_icon="🛡️", layout="centered")

# --- GENERATE HIGH-QUALITY BRIGHT MATRIX RAIN SVG ---
svg_cols = []
random.seed(101)

# Columns aur numbers ki density aur brightness badha di gayi hai
for col in range(16):
    x = 10 + col * 20
    for y in range(15, 600, 30):
        char = random.choice(['0', '1'])
        # Opacity badha di gayi hai taaki bright aur clear dikhe (0.4 se 1.0 ke beech)
        opacity = round(random.uniform(0.4, 1.0), 2)
        weight = "bold" if opacity > 0.7 else "normal"
        # Font size 13 se 15 kar diya gaya hai
        svg_cols.append(f"<text x='{x}' y='{y}' fill='%2300ff66' opacity='{opacity}' font-family='monospace' font-size='15' font-weight='{weight}'>{char}</text>")

svg_content = f"""<svg xmlns='http://www.w3.org/2000/svg' width='300' height='600' viewBox='0 0 300 600'>
    {"".join(svg_cols)}
</svg>"""

encoded_svg = urllib.parse.quote(svg_content)

# --- GLOBAL STYLING & CORE CSS ---
global_css = f"""
<style>
    /* 1. Global background */
    html {{
        background-color: #02040a !important;
        background-image: url("data:image/svg+xml;utf8,{encoded_svg}") !important;
        background-repeat: repeat !important;
        background-size: 300px 600px !important;
        animation: matrixScroll 12s linear infinite !important; /* Speed thodi fast ki hai */
    }}

    /* 2. Transparent wrappers */
    body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background: transparent !important;
    }}

    /* 3. Main Glassmorphic Box - Thoda transparent kiya taaki piche ka rain dikhe */
    [data-testid="stAppViewBlockContainer"] {{
        background: rgba(10, 15, 30, 0.82) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        border: 2px solid rgba(0, 255, 102, 0.6) !important;
        border-radius: 16px !important;
        padding: 35px !important;
        box-shadow: 0 0 40px rgba(0, 255, 102, 0.15) !important;
        max-width: 650px !important;
        margin: 60px auto !important;
    }}

    /* 4. Text Fonts */
    h1 {{
        color: #00ff66 !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
        text-shadow: 0 0 10px rgba(0, 255, 102, 0.6) !important;
        text-align: center;
        margin-top: 10px !important;
    }}

    label, p, span, div {{
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif !important;
    }}

    /* 5. Custom Input Area Box */
    .stTextArea textarea {{
        background-color: rgba(5, 10, 25, 0.9) !important;
        color: #00ff66 !important;
        border: 1px solid rgba(0, 255, 102, 0.6) !important;
        font-family: 'Courier New', monospace !important;
        font-size: 16px !important;
        border-radius: 8px !important;
    }}

    .stTextArea textarea:focus {{
        border-color: #00ff66 !important;
        box-shadow: 0 0 15px rgba(0, 255, 102, 0.5) !important;
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
        box-shadow: 0 4px 15px rgba(0, 255, 102, 0.4) !important;
    }}

    div.stButton > button:hover {{
        background-color: #ffffff !important;
        box-shadow: 0 0 25px rgba(0, 255, 102, 0.7) !important;
    }}

    /* 7. Keyframe animation */
    @keyframes matrixScroll {{
        0% {{ background-position: 0 0; }}
        100% {{ background-position: 0 600px; }}
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


# --- SPEECH SYNTHESIS ENGINE ---
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
            background: rgba(0, 255, 102, 0.15);
            border: 1px solid #00ff66;
            color: #00ff66;
            padding: 6px 16px;
            border-radius: 50px;
            font-size: 13px;
            font-family: monospace;
            letter-spacing: 1px;
            font-weight: bold;
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

        st.markdown("<hr style='border: 1px solid rgba(0, 255, 102, 0.25);'>", unsafe_allow_html=True)

        if is_spam:
            st.markdown(
                """
                <div style="
                    background: rgba(33, 7, 12, 0.9) !important;
                    border: 2px solid #ff003c !important;
                    border-radius: 8px !important;
                    padding: 15px !important;
                    text-align: center !important;
                    box-shadow: 0 0 20px rgba(255, 0, 60, 0.4) !important;
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
                    background: rgba(4, 31, 16, 0.9) !important;
                    border: 2px solid #00ff66 !important;
                    border-radius: 8px !important;
                    padding: 15px !important;
                    text-align: center !important;
                    box-shadow: 0 0 20px rgba(0, 255, 102, 0.4) !important;
                ">
                    <h3 style="color: #33ff99 !important; font-family: monospace; font-weight: bold; margin: 0; font-size: 18px;">✅ THREAT SCAN: SECURE (HAM)</h3>
                </div>
                """, 
                unsafe_allow_html=True
            )
            play_voice_alert("यह संदेश पूरी तरह सुरक्षित है।")
