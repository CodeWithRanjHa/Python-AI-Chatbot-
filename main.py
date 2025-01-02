import requests
from dotenv import load_dotenv
import os

load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API")
GEMINI_API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}'

assistant_name = "ANNA"
system_prompt = {
    'role': 'system',
    'content': (
        "You are a friendly and helpful AI voice assistant. Respond to user questions in a natural, conversational tone. "
        "Keep your answers brief and to the point, while remaining engaging and approachable."
    )
}

def get_text_response(user_input):
    prompt_content = f"{system_prompt['content']}\nUser: {user_input}\nAnna:"

    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "parts": [{"text": prompt_content}]
            }
        ]
    }

    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        try:
            ai_text = response.json()['candidates'][0]['content']['parts'][0]['text']
            return ai_text
        except KeyError:
            return "Sorry, I couldn't understand the response format."
    else:
        return f"Error: {response.status_code} - {response.text}"


