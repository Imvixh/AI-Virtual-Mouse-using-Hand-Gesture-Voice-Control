import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import psutil

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

engine = pyttsx3.init()

# Commands map
commands = {
    "notepad": "notepad",
    "paint": "mspaint",
    "chrome": "start chrome",
    "youtube": "https://www.youtube.com",
    "whatsapp": "https://web.whatsapp.com",
    "instagram": "https://www.instagram.com",
    "chatgpt": "https://chat.openai.com",
    "photos": "ms-photos:",
    "excel": "start excel",
    "files": "explorer",
    "camera": "start microsoft.windows.camera:",
    "settings": "start ms-settings:"
}

app_processes = [
    "notepad.exe",
    "mspaint.exe",
    "chrome.exe",
    "EXCEL.EXE",
    "PhotosApp.exe",
    "CameraApp.exe"
]

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_and_execute():
    recognizer = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening (Say: Jarvis open <app>)...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")

                if command.startswith("jarvis open"):
                    for app, action in commands.items():
                        if app in command:
                            speak(f"Opening {app}")
                            if action.startswith("http"):
                                webbrowser.open(action)
                            else:
                                os.system(action)
                            break

                elif "jarvis close all" in command:
                    speak("Closing all apps")
                    for proc in psutil.process_iter():
                        try:
                            if proc.name().lower() in app_processes:
                                proc.kill()
                        except:
                            pass
                else:
                    print("No valid Jarvis command.")
        except Exception as e:
            print(f"Voice error: {e}")
