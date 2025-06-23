import streamlit as st
import requests
import time

# Initialize text-to-speech engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Recognize speech from mic
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening...")
        audio = recognizer.listen(source)
        try:
            st.info("🔍 Recognizing...")
            text = recognizer.recognize_google(audio)
            st.success(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.warning("❌ Could not understand audio")
            return ""
        except sr.RequestError:
            st.error("⚠️ Speech recognition service unavailable")
            return ""

# Chatbot API call
def chat_with_groq(prompt, history):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer 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 ",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": history + [{"role": "user", "content": prompt}]
    }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        reply = res.json()["choices"][0]["message"]["content"]
        return reply
    else:
        return f"⚠️ API Error: {res.status_code} - {res.text}"

# Streamlit UI
st.set_page_config(page_title="Super Chatbot", page_icon="🤖")
st.title("🤖 Super Chatbot - Groq Powered")

if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": "You are a friendly, smart and helpful chatbot like ChatGPT."}
    ]

# Chat display
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.chat_message("You").markdown(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("🤖 Bot").markdown(msg["content"])

# Input from user
col1, col2 = st.columns([4,1])
with col1:
    user_input = st.text_input("Type your message", key="text")
with col2:
    if st.button("🎙️ Speak"):
        user_input = recognize_speech()

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    reply = chat_with_groq(user_input, st.session_state.history)
    st.session_state.history.append({"role": "assistant", "content": reply})
    st.chat_message("You").markdown(user_input)
    st.chat_message("🤖 Bot").markdown(reply)
    speak(reply)

