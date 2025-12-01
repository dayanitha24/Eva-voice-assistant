# EVA Voice Assistant

## Overview
**EVA** is an offline, Python-based voice assistant designed for real-time, hands-free interaction. It supports wake-word detection, user-defined commands, and persistent memory, allowing users to teach EVA new commands and store personal information across sessions. EVA can respond to general queries, tell jokes, play YouTube songs, provide time updates, and perform simple calculations — all without requiring any external APIs.

## Features
- **Wake-Word Detection:** EVA listens for “Hey Eva” using offline speech recognition via VOSK.  
- **Persistent Memory:** Remembers user information like name and custom settings across sessions.  
- **User-Defined Commands:** Users can teach EVA new commands with custom responses.  
- **Built-in Commands:** Includes time announcements, jokes, music playback (YouTube), greetings, and simple calculations.  
- **Offline Functionality:** Works without internet connectivity except for YouTube playback.  

## Technologies Used
- **Python:** Core programming language.  
- **VOSK:** Offline speech recognition and wake-word detection.  
- **PyAudio:** Captures microphone input for voice commands.  
- **pyttsx3:** Text-to-speech engine for responses.  
- **pywhatkit:** YouTube music playback.
  
## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/eva-voice-assistant.git

2.Navigate to the project directory:

