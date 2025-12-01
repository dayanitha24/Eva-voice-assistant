# -- coding: utf-8 --

import json
import os
import datetime
import pyttsx3
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import pyaudio
import pywhatkit
import random

# ------------------- FILES FOR MEMORY -------------------
MEMORY_FILE = "memory.json"
COMMANDS_FILE = "user_commands.json"

# Load or create memory
if not os.path.exists(MEMORY_FILE):
    json.dump({"name": None}, open(MEMORY_FILE, "w"))
memory = json.load(open(MEMORY_FILE))

# Load or create user-defined commands
if not os.path.exists(COMMANDS_FILE):
    json.dump({}, open(COMMANDS_FILE, "w"))
user_commands = json.load(open(COMMANDS_FILE))

# ------------------- TEXT-TO-SPEECH -------------------
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.say(text)
    engine.runAndWait()

# ------------------- SAVE MEMORY -------------------
def save_files():
    json.dump(memory, open(MEMORY_FILE, "w"))
    json.dump(user_commands, open(COMMANDS_FILE, "w"))

# ------------------- USER-DEFINED COMMANDS -------------------
def learn_command(command):
    # Pattern: "when I say <trigger> reply <response>"
    if "when i say" in command and "reply" in command:
        trigger = command.split("when i say")[1].split("reply")[0].strip()
        response = command.split("reply")[1].strip()
        user_commands[trigger] = response
        save_files()
        speak(f"I learned the command: {trigger}")
        return True
    return False

# ------------------- BUILT-IN COMMANDS -------------------
def handle_command(command):
    # Check user-defined commands
    if command in user_commands:
        speak(user_commands[command])
        return

    # Greetings
    if command in ["hello", "hi", "hey"]:
        speak(random.choice(["Hello!", "Hi there!", "Hey!"]))

    # Name handling
    elif "my name is" in command:
        name = command.replace("my name is", "").strip()
        memory["name"] = name
        save_files()
        speak(f"Nice to meet you, {name}")

    elif "what is my name" in command:
        if memory["name"]:
            speak(f"Your name is {memory['name']}")
        else:
            speak("I don't know your name yet.")

    # Time
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")

    # Play song (YouTube)
    elif "play song" in command:
        speak("Which song should I play?")
        song_name = listen_command()
        if song_name:
            speak(f"Playing {song_name}")
            pywhatkit.playonyt(song_name)
        else:
            speak("No song specified.")

    # Joke
    elif "joke" in command:
        jokes = [
            "Why did the computer go to the doctor? Because it had a virus.",
            "Debugging is like being the detective in a crime movie where you are also the murderer.",
            "I told a joke about UDP. Nobody got it."
        ]
        speak(random.choice(jokes))

    # Motivational
    elif "motivate me" in command or "motivation" in command:
        quotes = [
            "You are stronger than you think.",
            "Every day is a second chance.",
            "Dream big, work hard, stay focused."
        ]
        speak(random.choice(quotes))

    # Calculator (simple)
    elif any(x in command for x in ["plus", "minus", "times", "divided"]):
        try:
            expr = (
                command.replace("plus", "+")
                .replace("minus", "-")
                .replace("times", "*")
                .replace("multiplied by", "*")
                .replace("divided by", "/")
            )
            result = eval(expr)
            speak(f"The answer is {result}")
        except:
            speak("I could not calculate that.")

    # Unknown command
    else:
        speak("I don't know that yet. You can teach me by saying: when I say <trigger> reply <response>")

# ------------------- LISTEN FOR COMMAND -------------------
def listen_command():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("🎤 Listening for command...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
            command = recognizer.recognize_google(audio).lower()
            print("You:", command)
            return command
    except:
        return ""

# ------------------- WAKE WORD DETECTION -------------------
def listen_wakeword():
    model = Model("wakeword_model") 
    recognizer = KaldiRecognizer(model, 16000)
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000,
                      input=True, frames_per_buffer=8192)
    stream.start_stream()

    print("🎧 Listening for wake word 'Hey Eva' ...")
    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            text = recognizer.Result().lower()
            if "eva" in text or "hey eva" in text:
                speak("Yes, I am listening")
                return

# ------------------- MAIN LOOP -------------------
if __name__ == "__main__":
    speak("Eva is online and ready")
    while True:
        listen_wakeword()  
        command = listen_command()
        if not command:
            continue

        # Stop commands
        if any(x in command for x in ["stop", "exit", "bye", "quit"]):
            speak("Goodbye! Have a great day.")
            break

        # Learn command first
        if learn_command(command):
            continue

        # Handle built-in commands
        handle_command(command)
