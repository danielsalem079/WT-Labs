"""AstroBot coursework – completed from the supplied modular starter code.

Commands: /help, /weather <city>, /iss, /astronauts, /quit.
Install requests: python -m pip install requests
"""

# =========================
# REQUIRED LIBRARIES
# =========================
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
