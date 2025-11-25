import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import subprocess
import pyjokes

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def time():
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak("The current time is")
    speak(current_time)
    print("The current time is", current_time)


def date():
    now = datetime.datetime.now()
    speak("The current date is")
    speak(f"{now.day} {now.strftime('%B')} {now.year}")
    print(f"The current date is {now.day}/{now.month}/{now.year}")


def wishme():
    speak("Welcome back, sir!")
    print("Welcome back, sir!")

    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 16:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

    assistant_name = load_name()
    speak(f"{assistant_name} at your service. Please tell me how may I assist you.")
    print(f"{assistant_name} at your service.")


def screenshot():
    """EC2 ला GUI नाही → Real screenshot काम करणार नाही"""
    dummy_path = "/opt/jarvis/screenshot.png"
    with open(dummy_path, "w") as f:
        f.write("EC2 has no GUI to take screenshots.\n")

    speak("Screenshot feature is not available on EC2 server.")
    print("Screenshot skipped (No GUI on EC2).")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1

        try:
            audio = r.listen(source, timeout=5)
        except:
            speak("Timeout occurred.")
            return None

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(query)
        return query.lower()

    except:
        speak("Sorry, I did not understand.")
        return None


def play_music(song_name=None):
    music_dir = os.path.expanduser("~/Music")

    if not os.path.exists(music_dir):
        speak("Music folder not found.")
        return

    songs = os.listdir(music_dir)
    if song_name:
        songs = [s for s in songs if song_name.lower() in s.lower()]

    if songs:
        song = random.choice(songs)
        song_path = os.path.join(music_dir, song)
        subprocess.Popen(["xdg-open", song_path])  # Linux alternative
        speak(f"Playing {song}")
        print(f"Playing {song}")
    else:
        speak("No matching song found.")
        print("No matching song found.")


def set_name():
    speak("What should I call myself?")
    name = takecommand()
    if name:
        with open("assistant_name.txt", "w") as f:
            f.write(name)
        speak(f"Alright, I will be called {name} now.")


def load_name():
    try:
        with open("assistant_name.txt", "r") as f:
            return f.read().strip()
    except:
        return "Jarvis"


def search_wikipedia(query):
    try:
        speak("Searching Wikipedia...")
        result = wikipedia.summary(query, sentences=2)
        speak(result)
        print(result)
    except:
        speak("No results found.")


if __name__ == "__main__":
    wishme()

    while True:
        query = takecommand()
        if not query:
            continue

        if "time" in query:
            time()

        elif "date" in query:
            date()

        elif "wikipedia" in query:
            query = query.replace("wikipedia", "")
            search_wikipedia(query)

        elif "play music" in query:
            song = query.replace("play music", "").strip()
            play_music(song)

        elif "open youtube" in query:
            wb.open("https://youtube.com")

        elif "open google" in query:
            wb.open("https://google.com")

        elif "change your name" in query:
            set_name()

        elif "screenshot" in query:
            screenshot()

        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)

        elif "offline" in query or "exit" in query:
            speak("Going offline. Have a good day!")
            break
