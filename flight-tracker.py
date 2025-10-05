import requests
import folium
import threading
import time
from flask import Flask, send_file

# OpenSky API URL for live flights
URL = "https://opensky-network.org/api/states/all"

# Flask app to serve the flight map
app = Flask(__name__)

def fetch_flight_data():
    """Fetch flight data from OpenSky Network API."""
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json().get("states", [])
    return []

def plot_flights():
    """Fetch flights and generate an updated map."""
    while True:
        flights = fetch_flight_data()
        flight_map = folium.Map(location=[37.7749, -98.4194], zoom_start=4)

        for flight in flights[:50]:  # Limit to first 50 flights
            callsign = flight[1]  # Flight callsign
            latitude = flight[6]   # Latitude
            longitude = flight[5]  # Longitude
            altitude = flight[13]  # Altitude in meters

            if latitude and longitude:
                folium.Marker(
                    [latitude, longitude],
                    popup=f"Flight: {callsign}\nAltitude: {altitude}m",
                    icon=folium.Icon(color="blue", icon="plane", prefix="fa")
                ).add_to(flight_map)

        flight_map.save("flights.html")
        print("Map updated.")
        time.sleep(60)  # Refresh every minute

# Background thread for live tracking
threading.Thread(target=plot_flights, daemon=True).start()

@app.route("/")
def serve_map():
    """Serve the live flight map."""
    return send_file("flights.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
