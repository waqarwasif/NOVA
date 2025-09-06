import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import wikipedia
import os
import time
import pyjokes
import psutil
import requests
import google.generativeai as genai
 
genai.configure(api_key="AIzaSyAA2lq7nGaM65JY-X3Dx50Bc3U75sjuDGk")
WEATHER_API_KEY = "DX6HWG2UJREYCSUM2YW2D9U5C"
NEWS_API_KEY = "pub_f6194951aff54d578686f24a6c15d7d4"
 

def ask_gpt(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"Answer briefly in 3-4 sentences maximum. Keep it short and clear:\n\n{prompt}"
        )
        return response.text
    except Exception as e:
        return f"Sorry, I couldn't get an answer from Gemini. {e}"


def get_battery_status():
    battery = psutil.sensors_battery()
    if battery is None:
        return "Battery information not available"
    percent = battery.percent
    return (
        f"Battery is at {percent}% and charging."
        if battery.power_plugged
        else f"Battery is at {percent}%."
    )


def get_weather(city):
    try:
        if not WEATHER_API_KEY or WEATHER_API_KEY == "DX6HWG2UJREYCSUM2YW2D9U5C":
            return "Weather API key not configured."
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={WEATHER_API_KEY}&contentType=json"
        r = requests.get(url, timeout=10)
        data = r.json()
        if isinstance(data, dict) and "days" in data and data["days"]:
            today = data["days"][0]
            temp = today.get("temp")
            cond = today.get("conditions")
            feels = today.get("feelslike")
            return f"Weather in {city.title()}: {cond}, {temp}°C, feels like {feels}°C."
        return "Couldn't fetch weather for that location."
    except Exception as e:
        return f"Weather service error: {e}"


def search_wikipedia(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except Exception:
        return "Sorry, I couldn't find information on that topic."


def gen_news():
    try:
        if not NEWS_API_KEY or NEWS_API_KEY == "pub_f6194951aff54d578686f24a6c15d7d4":
            return "News API key not configured."
        url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&country=pk&language=en"
        response = requests.get(url, timeout=8)
        data = response.json()
        if "results" not in data:
            return "Sorry, I couldn't fetch the news right now."
        articles = data["results"][:3]
        headlines = [a.get("title") for a in articles if a.get("title")]
        return "Top headlines: " + ". ".join(headlines)
    except Exception as e:
        return f"News service error: {e}"


def speechtxt(text):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        if voices:
            engine.setProperty("voice", voices[0].id)
        engine.setProperty("rate", 125)
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass


def speech_to_text(timeout=8, phrase_time_limit=15):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("NOVA is listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1.2)
        try:
            audio = recognizer.listen(
                source, timeout=timeout, phrase_time_limit=phrase_time_limit
            )
            print("NOVA is recognizing...")
            text = recognizer.recognize_google(audio, language="en-in")
            return text
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase.")
            return None
        except sr.UnknownValueError:
            print("Could not understand, try again.")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition network error: {e}")
            return None
        except Exception as e:
            print(f"Unknown microphone error: {e}")
            return None


if __name__ == "__main__":
    speechtxt("Hello, I am NOVA. I am ready.")
    while True:
        data = speech_to_text(timeout=8, phrase_time_limit=15)
        if not data:
            time.sleep(1)
            continue
        print(f"You said: {data}")
        command = data.lower().strip()

        if "your name" in command:
            reply = "My name is NOVA."
            print(reply)
            speechtxt(reply)

        elif "who are you" in command:
            reply = "I am NOVA, your personal assistant."
            print(reply)
            speechtxt(reply)

        elif "how old are you" in command or "your age" in command:
            reply = "I was designed in 2025, so I am less than a year old."
            print(reply)
            speechtxt(reply)

        elif "time" in command and len(command.split()) <= 3:
            reply = datetime.datetime.now().strftime("The current time is %H:%M:%S %p")
            print(reply)
            speechtxt(reply)

        elif "date" in command and len(command.split()) <= 3:
            reply = datetime.datetime.now().strftime("Today's date is %d-%m-%Y")
            print(reply)
            speechtxt(reply)

        elif "youtube" in command:
            reply = "Opening YouTube"
            print(reply)
            speechtxt(reply)
            webbrowser.open("https://www.youtube.com")

        elif "google" in command:
            reply = "Opening Google"
            print(reply)
            speechtxt(reply)
            webbrowser.open("https://www.google.com")

        elif "joke" in command or "jokes" in command:
            reply = pyjokes.get_joke()
            print(reply)
            speechtxt(reply)

        elif "notepad" in command:
            reply = "Opening Notepad"
            print(reply)
            speechtxt(reply)
            os.startfile("C:\\Windows\\system32\\notepad.exe")

        elif "vs code" in command or "visual studio code" in command:
            reply = "Opening Visual Studio Code"
            print(reply)
            speechtxt(reply)
            try:
                os.startfile(
                    "C:\\Users\\usman electronics\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                )
            except Exception:
                pass

        elif "battery" in command:
            reply = get_battery_status()
            print(reply)
            speechtxt(reply)

        elif "wikipedia" in command:
            q = command.replace("wikipedia", "").strip()
            if not q:
                print("Please say the topic after 'wikipedia'.")
                speechtxt("Please say the topic after wikipedia.")
            else:
                reply = search_wikipedia(q)
                print("According to Wikipedia:")
                print(reply)
                speechtxt(reply)

        elif "search" in command:
            speechtxt("What do you want to search for?")
            query = speech_to_text(timeout=8, phrase_time_limit=12)
            if query:
                print(f"Searching Google for: {query}")
                webbrowser.open(f"https://www.google.com/search?q={query}")
                speechtxt(f"Here are the results for {query}")
            else:
                speechtxt("I didn't catch that search query.")

        elif "who made you" in command or "creator" in command:
            reply = "I was created by Waqar Wasif."
            print(reply)
            speechtxt(reply)

        elif "news" in command or "headlines" in command:
            reply = gen_news()
            print(reply)
            speechtxt(reply)

        elif (
            "meaning of" in command or "define" in command or "definition of" in command
        ):
            word = (
                command.replace("meaning of", "")
                .replace("define", "")
                .replace("definition of", "")
                .strip()
            )
            if not word:
                speechtxt("Please say the word you want to define.")
                print("No word detected for definition.")
            else:
                reply = ask_gpt(
                    f"Explain the meaning of the word '{word}' in one or two simple sentences."
                )
                print("")
                print(reply)
                speechtxt(reply)

        elif "weather" in command:
            city = command.replace("weather", "").strip()
            if not city:
                speechtxt("Please say the city name for weather.")
                print("City not provided for weather.")
            else:
                reply = get_weather(city)
                print(reply)
                speechtxt(reply)

        elif (
            "exit" in command
            or "quit" in command
            or "stop" in command
            or "bye" in command
        ):
            reply = "Thanks for using me. Goodbye."
            print(reply)
            speechtxt(reply)
            break

        else:
            reply = ask_gpt(command)
            print("")
            print(reply)
            speechtxt(reply)

        time.sleep(1)
 