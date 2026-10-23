"""AstroBot coursework – completed from the supplied modular starter code.

Commands: /help, /weather <city>, /iss, /astronauts, /quit.
Install requests: python -m pip install requests
"""

# =========================
# REQUIRED LIBRARIES
# =========================
import requests
import json
import time
from datetime import datetime

# =========================
# CONFIGURATION FUNCTIONS
# =========================
def get_webex_token():
    choice = input("Use hard-coded Webex token? (y/n): ").strip().lower()
    if choice == "n":
        token = input("Enter your Webex Access Token: ").strip()
        return f"Bearer {token}"
    else:
        # Do not replace this placeholder with a real token in public GitHub code.
        return "Bearer YOUR_WEBEX_TOKEN"


def get_api_key(prompt, hardcoded_key):
    choice = input(f"Use hard-coded {prompt}? (y/n): ").strip().lower()
    if choice == "n":
        return input(f"Enter {prompt}: ").strip()
    # Do not commit a real API key to GitHub.
    return hardcoded_key


# =========================
# WEBEX FUNCTIONS
# =========================
def get_rooms(token):
    url = "https://webexapis.com/v1/rooms"
    headers = {"Authorization": token}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print("Error fetching rooms:", response.status_code)
            return []
        return response.json().get("items", [])
    except (requests.RequestException, ValueError) as error:
        print("Unable to fetch rooms:", error)
        return []


def print_rooms(rooms):
    for room in rooms:
        print(f"Room: {room.get('title', 'Untitled')} | ID: {room.get('id', '')}")


def select_room(rooms):
    while True:
        name = input("Enter the name of the Webex room: ").strip()
        for room in rooms:
            if name.lower() in room.get("title", "").lower() and name:
                print(f"Selected room: {room['title']}")
                return room["id"]
        print("Room not found. Please try again.")


def get_latest_message(token, room_id):
    url = "https://webexapis.com/v1/messages"
    params = {"roomId": room_id, "max": 1}
    headers = {"Authorization": token}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code != 200:
            print("Error fetching messages:", response.status_code)
            return None, None
        data = response.json().get("items", [])
        if not data:
            return None, None
        latest = data[0]
        return latest.get("id"), latest.get("text", "")
    except (requests.RequestException, ValueError) as error:
        print("Unable to fetch messages:", error)
        return None, None


def send_message(token, room_id, message):
    url = "https://webexapis.com/v1/messages"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {"roomId": room_id, "text": message}
    try:
        response = requests.post(
            url, headers=headers, data=json.dumps(data), timeout=10
        )
        if response.status_code not in (200, 201):
            print("Error sending message:", response.status_code)
    except requests.RequestException as error:
        print("Unable to send message:", error)


# =========================
# WEATHER FUNCTIONS
# =========================
def get_city_coordinates(city, api_key):
    url = "https://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city, "limit": 1, "appid": api_key}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            print("Geocoding API error:", response.status_code)
            return None
        data = response.json()
        return data[0] if data else None
    except (requests.RequestException, ValueError, TypeError, IndexError) as error:
        print("Geocoding request failed:", error)
        return None


def format_weather_message(location, weather):
    """VIEW: turn weather data into readable Webex text."""
    return (
        f"Weather in {location['name']}, {location['country']}:\n"
        f"Temperature: {weather['main']['temp']} °C\n"
        f"Description: {weather['weather'][0]['description']}\n"
        f"Humidity: {weather['main']['humidity']}%\n"
        f"Wind speed: {weather['wind']['speed']} m/s"
    )


def get_weather(city, api_key):
    if not city or len(city) > 80:
        return "Please enter a valid city name (up to 80 characters)."
    location = get_city_coordinates(city, api_key)
    if not location:
        return "City not found or geocoding is unavailable."

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": location["lat"],
        "lon": location["lon"],
        "units": "metric",
        "appid": api_key
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return f"Unable to retrieve weather data (HTTP {response.status_code})."
        weather = response.json()
        return format_weather_message(location, weather)
    except (requests.RequestException, ValueError, KeyError, TypeError, IndexError) as error:
        print("Weather request failed:", error)
        return "Unable to retrieve valid weather data right now."


# =========================
# ISS FUNCTIONS
# =========================
def reverse_geocode(lat, lon, api_key):
    url = "https://api.openweathermap.org/geo/1.0/reverse"
    params = {"lat": lat, "lon": lon, "limit": 1, "appid": api_key}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return None
        data = response.json()
        return data[0] if data else None
    except (requests.RequestException, ValueError, TypeError, IndexError):
        return None


def format_iss_message(lat, lon, place, timestamp):
    """VIEW: turn ISS data into readable Webex text."""
    return (
        f"ISS current position:\n"
        f"Latitude: {lat:.4f}\n"
        f"Longitude: {lon:.4f}\n"
        f"Nearby place: {place}\n"
        f"Recorded: {timestamp}"
    )


def get_iss_location(api_key):
    # The coursework's specified Open Notify provider documents this HTTP URL.
    url = "http://api.open-notify.org/iss-now.json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return f"Unable to retrieve ISS location (HTTP {response.status_code})."
        data = response.json()
        lat = float(data["iss_position"]["latitude"])
        lon = float(data["iss_position"]["longitude"])
        location = reverse_geocode(lat, lon, api_key)
        place = "Over ocean / no nearby named location"
        if location:
            place = f"{location.get('name', 'Unknown')}, {location.get('country', 'Unknown')}"
        timestamp = time.strftime(
            "%d %B %Y at %H:%M:%S UTC", time.gmtime(int(data["timestamp"]))
        )
        return format_iss_message(lat, lon, place, timestamp)
    except (requests.RequestException, ValueError, KeyError, TypeError, OverflowError) as error:
        print("ISS request failed:", error)
        return "Unable to retrieve valid ISS location right now."


# =========================
# EXTENDED FEATURE
# =========================
def get_astronauts():
    """Additional Open Notify API for /astronauts command."""
    url = "http://api.open-notify.org/astros.json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return f"Unable to retrieve astronaut data (HTTP {response.status_code})."
        data = response.json()
        people = data["people"]
        lines = [f"People currently in space: {data['number']}"]
        for person in people:
            lines.append(f"- {person['name']} ({person['craft']})")
        return "\n".join(lines)
    except (requests.RequestException, ValueError, KeyError, TypeError) as error:
        print("Astronaut API request failed:", error)
        return "Unable to retrieve astronaut information right now."


# =========================
# MAIN BOT LOGIC
# =========================
def main():
    token = get_webex_token()
    weather_key = get_api_key("Weather API key", "YOUR_OPENWEATHER_API_KEY")
    rooms = get_rooms(token)
    if not rooms:
        print("No rooms available. Check your Webex token and room membership.")
        return
    print_rooms(rooms)
    room_id = select_room(rooms)
    last_message_id, _ = get_latest_message(token, room_id)

    print(f"AstroBot started at {datetime.now().strftime('%H:%M:%S')}.")
    print("AstroBot is running. Send /help in Webex. Press Ctrl+C to stop.")
    while True:
        message_id, message_text = get_latest_message(token, room_id)
        if message_id and message_id != last_message_id:
            last_message_id = message_id
            message_text = (message_text or "").strip()
            print(f"Received message: {message_text}")
            if not message_text.startswith("/"):
                time.sleep(5)
                continue

            if message_text.lower() == "/help":
                send_message(
                    token,
                    room_id,
                    "/weather <city>\n/iss\n/astronauts\n/help\n/quit"
                )
            elif message_text.lower().startswith("/weather"):
                parts = message_text.split(maxsplit=1)
                if len(parts) < 2 or not parts[1].strip():
                    send_message(token, room_id, "Usage: /weather <city>")
                else:
                    city = parts[1].strip()
                    send_message(token, room_id, get_weather(city, weather_key))
            elif message_text.lower() == "/iss":
                send_message(token, room_id, get_iss_location(weather_key))
            elif message_text.lower() == "/astronauts":
                send_message(token, room_id, get_astronauts())
            elif message_text.lower() == "/quit":
                send_message(token, room_id, "AstroBot shutting down.")
                break
            else:
                send_message(token, room_id, "Unknown command. Use /help")
        time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAstroBot stopped.")
