import speech_recognition as sr
import webbrowser
import os
import pywhatkit
import musicLibrary
import pyautogui
from client import client
from gtts import gTTS
import pygame
import time
import notepad


recognizer = sr.Recognizer()


def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "speech.mp3"
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.quit()
    os.remove(filename)


def ask_groq(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are Jarvis, a helpful voice assistant. Reply briefly, naturally, and clearly like a real assistant. Keep it short enough to speak aloud."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq error: {e}")
        return "Sorry, I could not reach the AI service right now."


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")

    elif "open notepad" in c.lower():
        os.startfile("C:\\Windows\\System32\\notepad.exe")

    elif c.lower().startswith("write"):
        text = c.lower().split(" ")[1]
        key = notepad.notepaddic.get(text)
        if key:
            os.startfile("C:\\Windows\\System32\\notepad.exe")
            with open("C:\\Windows\\System32\\notepad.exe", "w") as f:
                f.write(key)

    elif "python" in c.lower():
        pywhatkit.search("Python classes")

    elif "open whatsapp" in c.lower():
        webbrowser.open("https://web.whatsapp.com/")

    elif "send me" in c.lower():
        phone_number = os.getenv("JARVIS_WHATSAPP_NUMBER")
        if not phone_number:
            print("Set JARVIS_WHATSAPP_NUMBER to enable WhatsApp messaging.")
            return
        pywhatkit.sendwhatmsg_instantly(phone_number, "Hello, this is a test message from Jarvis.", wait_time=10, tab_close=True, close_time=3)

    elif c.lower().startswith("play"):
        songs = c.lower().split(" ")[1]
        link = musicLibrary.music.get(songs)
        webbrowser.open(link)

    elif "take screenshot" in c.lower():
        image = pyautogui.screenshot()
        image.save("screenshot.png")
        speak("screenshot taken")

    else:
        reply = ask_groq(c)
        print(reply)
        speak(reply)

if __name__ == "__main__":
    speak("Initializing Jarvis....")

    while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

            word = recognizer.recognize_google(audio).lower()
            print(f"Heard: {word}")

            if "jarvis" in word:
                speak("Yes Boss... How can I help you")
                with sr.Microphone() as source:
                    print("Activated. Listening for command...")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
                    command = recognizer.recognize_google(audio)
                    print(f"Command: {command}")
                    processCommand(command)
            else:
                print("Wake word not detected. Say 'Jarvis' clearly.")
        except sr.UnknownValueError:
            print("Couldn't understand the audio.")
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
