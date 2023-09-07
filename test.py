import os
import openai
import time
import speech_recognition as sr
import pyttsx3
import numpy as np
from gtts import gTTS
import pygame

# Set your OpenAI API key
openai.api_key = 'YOUR_API_KEY'

# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init("dummy")
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)

# Define the wake word and greetings
wake_word = "hey"
name = "Pangea"
greetings = [f"whats up master {name}",
             "yeah?",
             "Well, hello there, Master of Puns and Jokes - how's it going today?",
             f"Ahoy there, Captain {name}! How's the ship sailing?",
             f"Bonjour, Monsieur {name}! Comment ça va? Wait, why the hell am I speaking French?"]

# Function to play audio using pygame
def play_audio(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Listen for the wake word "hey"
def listen_for_wake_word(source):
    print("Listening for 'Hey'...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if wake_word in text.lower():
                print("Wake word detected.")
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass

# Listen for input and respond with OpenAI API
def listen_and_respond(source):
    print("Listening...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            if not text:
                continue

            # Send input to OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"{text}"}]
            )
            response_text = response.choices[0].message.content
            print(response_text)

            # Generate audio response
            myobj = gTTS(text=response_text, lang="en", slow=False)
            myobj.save("response.mp3")
            print("speaking")
            play_audio("response.mp3")

            # Speak the response
            print("speaking")
            engine.say(response_text)
            engine.runAndWait()

            if not audio:
                listen_for_wake_word(source)
        except sr.UnknownValueError:
            time.sleep(2)
            print("Silence found, shutting up, listening...")
            listen_for_wake_word(source)
            break
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(f"Could not request results; {e}")
            engine.runAndWait()
            listen_for_wake_word(source)
            break

# Use the default microphone as the audio source (adjust device_index if needed)
with sr.Microphone(device_index=1) as source:
    listen_for_wake_word(source)
