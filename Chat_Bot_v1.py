#Goal for this project is to correct code present on the screen with voice commands

#basic outline has completed
import spacy
import os
import pyttsx3
import speech_recognition as sr
import time

# Initialize spaCy model and pyttsx3 engine
nlp = spacy.load('en_core_web_sm')
engine = pyttsx3.init()

# Function to preprocess text
def preprocess_text(text):
    doc = nlp(text)
    return [token.lemma_ for token in doc if not token.is_stop]

# Function to recognize intent based on preprocessed text
def recognize_intent(preprocessed_text):
    if "open" in preprocessed_text and "browser" in preprocessed_text:
        return "open_browser"
    elif "time" in preprocessed_text:
        return "tell_time"
    elif "exit" in preprocessed_text or "stop" in preprocessed_text:
        return "exit"
    # Add more intents as needed

# Function to execute commands based on the intent
def execute_command(intent):
    if intent == "open_browser":
        os.system("start chrome")  # For Windows
    elif intent == "tell_time":
        return time.strftime("%H:%M:%S")
    elif intent == "exit":
        return "exit"

# Function to use the speech recognizer
recognizer = sr.Recognizer()

def listen_command():
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Limiting listening time
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

# Function to speak the response
def speak_response(response):
    engine.say(response)
    engine.runAndWait()

# Main chatbot loop
def chatbot():
    while True:
        print("Entering chatbot loop...")
        user_input = listen_command()
        if user_input is None:
            print("Error: No user input recognized")
            continue

        print("User input:", user_input)
        preprocessed = preprocess_text(user_input)
        intent = recognize_intent(preprocessed)

        response = execute_command(intent)
        if response:
            print("Bot:", response)
            speak_response(response)
            if response == "exit":
                break  # Exit the loop if the intent is to exit

chatbot()
