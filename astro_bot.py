"""AstroBot coursework – completed from the supplied modular starter code.

Commands: /help, /weather <city>, /iss, /astronauts, /quit.
Install requests: python -m pip install requests
"""
import requests
import json
import time
from datetime import datetime


def get_webex_token():
    choice = input("Use hard-coded Webex token? (y/n): ").strip().lower()
    if choice == "n":
        token = input("Enter your Webex Access Token: ").strip()
        return f"Bearer {token}"
    return "Bearer YOUR_WEBEX_TOKEN"


def get_api_key(prompt, hardcoded_key):
    choice = input(f"Use hard-coded {prompt}? (y/n): ").strip().lower()
    if choice == "n":
        return input(f"Enter {prompt}: ").strip()
    return hardcoded_key


# Webex functions

def get_rooms(token):
    url = "https://webexapis.com/v1/rooms"
    headers = {"Authorization": token}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print("Error fetching rooms:", response.status_code)
            return []
        return response.json().get("items", [])
    except (requests.RequestException, ValueError):
        print("Could not fetch rooms.")
        return []


def print_rooms(rooms):
    for room in rooms:
        print(f"{room['title']} - {room['id']}")


def select_room(rooms):
    while True:
        name = input("Enter room name: ").strip().lower()
        for room in rooms:
            if name and name in room["title"].lower():
                print("Selected room:", room["title"])
                return room["id"]
        print("Room not found. Try again.")


def get_latest_message(token, room_id):
    url = "https://webexapis.com/v1/messages"
    headers = {"Authorization": token}
    params = {"roomId": room_id, "max": 1}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code != 200:
            print("Error fetching messages:", response.status_code)
            return None, None
        messages = response.json().get("items", [])
        if not messages:
            return None, None
        return messages[0].get("id"), messages[0].get("text", "")
    except (requests.RequestException, ValueError):
        print("Could not fetch messages.")
        return None, None


def send_message(token, room_id, message):
    url = "https://webexapis.com/v1/messages"
    headers = {"Authorization": token, "Content-Type": "application/json"}
    data = {"roomId": room_id, "text": message}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=10)
        if response.status_code not in (200, 201):
            print("Error sending message:", response.status_code)
    except requests.RequestException:
        print("Could not send message.")


# Weather functions

def get_city_coordinates(city, api_key):
    url = "https://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city, "limit": 1, "appid": api_key}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return None
        locations = response.json()
        return locations[0] if locations else None
    except (requests.RequestException, ValueError, TypeError, IndexError):
        return None


def format_weather_message(location, weather):
    return (
        f"Weather in {location['name']}, {location['country']}:\n"
        f"Temperature: {weather['main']['temp']} °C\n"
        f"Description: {weather['weather'][0]['description']}\n"
        f"Humidity: {weather['main']['humidity']}%\n"
        f"Wind speed: {weather['wind']['speed']} m/s"
    )


def get_weather(city, api_key):
    if not city or len(city) > 80:
        return "Please enter a valid city name."

    location = get_city_coordinates(city, api_key)
    if not location:
        return "City not found or geocoding unavailable."

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
            return "Could not get weather information."
        return format_weather_message(location, response.json())
    except (requests.RequestException, ValueError, KeyError, TypeError, IndexError):
        return "Could not get weather information."
        return "Could not get weather information."


# ISS functions

def reverse_geocode(lat, lon, api_key):
    url = "https://api.openweathermap.org/geo/1.0/reverse"
    params = {"lat": lat, "lon": lon, "limit": 1, "appid": api_key}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return None
        locations = response.json()
        return locations[0] if locations else None
    except (requests.RequestException, ValueError, TypeError, IndexError):
        return None


def format_iss_message(lat, lon, place, timestamp):
    return (
        f"ISS current position:\n"
        f"Latitude: {lat:.4f}\n"
        f"Longitude: {lon:.4f}\n"
        f"Nearby place: {place}\n"
        f"Recorded: {timestamp}"
    )


def get_iss_location(api_key):
    url = "http://api.open-notify.org/iss-now.json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return "Could not get ISS location."

        data = response.json()
        lat = float(data["iss_position"]["latitude"])
        lon = float(data["iss_position"]["longitude"])
        location = reverse_geocode(lat, lon, api_key)

        place = "Over ocean / no nearby city"
        if location:
            place = f"{location['name']}, {location['country']}"

        timestamp = time.strftime(
            "%d %B %Y at %H:%M:%S UTC", time.gmtime(int(data["timestamp"]))
        )
        return format_iss_message(lat, lon, place, timestamp)
    except (requests.RequestException, ValueError, KeyError, TypeError, OverflowError):
        return "Could not get ISS location."


# Extra command

def get_astronauts():
    url = "http://api.open-notify.org/astros.json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return "Could not get astronaut information."

        data = response.json()
        lines = [f"People currently in space: {data['number']}"]
        for person in data["people"]:
            lines.append(f"{person['name']} - {person['craft']}")
        return "\n".join(lines)
    except (requests.RequestException, ValueError, KeyError, TypeError):
        return "Could not get astronaut information."


# Main program

def main():
    token = get_webex_token()
    weather_key = get_api_key("Weather API key", "YOUR_OPENWEATHER_API_KEY")
    rooms = get_rooms(token)

    if not rooms:
        print("No rooms found. Check your Webex token.")
        return

    print_rooms(rooms)
    room_id = select_room(rooms)
    last_message_id, _ = get_latest_message(token, room_id)
    print(f"AstroBot started at {datetime.now().strftime('%H:%M:%S')}")

    while True:
        message_id, message_text = get_latest_message(token, room_id)

        if message_id and message_id != last_message_id:
            last_message_id = message_id
            message_text = (message_text or "").strip()
            print("Message:", message_text)

            if message_text.startswith("/"):
                command = message_text.lower()

                if command == "/help":
                    send_message(token, room_id,
                                 "Commands:\n/weather <city>\n/iss\n/astronauts\n/help\n/quit")
                elif command == "/weather" or command.startswith("/weather "):
                    parts = message_text.split(maxsplit=1)
                    if len(parts) < 2:
                        send_message(token, room_id, "Usage: /weather <city>")
                    else:
                        send_message(token, room_id, get_weather(parts[1].strip(), weather_key))
                elif command == "/iss":
                    send_message(token, room_id, get_iss_location(weather_key))
                elif command == "/astronauts":
                    send_message(token, room_id, get_astronauts())
                elif command == "/quit":
                    send_message(token, room_id, "AstroBot shutting down.")
                    break
                else:
                    send_message(token, room_id, "Unknown command. Use /help")

        time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("AstroBot stopped.")
