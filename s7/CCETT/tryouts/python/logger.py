import pyautogui
import time
import pyaudio
import wave
import keyboard
import threading
import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS

print("Press 'Ctrl + C' to exit.")

frames = []
exit_flag = False

def get_audio():
    global exit_flag
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            while not exit_flag:
                audio = r.listen(source)
                said = ""
                try:
                    said = r.recognize_google(audio)
                    print(said)
                except Exception as e:
                    print("Exception: " + str(e))
    except KeyboardInterrupt:
        pass  # Handle the KeyboardInterrupt gracefully

audio_thread = threading.Thread(target=get_audio)
audio_thread.start()

def on_key_event(keyboard_event):
    global exit_flag
    if keyboard_event.event_type == keyboard.KEY_DOWN:
        print(f"Key '{keyboard_event.name}' pressed")
        # Perform actions based on the detected key
        
        # For example, if the 'q' key is pressed, set the exit flag to True
        if keyboard_event.name == 'q':
            exit_flag = True

# Start the keyboard event listener in a separate thread
keyboard_thread = threading.Thread(target=keyboard.hook, args=(on_key_event,))
keyboard_thread.start()

# Wait for audio thread to finish
audio_thread.join()
print("Exiting program.")
