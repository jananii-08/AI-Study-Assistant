import speech_recognition as sr
import sounddevice as sd
from scipy.io.wavfile import write

def listen_to_voice():

    # Recording settings
    fs = 44100
    seconds = 5

    try:

        print("Start speaking...")

        # Record audio
        audio_data = sd.rec(
            int(seconds * fs),
            samplerate=fs,
            channels=1,
            dtype='int16'
        )

        sd.wait()

        print("Recording done")

        # Save temporary audio file
        write("recorded.wav", fs, audio_data)

        # Speech Recognition
        recognizer = sr.Recognizer()

        with sr.AudioFile("recorded.wav") as source:

            audio = recognizer.record(source)

        print("Recognizing text...")

        # English recognition
        text = recognizer.recognize_google(
            audio,
            language='en-US'
        )

        return text

    except Exception as e:

        return f"Error: {e}"