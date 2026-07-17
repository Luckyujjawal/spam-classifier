import pandas as pd
import streamlit as st
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

# --- STREAMLIT WEB UI ---
st.set_page_config(page_title="AI Spam Classifier", page_icon="🛡️")
st.title("🛡️ AI Spam Email/SMS Classifier")
st.write(f"Model Accuracy: **{accuracy*100:.2f}%**")
st.write("---")

user_input = st.text_area("Apna Message yahan paste karein:", placeholder="Type something...")

if st.button("Predict"):
    if user_input.strip() == "":
        st.warning("Pehle text enter karein!")
    else:
        vect = cv.transform([user_input])
        prediction = model.predict(vect)
        if prediction[0] == 1:
            st.error("🚨 SPAM Message!")
        else:
            st.success("✅ Safe (HAM) Message.")