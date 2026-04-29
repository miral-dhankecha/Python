# main.py
import speech_recognition as sr
import pyttsx3
import datetime
from automation.commands import execute_command

# ---------------- VOICE ENGINE ----------------
engine = pyttsx3.init()
engine.setProperty('rate', 185)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
if voices:
    engine.setProperty('voice', voices[0].id)

# ---------------- GLOBAL ----------------
mode = "voice"  # default mode
recognizer = sr.Recognizer()
active = False

# ---------------- SPEAK ----------------
def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# ---------------- LISTEN ----------------
def listen():
    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            recognizer.energy_threshold = 250
            recognizer.pause_threshold = 0.8
            recognizer.dynamic_energy_threshold = True
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
            print("⚡ Processing...")
            text = recognizer.recognize_google(audio, language="en-IN")
            text = str(text).lower()
            print("You said:", text)
            return text
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        print("❌ Samajh nahi aaya")
        return ""
    except sr.RequestError:
        print("❌ Internet issue")
        return ""
    except Exception as e:
        print("Voice Error:", e)
        return ""

# ---------------- TIME ----------------
def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")

def greeting():
    now = datetime.datetime.now()
    h = now.hour

    if 5 <= h < 12:
        return "Morning"
    elif 12 <= h < 17:
        return "Afternoon"
    elif 17 <= h < 21:
        return "Evening"
    else:
        return "Night"

# ---------------- STARTUP ----------------
def startup():
    speak("System is online")
    speak(f"Good {greeting()} Min")
    speak(f"Current time is {get_time()}")
    speak("Jarvis is now ready. How can I assist you?")

# ---------------- SHUTDOWN ----------------
def shutdown():
    speak(f"Current time is {get_time()}")
    speak("You have worked well today Min")
    speak("I recommend taking some rest")
    speak("Goodbye Min")

# ---------------- MAIN ----------------
def main():
    global mode, active
    print("Jarvis ready. Say wake up jarvis")
    speak("Jarvis ready. Say wake up jarvis")
    while True:
        # -------- INPUT --------
        if mode == "voice":
            text = listen()
        else:
            try:
                text = input("⌨️ Type: ").lower()
            except:
                text = ""

        if not text:
            continue
        print("You:", text)

        # -------- WAKE --------
        if not active:
            if "jarvis" in text or "wake up" in text:
                active = True
                startup()
            continue

        # -------- MODE SWITCH --------
        if "switch to typing" in text:
            mode = "type"
            speak("Typing mode activated")
            print("Jarvis: Typing mode activated")
            continue
        if "switch to voice" in text:
            mode = "voice"
            speak("Voice mode activated")
            print("Jarvis: Voice mode activated")
            continue

        # -------- EXIT --------
        if any(x in text for x in ["exit", "bye", "shutdown", "stop"]):
            shutdown()
            break

        # -------- COMMAND EXECUTION --------
        try:
            result = execute_command(text)
        except Exception as e:
            print("Command Error:", e)
            result = "error"

        # -------- OUTPUT --------
        if result and result != "not found":
            speak(result)
        else:
            speak("Sorry Min, command samajh nahi aaya")

# ---------------- RUN ----------------
if __name__ == "__main__":
    main()