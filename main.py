import http.client
import json
import time
import matplotlib.pyplot as plt
from datetime import datetime

# Tomorrow.io API key
API_KEY = "NNZFXpCIm72k3do9mKu8SAvhyXgA1kM0"

# Map weatherCode to human-readable condition
WEATHER_CODES = {
    0: "Unknown",
    1000: "Clear",
    1001: "Cloudy",
    1100: "Mostly Clear",
    1101: "Partly Cloudy",
    1102: "Mostly Cloudy",
    2000: "Fog",
    2100: "Light Fog",
    3000: "Light Wind",
    3001: "Wind",
    3002: "Strong Wind",
    4000: "Drizzle",
    4001: "Rain",
    4200: "Light Rain",
    4201: "Heavy Rain",
    5000: "Snow",
    5001: "Flurries",
    5100: "Light Snow",
    5101: "Heavy Snow",
    6000: "Freezing Drizzle",
    6001: "Freezing Rain",
    6200: "Light Freezing Rain",
    6201: "Heavy Freezing Rain",
    7000: "Ice Pellets",
    7101: "Heavy Ice Pellets",
    7102: "Light Ice Pellets",
    8000: "Thunderstorm"
}

def fetch_weather(city: str):
    try:
        conn = http.client.HTTPSConnection("api.tomorrow.io", timeout=10)
        path = f"/v4/weather/realtime?location={city}&apikey={API_KEY}"
        conn.request("GET", path)
        response = conn.getresponse()
        data = response.read().decode()
        conn.close()

        data = json.loads(data)
        # Debug
        print("DEBUG API RESPONSE:", data)

        if "error" in data:
            print(f"Error: {data['error'].get('message', 'Unable to fetch data')}")
            return None

        current = data["data"]["values"]

        condition = WEATHER_CODES.get(current.get("weatherCode", 0), "Unknown")

        weather = {
            "City": city,
            "Temperature (°C)": current.get("temperature"),
            "Humidity (%)": current.get("humidity"),
            "Wind Speed (m/s)": current.get("windSpeed"),
            "Condition": condition
        }
        return weather

    except Exception as e:
        print(f"Error: {e}")
        return None

def display_weather(weather: dict):
    print("\n🌦 Weather Report")
    print("-" * 30)
    for key, value in weather.items():
        print(f"{key:20}: {value}")
    print("-" * 30)

if __name__ == "__main__":
    city = input("Enter a city name: ").strip()

    times, temps = [], []
    plt.ion()
    fig, ax = plt.subplots()

    while True:
        weather = fetch_weather(city)
        if weather:
            display_weather(weather)

            times.append(datetime.now().strftime("%H:%M:%S"))
            temps.append(weather["Temperature (°C)"])

            times, temps = times[-10:], temps[-10:]

            ax.clear()
            ax.plot(times, temps, marker="o", linestyle="-", color="tab:blue")
            ax.set_title(f"Live Temperature in {city}")
            ax.set_xlabel("Time")
            ax.set_ylabel("Temperature (°C)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.pause(1)

        time.sleep(10)

        print("Weather is good")


