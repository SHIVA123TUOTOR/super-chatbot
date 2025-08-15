import streamlit as st
import requests
import base64

# API KEYS
GROQ_API_KEY = "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"
ASSEMBLYAI_API_KEY = "assemblyai-e238350da8ad4b7f8c077731ff80c8f8"
PEXELS_API_KEY = "0x4Fqd2tOFWhdEDn9hC96Y7iXPYTQ6KUV0qX3p9lLu7eR4kAfz3IElB4"
REMOVEBG_API_KEY = "FRZPYZmMn895ZCh5GoctrSqK"
WOLFRAMALPHA_APPID = "GGV577-9U5LR6JR35"
OPENTDB_API_URL = "https://opentdb.com/api.php?amount=50&difficulty=easy"

# Set Streamlit page
st.set_page_config(page_title="Jarvis AI", layout="wide")
st.title("🧠 Jarvis AI - All-in-One Web Assistant")

# User input
user_input = st.text_input("Ask Jarvis anything...", "")

# Function: Groq Chat API
def chat_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

# Function: WolframAlpha Query
def query_wolfram(query):
    url = f"https://api.wolframalpha.com/v1/result?i={query}&appid={WOLFRAMALPHA_APPID}"
    response = requests.get(url)
    return response.text

# Function: Random Quiz
def get_quiz():
    res = requests.get(OPENTDB_API_URL).json()
    q = res['results'][0]
    return f"Q: {q['question']} (Category: {q['category']})\nOptions: {q['incorrect_answers'] + [q['correct_answer']]}"

# Function: Get Pexels Image
def get_image(query):
    headers = {"Authorization": PEXELS_API_KEY}
    res = requests.get(f"https://api.pexels.com/v1/search?query={query}&per_page=1", headers=headers).json()
    if res["photos"]:
        return res["photos"][0]["src"]["original"]
    return "No image found."

# Function: Remove Background
def remove_bg(image_url):
    headers = {
        "X-Api-Key": REMOVEBG_API_KEY
    }
    data = {
        "image_url": image_url,
        "size": "auto"
    }
    res = requests.post("https://api.remove.bg/v1.0/removebg", headers=headers, data=data)
    if res.status_code == 200:
        return res.content
    return None

# Process user input
if user_input:
    with st.spinner("Jarvis is thinking..."):
        try:
            # Check for Wolfram keywords
            if any(x in user_input.lower() for x in ["calculate", "define", "who is", "what is"]):
                answer = query_wolfram(user_input)
            elif "quiz" in user_input.lower():
                answer = get_quiz()
            elif "image" in user_input.lower():
                topic = user_input.split("image of")[-1].strip()
                answer = get_image(topic)
                st.image(answer)
            elif "remove background" in user_input.lower():
                image_url = user_input.split("remove background of")[-1].strip()
                result = remove_bg(image_url)
                if result:
                    st.image(result)
                    st.success("Background removed!")
                else:
                    st.error("Failed to remove background.")
                answer = "Here is your edited image."
            else:
                answer = chat_groq(user_input)

            st.markdown(f"🧠 **Jarvis:** {answer}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

