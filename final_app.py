import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# --- WEB UI CONFIG ---
st.set_page_config(page_title="AI Cyber Shield Classifier", page_icon="🛡️", layout="centered")

# --- PRO FOOTER & TRANSPARENT MATRIX CSS + JS ---
matrix_bg_html = """
<canvas id="matrixCanvas"></canvas>
<style>
    /* Full screen canvas fixed in background */
    #matrixCanvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -9999;
        background-color: #030712; /* Dark deep background */
    }
    
    /* Make Streamlit container transparent to see the canvas */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMainTemplate"] {
        background: transparent !important;
    }
    
    /* Highly readable solid dark box with clean border */
    .main-box {
        background: rgba(15, 23, 42, 0.96) !important; /* solid slate to block moving numbers behind text */
        border: 2px solid #10b981 !important; /* Elegant green border */
        border-radius: 12px !important;
        padding: 30px !important;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.15) !important;
        margin-top: 20px;
    }
    
    /* Clean and High-Contrast Typography */
    h1 {
        color: #10b981 !important; /* Emerald green without annoying glow */
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
        text-align: center;
        font-size: 32px !important;
        margin-bottom: 5px !important;
    }
    
    /* Pure readable text colors (No blinding glows) */
    p, label, span, .stMarkdown {
        color: #f1f5f9 !important; /* Pure clean light-white for extreme readability */
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 16px;
    }
    
    /* User text area styling */
    .stTextArea textarea {
        background-color: #0f172a !important; /* Slate Dark */
        color: #f8fafc !important; /* White text for typing */
        border: 1px solid #334155 !important;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 16px !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.25) !important;
    }
    
    /* Clean green scanning button */
    div.stButton > button {
        background-color: #10b981 !important;
        color: #0f172a !important;
        font-weight: bold !important;
        border: none !important;
        width: 100% !important;
        padding: 12px 20px !important;
        border-radius: 6px !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        transition: all 0.2s ease !important;
    }
    
    div.stButton > button:hover {
        background-color: #34d399 !important; /* Lighter emerald on hover */
        transform: translateY(-1px) !important;
    }
</style>

<script>
    // Matrix Rain Script with custom Delay check
    setTimeout(() => {
        const canvas = document.getElementById('matrixCanvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize);
        resize();

        const alphabet = '01';
        const fontSize = 16;
        const columns = canvas.width / fontSize;

        const rainDrops = [];
        for (let x = 0; x < columns; x++) {
            rainDrops[x] = Math.random() * -100;
        }

        function drawMatrix() {
            ctx.fillStyle = 'rgba(3, 7, 18, 0.08)'; // Smooth fading trail
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = 'rgba(16, 185, 129, 0.35)'; // Highly transparent green binary numbers
            ctx.font = fontSize + 'px monospace';

            for (let i = 0; i < rainDrops.length; i++) {
                const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
                ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);

                if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.985) {
                    rainDrops[i] = 0;
                }
                rainDrops[i] += 0.8;
            }
        }

        if (window.matrixInterval) clearInterval(window.matrixInterval);
        window.matrixInterval = setInterval(drawMatrix, 33);
    }, 100);
</script>
"""
st.markdown(matrix_bg_html, unsafe_allow_html=True)


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
    " allow="autoplay" style="display:none; width:0; height:0; border:none;"></iframe>
    """
    st.markdown(iframe_html, unsafe_allow_html=True)


# --- DASHBOARD LAYOUT & CARD ---
st.markdown('<div class="main-box">', unsafe_allow_html=True)

st.title("🛡️ CYBER SPAM SHIELD")

# Elegant accuracy badge
st.markdown(
    f"""
    <div style="text-align: center; margin-bottom: 25px;">
        <span style="
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid #10b981;
            color: #10b981;
            padding: 5px 15px;
            border-radius: 50px;
            font-size: 13px;
            font-family: monospace;
            font-weight: bold;
        ">
            SYSTEM SECURE | MODEL ACCURACY: {accuracy*100:.2f}%
        </span>
    </div>
    """, 
    unsafe_allow_html=True
)

# User input text area
user_input = st.text_area("Hacker, enter SMS or Email message to scan:", placeholder="Type or paste your message here...")

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

if st.button("RUN SCANNING"):
    if user_input.strip() == "":
        st.warning("Pehle scan karne ke liye text enter karein!")
    else:
        # Custom Bypass Rules
        spam_keywords = ["won", "claim", "clam", "lottery", "prize", "crore", "lakh", "selected", "free gift", "rewarded"]
        is_spam_keyword = any(word in user_input.lower() for word in spam_keywords)

        safe_keywords = ["debited", "credited", "refno", "upi user", "a/c", "sbi"]
        is_bank_msg = any(word in user_input.lower() for word in safe_keywords)

        # Vectorization & Prediction
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

        st.markdown("<hr style='border: 1px solid rgba(16, 185, 129, 0.2); margin: 20px 0;'>", unsafe_allow_html=True)

        if is_spam:
            st.markdown(
                """
                <div style="
                    background: rgba(239, 68, 68, 0.15) !important;
                    border: 2px solid #ef4444 !important;
                    border-radius: 8px !important;
                    padding: 15px !important;
                    text-align: center !important;
                ">
                    <h3 style="color: #ef4444 !important; font-family: monospace; font-weight: bold; margin: 0; font-size: 20px;">🚨 THREAT DETECTED: SPAM</h3>
                </div>
                """, 
                unsafe_allow_html=True
            )
            play_voice_alert("सावधान! यह एक फ्रॉड या स्पैम संदेश हो सकता है।")
        else:
            st.markdown(
                """
                <div style="
                    background: rgba(16, 185, 129, 0.1) !important;
                    border: 2px solid #10b981 !important;
                    border-radius: 8px !important;
                    padding: 15px !important;
                    text-align: center !important;
                ">
                    <h3 style="color: #10b981 !important; font-family: monospace; font-weight: bold; margin: 0; font-size: 20px;">✅ THREAT SCAN: SECURE (HAM)</h3>
                </div>
                """, 
                unsafe_allow_html=True
            )
            play_voice_alert("यह संदेश पूरी तरह सुरक्षित है।")

st.markdown('</div>', unsafe_allow_html=True)
