import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime


API_KEY = "42b7a9ce364506ad44f156d43faba408" 
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
ICON_URL = "http://openweathermap.org/img/wn/{}@2x.png"
IP_URL = "http://ipinfo.io/json"


def auto_detect_location():
    try:
        response = requests.get(IP_URL)
        if response.status_code == 200:
            data = response.json()
            location_entry.delete(0, tk.END)
            location_entry.insert(0, data.get("city", ""))
        else:
            messagebox.showerror("Error", "❗ Unable to detect location.")
    except Exception as e:
        messagebox.showerror("Error", f"❗ Error detecting location: {e}")


def fetch_weather():
    location = location_entry.get().strip()
    units = "metric" if unit_var.get() == "Celsius" else "imperial"

    if not location:
        messagebox.showerror("Error", "❗ Please enter a location.")
        return

    params = {"q": location, "units": units, "appid": API_KEY}
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        display_weather(data, units)
    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "❗ Network error. Please check your internet connection.")
    except Exception as e:
        messagebox.showerror("Error", f"❗ Unable to fetch weather data: {e}")


def display_weather(data, units):
    city = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather = data["weather"][0]["description"].capitalize()
    wind_speed = data["wind"]["speed"]
    timestamp = datetime.fromtimestamp(data["dt"]).strftime("%Y-%m-%d %H:%M:%S")
    icon_code = data["weather"][0]["icon"]

   
    location_label.config(text=f"{city}, {country}")
    temp_label.config(text=f"Temperature: {temp}°{'C' if units == 'metric' else 'F'}")
    humidity_label.config(text=f"Humidity: {humidity}%")
    weather_label.config(text=f"Weather: {weather}")
    wind_label.config(text=f"Wind Speed: {wind_speed} m/s")
    time_label.config(text=f"Last updated: {timestamp}")

    
    icon_response = requests.get(ICON_URL.format(icon_code))
    icon_image = Image.open(BytesIO(icon_response.content)).resize((100, 100), Image.LANCZOS)
    icon_photo = ImageTk.PhotoImage(icon_image)
    icon_label.config(image=icon_photo)
    icon_label.image = icon_photo


root = tk.Tk()
root.title("🌤️ Enhanced Weather App")
root.geometry("350x400")


tk.Label(root, text="Enter city name or ZIP code:").pack(pady=5)
location_entry = tk.Entry(root, width=30)
location_entry.pack(pady=5)

unit_var = tk.StringVar(value="Celsius")
tk.Radiobutton(root, text="Celsius", variable=unit_var, value="Celsius").pack(anchor="w", padx=50)
tk.Radiobutton(root, text="Fahrenheit", variable=unit_var, value="imperial").pack(anchor="w", padx=50)


tk.Button(root, text="Get Weather", command=fetch_weather).pack(pady=5)
tk.Button(root, text="Auto Detect Location", command=auto_detect_location).pack(pady=5)


location_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
location_label.pack(pady=5)

icon_label = tk.Label(root)
icon_label.pack(pady=5)

temp_label = tk.Label(root, text="")
temp_label.pack()

humidity_label = tk.Label(root, text="")
humidity_label.pack()

weather_label = tk.Label(root, text="")
weather_label.pack()

wind_label = tk.Label(root, text="")
wind_label.pack()

time_label = tk.Label(root, text="", font=("Arial", 8))
time_label.pack(pady=5)

root.mainloop()
