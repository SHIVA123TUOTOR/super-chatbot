import streamlit as st
import requests

st.set_page_config(page_title="Super Chatbot", page_icon="🤖")
st.title("🤖 Super Chatbot - Groq Powered")

# Groq API function
def chat_with_groq(prompt, history):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": history + [{"role": "user", "content": prompt}]
    }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        return res.json()["choices"][0]["message"]["content"]
    else:
        return f"⚠️ API Error: {res.status_code}\n{res.text}"

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display previous chat
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.chat_message("You").markdown(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("🤖 Bot").markdown(msg["content"])

# Text input
user_input = st.chat_input("Say something...")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    response = chat_with_groq(user_input, st.session_state.history)
    st.session_state.history.append({"role": "assistant", "content": response})
    st.chat_message("🤖 Bot").markdown(response)
