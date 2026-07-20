import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# --- WEB UI CONFIG ---
st.set_page_config(page_title="AI Spam Classifier", page_icon="🛡️")

# --- CACHED MODEL TRAINING ---
# Isse model training sirf ek baar website khulne par hogi, click karne par delay khatam!
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

st.title("🛡️ AI Spam Email/SMS Classifier")
st.write(f"Model Accuracy: **{accuracy*100:.2f}%**")
st.write("---")

# User Input Box
user_input = st.text_area("Apna Message yahan paste karein:", placeholder="Type or paste your SMS here...")

# --- GUARANTEED AUTO-PLAY VOICE FUNCTION ---
def play_voice_alert(text):
    iframe_html = f"""
    <iframe srcdoc="
        <script>
            function speak() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel(); // Purani aawaz ko rokein
                    var msg = new SpeechSynthesisUtterance('{text}');
                    msg.lang = 'hi-IN'; // Pure Hindi Accent
                    msg.pitch = 1.0;
                    msg.rate = 1.0;
                    window.speechSynthesis.speak(msg);
                }}
            }}
            setTimeout(speak, 10); // Instant 10 milliseconds delay
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

        # Vectorization & Prediction (Instant because model is pre-trained)
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

        # Output Results
        if is_spam:
            st.error("🚨 SPAM Message!")
            play_voice_alert("सावधान! यह एक फ्रॉड या स्पैम संदेश हो सकता है।")
        else:
            st.success("✅ Safe (HAM) Message.")
            play_voice_alert("यह संदेश पूरी तरह सुरक्षित है।")
