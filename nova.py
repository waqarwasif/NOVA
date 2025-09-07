from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pyttsx3, wikipedia, pyjokes, psutil, os, requests, google.generativeai as genai, webbrowser

genai.configure(api_key="AIzaSyAA2lq7nGaM65JY-X3Dx50Bc3U75sjuDGk")
WEATHER_API_KEY = "DX6HWG2UJREYCSUM2YW2D9U5C"
NEWS_API_KEY = "pub_f6194951aff54d578686f24a6c15d7d4"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Command(BaseModel):
    text: str


def ask_gpt(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Answer briefly:\n{prompt}")
        return response.text
    except Exception as e:
        return f"Sorry, Gemini failed. {e}"


def get_weather(city):
    try:
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={WEATHER_API_KEY}&contentType=json"
        data = requests.get(url, timeout=10).json()
        today = data["days"][0]
        return f"Weather in {city.title()}: {today['conditions']}, {today['temp']}°C, feels like {today['feelslike']}°C."
    except:
        return "Couldn't fetch weather."


def gen_news(): 
    try: 
        url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&country=pk&language=en"
        data = requests.get(url, timeout=8).json()
        articles = data.get("results", [])[:3]
        headlines = [a.get("title") for a in articles if a.get("title")]
        return (
            "Top headlines: " + ". ".join(headlines) if headlines else "No news found."
        )
    except:
        return "News fetch failed."



def get_battery_status():
    battery = psutil.sensors_battery()
    if not battery:
        return "Battery info not available"
    return (
        f"Battery at {battery.percent}% and charging."
        if battery.power_plugged
        else f"Battery at {battery.percent}%."
    )


def open_app(app_name):
    try:
        if "notepad" in app_name:
            os.startfile("C:\\Windows\\system32\\notepad.exe")
        elif "vs code" in app_name:
            os.startfile(
                "C:\\Users\\usman electronics\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            )
        return f"Opening {app_name}"
    except:
        return f"Cannot open {app_name}."


@app.post("/command")
def handle_command(command: Command):
    text = command.text.lower()

    if "your name" in text:
        return {"reply": "My name is NOVA."}
    elif "who are you" in text:
        return {"reply": "I am NOVA, your personal assistant."}
    elif "time" in text or "date" in text:
        # Fetch online date/time from GPT
        return {
            "reply": ask_gpt(
                "Tell me the current date and time in DD-MM-YYYY HH:MM:SS format"
            )
        }
    elif "joke" in text:
        return {"reply": pyjokes.get_joke()}
    elif "wikipedia" in text:
        query = text.replace("wikipedia", "").strip()
        try:
            return {"reply": wikipedia.summary(query, sentences=2)}
        except:
            return {"reply": "Couldn't find information on that topic."}
    elif "weather" in text:
        city = text.replace("weather", "").strip()
        return {"reply": get_weather(city)}
    elif "news" in text:
        return {"reply": gen_news()}
    elif "battery" in text:
        return {"reply": get_battery_status()}
    elif "notepad" in text or "vs code" in text:
        return {"reply": open_app(text)}
    elif "youtube" in text:
        webbrowser.open("https://www.youtube.com")
        return {"reply": "Opening YouTube"}
    elif "google" in text:
        webbrowser.open("https://www.google.com")
        return {"reply": "Opening Google"}
    elif "who made you" in text or "creator" in text:
        return {"reply": "I was created by Waqar Wasif."}
    elif "exit" in text or "quit" in text or "stop" in text or "bye" in text:
        return {"reply": "Goodbye!"}
    else:
        return {"reply": ask_gpt(text)}
