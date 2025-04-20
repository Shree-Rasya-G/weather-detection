import tkinter as tk
from tkinter import ttk, messagebox
import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Replace with your OpenWeatherMap API key
API_KEY = 'e126501c059cfb527e1bec2593a966e6'

def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("City not found or API error.")
    return response.json()

def plot_weather(data):
    temps = []
    times = []

    for entry in data['list'][:8]:  # Show next 24 hours
        temps.append(entry['main']['temp'])
        times.append(datetime.fromtimestamp(entry['dt']).strftime('%H:%M'))

    plt.figure(figsize=(10, 5))
    plt.plot(times, temps, marker='o')
    plt.title('Temperature Trend (Next 24 hours)')
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def show_weather():
    city = city_var.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return
    try:
        data = fetch_weather(city)
        temp = data['list'][0]['main']['temp']
        desc = data['list'][0]['weather'][0]['description']
        humidity = data['list'][0]['main']['humidity']
        wind = data['list'][0]['wind']['speed']

        output = (
            f"City: {city.title()}\n"
            f"Temperature: {temp}°C\n"
            f"Condition: {desc}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind} m/s"
        )
        result_label.config(text=output)
        plot_weather(data)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("Weather Dashboard")
root.geometry("400x300")

city_var = tk.StringVar()

ttk.Label(root, text="Enter City Name:", font=("Arial", 12)).pack(pady=10)
ttk.Entry(root, textvariable=city_var, width=30).pack(pady=5)
ttk.Button(root, text="Get Weather", command=show_weather).pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 11), justify='left')
result_label.pack(pady=10)

root.mainloop()

