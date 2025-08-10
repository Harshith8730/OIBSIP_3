import requests
import tkinter as tk
from tkinter import messagebox


# Replace with your actual API key
API_KEY = "YOUR_API_KEY_HERE"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
GEOLOCATION_URL = "http://ip-api.com/json"


def get_location_by_ip():
    """
    Fetches the user's city name using their IP address.
    """
    try:
        response = requests.get(GEOLOCATION_URL)
        response.raise_for_status()
        location_data = response.json()
        if location_data['status'] == 'success':
            return location_data['city']
    except requests.exceptions.RequestException:
        return None


def fetch_weather(city):
    """
    Fetches weather data for a given city and returns it.
    """
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return None
    
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    
    try:
        response = requests.get(WEATHER_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            messagebox.showerror("Error", "City not found. Please try again.")
        elif e.response.status_code == 401:
            messagebox.showerror("Error", "Invalid API key or key not activated. Please check your key.")
        else:
            messagebox.showerror("Error", f"HTTP Error: {e.response.status_code}")
    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Could not connect to the weather service. Check your internet connection.")
    return None


def update_weather_display(weather_data):
    """
    Updates the GUI labels with the new weather data.
    """
    if weather_data and weather_data.get('cod') == 200:
        city = weather_data['name']
        country = weather_data['sys']['country']
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']

        city_label.config(text=f"Weather in {city}, {country}")
        temp_label.config(text=f"Temperature: {temp}°C")
        humidity_label.config(text=f"Humidity: {humidity}%")
        desc_label.config(text=f"Description: {description.capitalize()}")
    else:
        # Clear the display if data is invalid
        city_label.config(text="")
        temp_label.config(text="")
        humidity_label.config(text="")
        desc_label.config(text="")


def on_search():
    """
    Function to be called when the Search button is clicked.
    """
    city = city_entry.get().strip()
    weather_data = fetch_weather(city)
    update_weather_display(weather_data)


def on_auto_detect():
    """
    Function to be called when the 'Use Current Location' button is clicked.
    """
    city = get_location_by_ip()
    if city:
        city_entry.delete(0, tk.END)
        city_entry.insert(0, city)
        on_search()
    else:
        messagebox.showerror("Error", "Could not detect your location.")


# --- GUI Setup ---
root = tk.Tk()
root.title("Python Weather App")
root.geometry("400x300")
root.config(bg="#f0f0f0")


# Frame for the input section
input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=10)

# City entry field
city_label_text = tk.Label(input_frame, text="Enter City Name or Use Current Location:", bg="#f0f0f0")
city_label_text.pack(side=tk.LEFT, padx=5)
city_entry = tk.Entry(input_frame, width=20)
city_entry.pack(side=tk.LEFT, padx=5)

# Buttons
search_button = tk.Button(root, text="Search", command=on_search)
search_button.pack(pady=5)
auto_detect_button = tk.Button(root, text="Use Current Location", command=on_auto_detect)
auto_detect_button.pack(pady=5)

# Frame for displaying weather results
result_frame = tk.Frame(root, bg="#f0f0f0")
result_frame.pack(pady=10)

# Weather display labels
city_label = tk.Label(result_frame, text="", font=("Arial", 16, "bold"), bg="#f0f0f0")
city_label.pack(pady=2)
temp_label = tk.Label(result_frame, text="", font=("Arial", 12), bg="#f0f0f0")
temp_label.pack(pady=2)
humidity_label = tk.Label(result_frame, text="", font=("Arial", 12), bg="#f0f0f0")
humidity_label.pack(pady=2)
desc_label = tk.Label(result_frame, text="", font=("Arial", 12), bg="#f0f0f0")
desc_label.pack(pady=2)


root.mainloop()