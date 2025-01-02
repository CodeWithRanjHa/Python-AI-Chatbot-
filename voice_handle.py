# voice_chatbot.py
import requests
import speech_recognition as sr
import os

# Replace with your Eleven Labs and Gemini API keys
ELEVEN_LABS_API_KEY = 'sk_f26afcb4cd7adfe0c040de2cd1a606ede25be21405f487f8'
GEMINI_API_KEY = 'AIzaSyCg0kt7d_juuukipiDmOzniqblvPsjgav0'
GEMINI_API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}'

assistant_name = "ANNA"

def speak(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/XB0fDUnXU5powFXDhCwa"
    headers = {"xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json"}
    data = {"text": text, "voice_settings": {"stability": 0.7, "similarity_boost": 0.7}}
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        with open("speech.mp3", "wb") as f:
            f.write(response.content)
        os.system("mpg321 speech.mp3")  # Ensure mpg321 is installed for playback
        os.remove("speech.mp3")
    else:
        print("Error with Eleven Labs API:", response.text)

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Sorry, the speech service is unavailable.")

def get_voice_response(user_input):
    prompt_content = f"User: {user_input}\nAnna:"
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

