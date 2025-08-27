import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv
import openai

from openai import OpenAI

client = OpenAI(
  organization='org-p7sZdXn8rgT33bX9r2zGLru0',
  project='$PROJECT_ID',
)

# Load environment variables
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

# Set OpenAI API key
openai.api_key = OPENAI_KEY

# Text-to-speech function
def speak_text(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Speech recognizer
r = sr.Recognizer()

# Function to record speech and return text
def record_text():
    while True:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                print("I'm listening...")
                audio2 = r.listen(source2)
                my_text = r.recognize_google(audio2)
                return my_text
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Unknown error occurred")

# Function to send messages to ChatGPT and get response
def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    messages.append({"role": "assistant", "content": response.choices[0].message.content})
    return response.choices[0].message.content

# Main loop
messages = []
while True:
    text = record_text()
    messages.append({"role": "user", "content": text})
    response = send_to_chatGPT(messages)
    speak_text(response)
    print(response)
