import requests

api_key = "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"
endpoint = "https://api.groq.com/openai/v1/chat/completions"

def chat(prompt):
    res = requests.post(endpoint,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mixtral-8x7b-32768",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    print("Bot:", res.json()["choices"][0]["message"]["content"])

while True:
    user = input("You: ")
    chat(user)
