import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

st.set_page_config(page_title="AI Cyber Shield Classifier", page_icon="🛡️", layout="centered")

matrix_bg_html = """
<canvas id="matrixCanvas"></canvas>
<style>
    /* Full screen background canvas */
    #matrixCanvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -9999;
        background-color: #060814;
    }
    
    /* Make Streamlit background transparent to show Matrix canvas */
    .stApp {
        background: transparent !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background: transparent !important;
    }
    
    /* Elegant futuristic glassmorphic container */
    .main-box {
        background: rgba(10, 15, 30, 0.85) !important;
        border: 2px solid #00ff66 !important;
        border-radius: 16px !important;
        padding: 30px !important;
        box-shadow: 0 0 25px rgba(0, 255, 102, 0.25) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        color: #ffffff !important;
        margin-top: 20px;
    }
    
    /* Glowing typography style */
    h1 {
        color: #00ff66 !important;
        text-shadow: 0 0 10px rgba(0, 255, 102, 0.8) !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
        text-align: center;
    }
    
    p, label, span {
        color: #e0e0e0 !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    
    /* High-tech text area styling */
    .stTextArea textarea {
        background-color: rgba(5, 10, 20, 0.9) !important;
        color: #00ff66 !important;
        border: 1px solid #00ff66 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 16px !important;
        box-shadow: inset 0 0 10px rgba(0, 255, 102, 0.1) !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #00ff66 !important;
        box-shadow: 0 0 15px rgba(0, 255, 102, 0.5) !important;
    }
    
    /* Neon glow terminal button */
    div.stButton > button {
        background-color: #00ff66 !important;
        color: #060814 !important;
        font-weight: bold !important;
        border: none !important;
        width: 100% !important;
        padding: 12px 20px !important;
        border-radius: 8px !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        box-shadow: 0 4px 15px rgba(0, 255, 102, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    div.stButton > button:hover {
        background-color: #ffffff !important;
        box-shadow: 0 0 25px rgba(0, 255, 102, 0.8) !important;
        transform: translateY(-2px) !important;
    }
</style>

<script>
    const canvas = document.getElementById('matrixCanvas');
    const ctx = canvas.getContext('2d');

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    // Falling binary stream characters (0 and 1)
    const alphabet = '01';
    const fontSize = 16;
    const columns = canvas.width / fontSize;

    const rainDrops = [];
    for (let x = 0; x < columns; x++) {
        rainDrops[x] = Math.random() * -100;
    }

    function drawMatrix() {
        ctx.fillStyle = 'rgba(6, 8, 20, 0.1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#00ff66';
        ctx.font = fontSize + 'px monospace';
        ctx.shadowBlur = 8;
        ctx.shadowColor = '#00ff66';

        for (let i = 0; i < rainDrops.length; i++) {
            const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
            ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);

            if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                rainDrops[i] = 0;
            }
            rainDrops[i] += 0.85; // Matrix fall speed
        }
    }

    setInterval(drawMatrix, 30);
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
                    msg.lang = 'hi-IN'; // Elegant Hindi speech dialect
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

# Status badge showing real-time ML score
st.markdown(
    f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <span style="
            background: rgba(0, 255, 102, 0.15);
            border: 1px solid #00ff66;
            color: #00ff66;
            padding: 5px 15px;
            border-radius: 50px;
            font-size: 14px;
            font-family: monospace;
            box-shadow: 0 0 10px rgba(0, 255, 102, 0.3);
        ">
            SYSTEM ONLINE | ACCURACY: {accuracy*100:.2f}%
        </span>
    </div>
    """, 
    unsafe_allow_html=True
)

# User Text area inside the glass container
user_input = st.text_area("Hacker, enter SMS or Email message to scan:", placeholder="Type or paste your message here...")

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

if st.button("RUN SCANNING"):
    if user_input.strip() == "":
        st.warning("Pehle scan karne ke liye text enter karein!")
    else:
        # Custom Bypass Rules for Common Spam keywords
        spam_keywords = ["won", "claim", "clam", "lottery", "prize", "crore", "lakh", "selected", "free gift", "rewarded"]
        is_spam_keyword = any(word in user_input.lower() for word in spam_keywords)

        # Bank/Safe Keywords
        safe_keywords = ["debited", "credited", "refno", "upi user", "a/c", "sbi"]
        is_bank_msg = any(word in user_input.lower() for word in safe_keywords)

        # Vectorization & Prediction (Instant)
        vect = cv.transform([user_input])
        prediction = model.predict(vect)
        
        # Final Hybrid Classification
        if is_bank_msg:
            is_spam = False
        elif is_spam_keyword:
            is_spam = True
        elif prediction[0] == 1:
            is_spam = True
        else:
            is_spam = False

        st.markdown("<hr style='border: 1px solid rgba(0, 255, 102, 0.2);'>", unsafe_allow_html=True)

        if is_spam:
            st.markdown(
                """
                <div style="
                    background: rgba(255, 0, 50, 0.15) !important;
                    border: 2px solid #ff003c !important;
                    border-radius: 8px !important;
                    padding: 15px !important;
                    text-align: center !important;
                    box-shadow: 0 0 15px rgba(255, 0, 60, 0.4) !important;
                ">
                    <h3 style="color: #ff003c !important; font-family: monospace; font-weight: bold; margin: 0;">🚨 THREAT DETECTED: SPAM</h3>
                </div>
                """, 
                unsafe_allow_html=True
            )
            play_voice_alert("सावधान! यह एक फ्रॉड या स्पैम संदेश हो सकता है।")
        else:
            st.markdown(
                """
                <div style="
                    background: rgba(0, 255, 102, 0.1) !important;
                    border: 2px solid #00ff66 !important;
                    border-radius: 8px !important;
                    padding: 15px !important;
                    text-align: center !important;
                    box-shadow: 0 0 15px rgba(0, 255, 102, 0.3) !important;
                ">
                    <h3 style="color: #00ff66 !important; font-family: monospace; font-weight: bold; margin: 0;">✅ THREAT SCAN: SECURE (HAM)</h3>
                </div>
                """, 
                unsafe_allow_html=True
            )
            play_voice_alert("यह संदेश पूरी तरह सुरक्षित है।")

st.markdown('</div>', unsafe_allow_html=True)
