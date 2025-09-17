from flask import Flask, render_template, jsonify
import http.client
import json

app = Flask(__name__)

# Your Tomorrow.io API key
API_KEY = "NNZFXpCIm72k3do9mKu8SAvhyXgA1kM0"

# Map weatherCode to human-readable condition
WEATHER_CODES = {
    0: "Unknown", 1000: "Clear", 1001: "Cloudy", 1100: "Mostly Clear",
    1101: "Partly Cloudy", 1102: "Mostly Cloudy", 2000: "Fog", 2100: "Light Fog",
    4000: "Drizzle", 4001: "Rain", 4200: "Light Rain", 4201: "Heavy Rain",
    5000: "Snow", 5001: "Flurries", 5100: "Light Snow", 5101: "Heavy Snow",
    8000: "Thunderstorm"
}

def fetch_weather_data(city: str):
    try:
        conn = http.client.HTTPSConnection("api.tomorrow.io", timeout=10)
        path = f"/v4/weather/realtime?location={city}&apikey={API_KEY}&units=metric"
        conn.request("GET", path)
        response = conn.getresponse()
        data = json.loads(response.read().decode())
        conn.close()

        if "code" in data: # Error handling for Tomorrow.io
            return {"error": data.get('message', 'Unable to fetch data')}

        current = data["data"]["values"]
        location = data["location"]["name"]
        condition = WEATHER_CODES.get(current.get("weatherCode", 0), "Unknown")

        weather = {
            "city": location.split(',')[0],
            "temperature": current.get("temperature"),
            "humidity": current.get("humidity"),
            "windSpeed": current.get("windSpeed"),
            "condition": condition
        }
        return weather
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather/<city>')
def get_weather(city):
    weather_data = fetch_weather_data(city)
    if "error" in weather_data:
        return jsonify(weather_data), 404
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True)