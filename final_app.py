import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# --- WEB UI CONFIG ---
st.set_page_config(page_title="AI Cyber Spam Guard", page_icon="🛡️", layout="centered")

# --- CUSTOM CSS FOR PREMIUM HIGH-TECH LOOK ---
st.markdown("""
    <style>
    /* Global background gradient */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% 50%, #0f172a 0%, #030712 100%) !important;
    }
    
    /* Input Text Area premium look */
    textarea {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        font-size: 16px !important;
    }
    textarea:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.3) !important;
    }

    /* Style Streamlit primary button */
    div.stButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 30px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
        transition: all 0.3s ease-in-out !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5) !important;
    }

    /* Beautiful custom Alert Box for Safe (HAM) */
    .glowing-card-safe {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 2px solid #10b981 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        color: #f8fafc !important;
        font-size: 18px !important;
        font-weight: bold !important;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.25) !important;
        margin-top: 15px !important;
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
    }

    /* Beautiful custom Alert Box for Spam */
    .glowing-card-spam {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 2px solid #ef4444 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        color: #f8fafc !important;
        font-size: 18px !important;
        font-weight: bold !important;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.25) !important;
        margin-top: 15px !important;
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)


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

# Resources load karein
model, cv, accuracy = load_and_train_model()

if model is None:
    st.error("Dataset load nahi ho paya!")
    st.stop()


# --- HEADER SECTION ---
st.markdown("""
    <div style="text-align: center; padding: 10px 0 30px 0;">
        <span style="background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.4); padding: 6px 16px; border-radius: 20px; font-size: 13px; font-weight: bold; color: #3b82f6; text-transform: uppercase; letter-spacing: 1px;">
            🤖 Advanced AI Guard System
        </span>
        <h1 style="margin-top: 15px; font-size: 42px; font-weight: 800; background: linear-gradient(90deg, #10b981, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🛡️ AI Spam Shield Classifier
        </h1>
        <p style="color: #94a3b8; font-size: 16px; margin-top: 5px;">
            Secure your daily life. Keep fraud, scams, and fake alert messages away.
        </p>
        <span style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 5px 14px; border-radius: 8px; color: #10b981; font-weight: bold; font-size: 14px;">
            🎯 Model accuracy: """ + f"{accuracy*100:.2f}%" + """
        </span>
    </div>
""", unsafe_allow_html=True)


# --- INPUT BOX ---
user_input = st.text_area("Apna Message yahan paste karein:", placeholder="Type or paste your SMS or Email here...", height=150)


# --- GUARANTEED AUTO-PLAY VOICE FUNCTION ---
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


# Predict Button logic
if st.button("Predict"):
    if user_input.strip() == "":
        st.warning("Pehle text enter karein!")
    else:
        # 1. Custom Bypass Rules for Common Spam keywords
        spam_keywords = ["won", "claim", "clam", "lottery", "prize", "crore", "lakh", "selected", "free gift", "rewarded"]
        is_spam_keyword = any(word in user_input.lower() for word in spam_keywords)

        # 2. Bank/Safe Keywords
        safe_keywords = ["debited", "credited", "refno", "upi user", "a/c", "sbi"]
        is_bank_msg = any(word in user_input.lower() for word in safe_keywords)

        # Vectorization & Prediction
        vect = cv.transform([user_input])
        prediction = model.predict(vect)
        
        # Final Decision Logic
        if is_bank_msg:
            is_spam = False
        elif is_spam_keyword:
            is_spam = True
        elif prediction[0] == 1:
            is_spam = True
        else:
            is_spam = False

        # Output Results with glowing custom HTML cards
        if is_spam:
            st.markdown("""
                <div class="glowing-card-spam">
                    <span>🚨</span>
                    <div>
                        <div style="font-size: 18px; color: #ef4444; margin-bottom: 2px;">SPAM Message Detected!</div>
                        <div style="font-size: 14px; font-weight: normal; color: #cbd5e1;">Be careful. This message is flagged as a potential fraud or scam.</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            play_voice_alert("सावधान! यह एक फ्रॉड या स्पैम संदेश हो सकता है।")
        else:
            st.markdown("""
                <div class="glowing-card-safe">
                    <span>✅</span>
                    <div>
                        <div style="font-size: 18px; color: #10b981; margin-bottom: 2px;">Safe (HAM) Message Verified</div>
                        <div style="font-size: 14px; font-weight: normal; color: #cbd5e1;">This message is verified and secure to read. No threats detected.</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            play_voice_alert("यह संदेश पूरी तरह सुरक्षित है।")
