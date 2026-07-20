import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# --- DATA LOAD ---
try:
    df = pd.read_csv("spam (1).csv", encoding="latin-1")
    df = df.dropna(how="any", axis=1)
    df.columns = ["label", "message"]
except Exception as e:
    st.error(f"Dataset load nahi ho paya! Error: {e}")

# Data prep
df["label_num"] = df["label"].map({"ham": 0, "spam": 1})
X = df["message"]
y = df["label_num"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorization
cv = CountVectorizer()
X_train_vectorized = cv.fit_transform(X_train)
X_test_vectorized = cv.transform(X_test)

# Model Training
model = MultinomialNB()
model.fit(X_train_vectorized, y_train)
accuracy = model.score(X_test_vectorized, y_test)

# --- WEB UI CONFIG ---
st.set_page_config(page_title="AI Spam Classifier", page_icon="🛡️")
st.title("🛡️ AI Spam Email/SMS Classifier")
st.write(f"Model Accuracy: **{accuracy*100:.2f}%**")
st.write("---")

# User Input Box
user_input = st.text_area("Apna Message yahan paste karein:", placeholder="Type or paste your SMS here...")

# --- SPEECH SYNTHESIS ENGINE (HTML + JS) ---
def play_voice_alert(text, button_color="#4CAF50"):
    html_code = f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-top: 10px;">
        <button onclick="playTTS()" style="
            background-color: {button_color}; 
            color: white; 
            border: none; 
            padding: 8px 16px; 
            border-radius: 5px; 
            cursor: pointer; 
            font-size: 14px; 
            font-weight: bold;
            font-family: sans-serif;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.2);
        ">
            🔊 Voice Alert Suniye
        </button>
    </div>

    <script>
        function playTTS() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance("{text}");
                msg.lang = 'hi-IN';
                msg.pitch = 1.0;
                msg.rate = 0.95;
                window.speechSynthesis.speak(msg);
            }}
        }}
        setTimeout(playTTS, 100);
    </script>
    """
    components.html(html_code, height=55)

# Predict Button logic
if st.button("Predict"):
    if user_input.strip() == "":
        st.warning("Pehle text enter karein!")
    else:
        # Bank ke genuine keywords check karne ke liye custom bypass rule
        safe_keywords = ["debited", "credited", "refno", "upi user", "a/c", "sbi"]
        is_bank_msg = any(word in user_input.lower() for word in safe_keywords)

        vect = cv.transform([user_input])
        prediction = model.predict(vect)
        
        # Result decision
        if prediction[0] == 1 and is_bank_msg:
            is_spam = False
        elif prediction[0] == 1:
            is_spam = True
        else:
            is_spam = False

        # Output Results
        if is_spam:
            st.error("🚨 SPAM Message!")
            play_voice_alert("सावधान! यह एक फ्रॉड या स्पैम संदेश हो सकता है।", button_color="#d9534f")
        else:
            st.success("✅ Safe (HAM) Message.")
            play_voice_alert("यह संदेश पूरी तरह सुरक्षित है।", button_color="#5cb85c")
