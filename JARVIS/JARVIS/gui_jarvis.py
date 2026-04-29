import customtkinter as ctk
import threading
import time
import speech_recognition as sr
import pyttsx3
from automation.commands import execute_command
from datetime import datetime

# ---------------- TIME FUNCTION ----------------
def get_time():
    return datetime.now().strftime("%I:%M %p")

def greeting():
    h = datetime.now().hour

    if 5 <= h < 12:
        return "Morning"
    elif 12 <= h < 17:
        return "Afternoon"
    elif 17 <= h < 21:
        return "Evening"
    else:
        return "Night"

# ---------------- APP ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.title("JARVIS AI")
app.geometry("700x500")

# ---------------- GLOBAL ----------------
mode = "voice"
active = False
voice_lock = threading.Lock()

# ---------------- CHAT BOX ----------------
chat_frame = ctk.CTkTextbox(app, wrap="word", font=("Consolas", 14))
chat_frame.pack(padx=10, pady=10, fill="both", expand=True)

# ---------------- INPUT ----------------
entry = ctk.CTkEntry(app, placeholder_text="Type command and press Enter...")
entry.pack(padx=10, pady=10, fill="x")

# ---------------- SPEECH ENGINE ----------------
engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
if voices:
    engine.setProperty('voice', voices[0].id)

def speak(text):
    with voice_lock:
        engine.say(str(text))
        engine.runAndWait()

# ---------------- TEXT ANIMATION ----------------
def animate_text(text):
    chat_frame.insert("end", "Jarvis: ")
    for c in text:
        chat_frame.insert("end", c)
        chat_frame.update()
        time.sleep(0.01)
    chat_frame.insert("end", "\n\n")
    chat_frame.see("end")

def show_user(text):
    chat_frame.insert("end", f"You: {text}\n")
    chat_frame.see("end")

def speak_and_show(text):
    animate_text(text)
    speak(text)

# ---------------- MICROPHONE ----------------
recognizer = sr.Recognizer()
mic = None

def init_microphone():
    global mic
    try:
        mic = sr.Microphone()
    except:
        mic = None

def listen():
    global mic
    if mic is None:
        init_microphone()
        if mic is None:
            return ""

    try:
        with mic as source:
            recognizer.energy_threshold = 300
            recognizer.pause_threshold = 0.7
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)

        text = recognizer.recognize_google(audio, language="en-IN")
        return str(text).lower()

    except:
        return ""

# ---------------- COMMAND PROCESS ----------------
def process_command(raw_text):
    global active, mode

    text = str(raw_text).lower()
    show_user(text)

    # WAKE UP
    if not active:
        if "jarvis" in text or "wake up" in text:
            active = True
            speak_and_show("System is online")
            speak_and_show(f"Good {greeting()} Min")   # ✅ FIXED
            speak_and_show(f"Current time is {get_time()}")  # ✅ Added
            speak_and_show("Jarvis is ready")
            speak_and_show("How can I assist you?")
        return

    # MODE SWITCH
    if "switch to typing" in text:
        mode = "type"
        speak_and_show("Typing mode activated")
        return

    if "switch to voice" in text:
        mode = "voice"
        speak_and_show("Voice mode activated")
        return

    # EXIT
    if any(x in text for x in ["exit", "bye", "shutdown", "stop"]):
        speak_and_show(f"Current time is {get_time()}")
        speak_and_show("You have worked well today Min")
        speak_and_show("I recommend taking some rest")
        speak_and_show("Goodbye Min")
        app.after(3000, app.destroy)
        return

    # EXECUTE COMMAND
    try:
        result = execute_command(text)

        if isinstance(result, (list, tuple)):
            result = " ".join(map(str, result))
        elif not isinstance(result, str):
            result = str(result)

    except:
        result = ""

    if result and result != "not found":
        speak_and_show(result)
    else:
        speak_and_show("Sorry Min, I did not understand")

# ---------------- ENTER KEY ----------------
def on_enter(event):
    text = entry.get()
    entry.delete(0, "end")
    threading.Thread(target=process_command, args=(text,), daemon=True).start()

entry.bind("<Return>", on_enter)

# ---------------- VOICE LOOP ----------------
def voice_loop():
    global mode
    while True:
        if mode == "voice":
            text = listen()
            if text:
                app.after(0, lambda t=text: threading.Thread(
                    target=process_command, args=(t,), daemon=True).start())
        time.sleep(0.5)

threading.Thread(target=voice_loop, daemon=True).start()

# ---------------- START MESSAGE ----------------
def startup_message():
    speak_and_show("Jarvis ready. Say wake up Jarvis")  # ✅ voice + text

app.after(1000, startup_message)  # ✅ FIXED (important)

# ---------------- RUN ----------------
app.mainloop()