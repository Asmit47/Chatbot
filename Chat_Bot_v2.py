import os
import pyttsx3
import speech_recognition as sr
import time
import google.generativeai as genai
from config import API_KEY
# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Configure Google Generative AI API
genai.configure(api_key = API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to speak the response
def speak_response(response):
    engine.say(response)
    engine.runAndWait()
# Function to preprocess the user command
def preprocess_text(text):
    return text.lower()

# Function to recognize intent based on the user input
def recognize_intent(preprocessed_text):
    if "open" in preprocessed_text:
        return "open_app"
    elif "brightness" in preprocessed_text:
        return "adjust_brightness"
    elif "volume" in preprocessed_text:
        return "adjust_volume"
    elif "exit" in preprocessed_text or "stop" in preprocessed_text:
        return "exit"
    else:
        return "chat"

# Function to execute commands based on the intent
def execute_command(intent, user_input):
    if intent == "open_app":
        app_name = user_input.replace("open", "").strip()
        os.system(f"start {app_name}")
        return f"Opened {app_name}"
    elif intent == "adjust_brightness":
        brightness_level = user_input.replace("brightness", "").strip()
        # Implement brightness adjustment logic here
        return f"Adjusted brightness to {brightness_level}"
    elif intent == "adjust_volume":
        volume_level = user_input.replace("volume", "").strip()
        # Implement volume adjustment logic here
        return f"Adjusted volume to {volume_level}"
    elif intent == "chat":
        response = model.generate_content(user_input)
        return response.text
    elif intent == "exit":
        return "exit"

# Function to use the speech recognizer
recognizer = sr.Recognizer()

def listen_command():
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Error: Unable to recognize speech")
        return None
    except sr.RequestError as e:
        print(f"Error: Request error - {e}")
        return None
    except sr.WaitTimeoutError:
        print("Error: Wait timeout error")
        return None

# Function to wait for wake word
def wait_for_wake_word():
    print("Waiting for wake word 'Jarvis'...")
    while True:
        user_input = listen_command()
        if user_input and "jarvis" in preprocess_text(user_input):
            return True

# Main chatbot loop
def chatbot():
    while True:
        # Wait for wake word
        if not wait_for_wake_word():
            continue

        print("Wake word detected. Jarvis is active!")
        speak_response("How can I help you?")

        # Enter active listening mode
        while True:
            user_input = listen_command()
            if user_input is None:
                continue

            preprocessed = preprocess_text(user_input)
            intent = recognize_intent(preprocessed)
            response = execute_command(intent, preprocessed)

            if response:
                print("Bot:", response)
                speak_response(response)

                if response == "exit":
                    print("Exiting active mode. Say 'Jarvis' to wake me up again.")
                    break  # Exit the active listening loop

if __name__ == "__main__":
    print("Jarvis is ready. Say 'Jarvis' to activate.")
    chatbot()