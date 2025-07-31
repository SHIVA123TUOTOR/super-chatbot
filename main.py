import requests
import os

# API Keys
GROQ_API = "groq-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"
WOLFRAM_API = "GGV577-9U5LR6JR35"
PEXELS_API = "0x4Fqd2tOFWhdEDn9hC96Y7iXPYTQ6KUV0qX3p9lLu7eR4kAfz3IElB4"
REMOVEBG_API = "FRZPYZmMn895ZCh5GoctrSqK"
TRIVIA_URL = "https://opentdb.com/api.php?amount=1"

def chat_with_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8
    }
    res = requests.post(url, headers=headers, json=body)
    return res.json()['choices'][0]['message']['content']

def solve_math(query):
    url = f"http://api.wolframalpha.com/v1/result?appid={WOLFRAM_API}&i={query}"
    res = requests.get(url)
    return res.text

def get_trivia():
    res = requests.get(TRIVIA_URL).json()
    q = res['results'][0]
    return f"🧠 Trivia:\nQ: {q['question']}\nA: {q['correct_answer']}"

def get_pexels_image(query):
    headers = {"Authorization": PEXELS_API}
    res = requests.get(f"https://api.pexels.com/v1/search?query={query}&per_page=1", headers=headers)
    try:
        photo_url = res.json()['photos'][0]['src']['original']
        img = requests.get(photo_url)
        with open("pexels_image.jpg", "wb") as f:
            f.write(img.content)
        return "Image downloaded as 'pexels_image.jpg'"
    except:
        return "No image found."

def remove_bg(image_path):
    with open(image_path, 'rb') as f:
        files = {'image_file': f}
        headers = {'X-Api-Key': REMOVEBG_API}
        response = requests.post('https://api.remove.bg/v1.0/removebg', files=files, headers=headers)
        if response.status_code == 200:
            with open("no_bg.png", "wb") as out:
                out.write(response.content)
            return "Background removed and saved as 'no_bg.png'"
        else:
            return "Background removal failed."

def main():
    print("🤖 Welcome to Jarvis AI (Text Mode)")
    while True:
        cmd = input("🗨  You: ").strip()
        
        if cmd.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        elif cmd.startswith("math "):
            print("🧮", solve_math(cmd[5:]))

        elif cmd.lower() == "trivia":
            print(get_trivia())

        elif cmd.startswith("image "):
            topic = cmd[6:]
            print(get_pexels_image(topic))

        elif cmd.startswith("removebg "):
            path = cmd[9:]
            print(remove_bg(path))

        else:
            print("💬", chat_with_groq(cmd))

if _name_ == "_main_":
    main()
