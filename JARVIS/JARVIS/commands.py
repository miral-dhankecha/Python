import os
import webbrowser
import subprocess
import shutil
import psutil
import time
import requests
from dotenv import load_dotenv

# Load .env for API keys
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# ---------------- STYLE ----------------
def speak_style(msg):
    return f"Yes Min, {msg}"

# ---------------- OPEN PATH ----------------
def open_path(path):
    if os.path.exists(path) or path.rstrip("\\").upper() in ["C:", "D:"]:
        try:
            if path.rstrip("\\").upper() in ["C:", "D:"]:
                subprocess.Popen(f'explorer "{path}"')
            else:
                os.startfile(path)
            name = os.path.basename(path) or path
            return speak_style(f"{name} open kar diya hai")
        except Exception as e:
            return f"Min, {path} open nahi ho paaya: {e}"
    return "Min, path galat hai"

# ---------------- CLOSE PATH (for drives/folders) ----------------
def close_path(path):
    try:
        # Windows limitation: Explorer window cannot be closed individually by path reliably
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == "explorer.exe":
                    proc.kill()
            except:
                pass
        return speak_style(f"{path} windows close karne ki koshish ki")
    except Exception as e:
        return f"Min, close nahi ho paaya: {e}"

# ---------------- CREATE ----------------
def create_item(path):
    try:
        name = os.path.basename(path)
        if "." in name:  # File
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w").close()
        else:  # Folder
            os.makedirs(path, exist_ok=True)

        # Open parent folder in Explorer to show the created item
        parent_folder = os.path.dirname(path) if os.path.isfile(path) else path
        if os.path.exists(parent_folder):
            os.startfile(parent_folder)

        return speak_style(f"{name} create kar diya hai")
    except Exception as e:
        return f"Error: {e}"

# ---------------- DELETE ----------------
def delete_item(path):
    try:
        if not os.path.exists(path):
            return "Min, file ya folder nahi mila"

        name = os.path.basename(path)
        parent_folder = os.path.dirname(path)  # Parent folder to open after deletion

        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            return "Min, file ya folder nahi mila"

        # Open parent folder to show deletion
        if os.path.exists(parent_folder):
            os.startfile(parent_folder)

        return speak_style(f"{name} delete kar diya hai")
    except Exception as e:
        return f"Error: {e}"

# ---------------- WEATHER ----------------
def get_weather(city):
    try:
        base = "http://api.openweathermap.org/data/2.5/weather?"
        url = f"{base}q={city}&appid={WEATHER_API_KEY}&units=metric"
        res = requests.get(url).json()
        if res.get("cod") != 200:
            return f"Min, {city} ka weather nahi mil paaya"
        weather_desc = res["weather"][0]["description"]
        temp = res["main"]["temp"]
        humidity = res["main"]["humidity"]
        return f"{city.title()} me mausam {weather_desc} hai, temperature {temp}°C aur humidity {humidity}% hai."
    except Exception as e:
        return f"Min, weather info nahi mil paaya: {e}"

# ---------------- CLOSE APP ----------------
def close_app_by_name(name):
    name = name.lower()
    exe_map = {
        "chrome": "chrome.exe",
        "edge": "msedge.exe",
        "notepad": "notepad.exe",
        "calculator": "CalculatorApp.exe",
        "paint": "mspaint.exe",
        "word": "WINWORD.EXE",
        "excel": "EXCEL.EXE",
        "powerpoint": "POWERPNT.EXE",
        "outlook": "OUTLOOK.EXE",
        "access": "MSACCESS.EXE",
        "snipping tool": "SnippingTool.exe",
        "visual studio code": "Code.exe",
        "visual studio insider 2026": "devenv.exe",
        "file explorer": "explorer.exe",
        "settings": "SystemSettings.exe",
        "spotify": "Spotify.exe"
    }

    exe_name = exe_map.get(name)
    if not exe_name:
        return "Min, app close nahi ho paaya"

    success = False
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and exe_name.lower() == proc.info['name'].lower():
                proc.kill()
                success = True
        except:
            pass

    if success:
        return speak_style(f"{name} band kar diya hai")
    else:
        return f"Min, {name} running nahi hai"

# ---------------- OPEN APP ----------------
def open_app_by_name(name):
    name = name.lower()
    try:
        if name == "settings":
            subprocess.Popen("explorer ms-settings:", shell=True)
        elif name == "camera":
            subprocess.Popen("start microsoft.windows.camera:", shell=True)
        elif name == "calculator":
            subprocess.Popen("calc.exe")
        elif name == "notepad":
            os.system("start notepad")
        elif name == "paint":
            os.system("start mspaint")
        elif name == "file explorer":
            os.startfile("explorer")
        elif name == "chrome":
            os.system("start chrome")
        elif name == "edge":
            os.system("start msedge")
        elif name == "visual studio code":
            os.system("start code")
        elif name == "visual studio insider 2026":
            os.system("start devenv")
        elif name in ["word", "excel", "powerpoint", "outlook", "access"]:
            ms_map = {
                "word":"winword",
                "excel":"excel",
                "powerpoint":"powerpnt",
                "outlook":"outlook",
                "access":"msaccess"
            }
            os.system(f"start {ms_map[name]}")
        elif name == "microsoft store":
            os.system("start ms-windows-store:")
        elif name == "whatsapp":
            webbrowser.open("https://web.whatsapp.com")
        elif name == "chatgpt":
            webbrowser.open("https://chat.openai.com")
        elif name == "youtube":
            webbrowser.open("https://youtube.com")
        elif name == "gmail":
            webbrowser.open("https://mail.google.com")
        elif name == "spotify":
            os.system("start spotify")
        else:
            return "Min, app open nahi ho paaya"
        return speak_style(f"{name} open kar diya hai")
    except Exception as e:
        return f"Error: {e}"

# ---------------- SEARCH ----------------
def search_query(query):
    query = query.strip()
    webbrowser.open(f"https://www.google.com/search?q={query}")
    return speak_style(f"{query} search kar diya hai")

# ---------------- PLAY ----------------
def play_song(song):
    song = song.strip()
    webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
    return speak_style(f"{song} play kar raha hoon")

# ---------------- EXECUTE COMMAND ----------------
def execute_command(text):
    text = str(text).lower().strip()

    # ----- WEATHER -----
    if "weather" in text:
        city = text.replace("weather", "").strip()
        if city:
            return get_weather(city)
        else:
            return get_weather("Muzaffarpur")  # default city

    # ----- PATH -----  
    if text.startswith("open c:\\") or text.startswith("open d:\\"):
        return open_path(text.replace("open", "").strip())
    if text.startswith("close c:\\") or text.startswith("close d:\\"):
        return close_path(text.replace("close", "").strip())
    if "open path" in text:
        return open_path(text.replace("open path", "").strip())
    if "close path" in text:
        return close_path(text.replace("close path", "").strip())

    # ----- CREATE -----  
    if "create" in text:
        return create_item(text.replace("create", "").strip())

    # ----- DELETE -----  
    if "delete" in text:
        return delete_item(text.replace("delete", "").strip())

    # ----- FOLDERS -----  
    base = os.environ["USERPROFILE"]
    folders = {
        "desktop": os.path.join(base, "Desktop"),
        "downloads": os.path.join(base, "Downloads"),
        "documents": os.path.join(base, "Documents"),
        "videos": os.path.join(base, "Videos"),
        "music": os.path.join(base, "Music"),
    }
    for name, path in folders.items():
        if f"open {name}" in text:
            return open_path(path)
        if f"close {name}" in text:
            return close_path(path)
    
    # ----- OPEN APPS -----  
    app_names = ["chrome","edge","notepad","paint","calculator","word","excel","powerpoint","outlook","access",
                 "settings","camera","file explorer","microsoft store","whatsapp","chatgpt","youtube","gmail",
                 "spotify","visual studio insider 2026","visual studio code"]
    for app in app_names:
        if f"open {app}" in text:
            return open_app_by_name(app)
        if f"close {app}" in text:
            return close_app_by_name(app)

    # ----- SEARCH -----  
    if "search" in text:
        return search_query(text.replace("search", "").strip())

    # ----- PLAY -----  
    if "play" in text:
        return play_song(text.replace("play", "").strip())

    return "not found"