import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="ctranslate2")
import ollama
import os
import pyttsx3 as py
import datetime as dt
import pyjokes as pj
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
from faster_whisper import WhisperModel

# Load model (tiny, base, small, medium, large-v2)
model = WhisperModel("tiny", device="cpu", compute_type="int8")
def llama_reply(prompt):
    try:
        response = ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]
    except Exception as e:
        return f"Error with llama: {str(e)}"

def listen():

    print("Listening........")
    freq = 44100

# Recording duration
    duration = 3

# Start recorder with the given values
# of duration and sample frequency
    recording = sd.rec(int(duration * freq),
                   samplerate=freq, channels=2)

# Record audio for the given number of seconds
    sd.wait()

# This will convert the NumPy array to an audio
# file with the given sampling frequency
    write("recording0.wav", freq, recording)

# Convert the NumPy array to audio file
    wv.write("recording1.wav", recording, freq, sampwidth=2)
# compute_type can be: int8, int8_float16, float16, float32

# Transcribe audio
    segments, info = model.transcribe("recording1.wav")
    he=''
    print("Detected language:", info.language)
    for segment in segments:
        he+=segment.text
    return he
def speak(text):
    print(f"Assistant: {text}")
    try:
        engine = py.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.say(text)
        engine.runAndWait()
    except:
        print("Speech output not supported in Colab.")

def greet():
    hour = int(dt.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your voice assistant. How can I help you today?")


def write_query(query):
    print(f"User query : {query}")


def open_app(query):
    if "notepad" or "note pad" in query:
        os.system("notepad")
        return "Opening Notepad..."
    else:
        return "Sorry, I don't know that app."


def run():
    greet()
    while True:

        query = listen()
        write_query(query)

        if 'time' in query:
            strTime = dt.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {strTime}")

        elif 'joke' in query:
            joke = pj.get_joke()
            speak(joke)

        elif "open" in query:
            response = open_app(query)
            speak(response)

        elif 'exit' in query or 'bye' in query:
            speak("Goodbye! Have a nice day!")
            break

        else:
            speak("Let me think...")
            answer=llama_reply(query)
            speak(answer)
run()