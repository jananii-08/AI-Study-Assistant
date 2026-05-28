from gtts import gTTS
from playsound3 import playsound
import threading

def play_sound():

    playsound("audio.mp3")

def speak_text(message):

    try:

        speech = gTTS(
            text=message,
            lang='en'
        )

        speech.save("audio.mp3")

        # Run audio separately
        threading.Thread(
            target=play_sound,
            daemon=True
        ).start()

    except Exception as e:

        print("Error:", e)