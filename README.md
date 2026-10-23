# 🚀 Space Bot API Investigation Sheet
**Total Marks: 40**https://github.com/danielsalem079/WT-Labs/blob/main/README.md
**TASK 1: Collect Required API Documentation**
This investigation sheet helps you gather key technical information from the three
APIs required for the Space Bot project: **Webex Messaging API**, **ISS Current
Location API**, **Weather API** and a **Geocoding API** , plus the Python time
module. Also furhter investigate the application of Web Architecture and MVC design
pattern in development of the Bot
---
## Webex Messaging API (4 marks)
| Criteria | Details |
|---------|---------|
| API Base URL | `https://webexapis.com/v1` |
| Authentication Method | `BEARER token` |
| Endpoint to list rooms | `https://webexapis.com/v1/rooms` |
| Endpoint to get messages | `https://webexapis.com/v1/messages/{messageId}` |
| Endpoint to send message | `https://webexapis.com/v1/messages` |
| Required headers | `Authorization: Bearer YOUR_ACCESS_TOKEN Content-Type: application/json` |
| Sample full GET or POST request | `_______________________________` |
---
## ISS Current Location API (2 marks)
| Criteria | Details |
|---------|---------|
| API Base URL | `http://api.open-notify.org` |
| Endpoint for current ISS location | `http://api.open-notify.org/iss-now.json` |
| Sample response format (example JSON) |
{
  "message": "success",
  "timestamp": 1735689600,
  "iss_position": {
    "latitude": "51.5000",
    "longitude": "-0.1200"
  }
}
```
```
|
---
## Geocoding API (4 marks)
| Criteria | Details |
|---------|---------|
| Provider used (Choose one) | **OpenWeatherMap for both forward and reverse geocoding -provide
detail** |
| API Base URL | `https://api.openweathermap.org/geo/1.0` |
| Endpoint for geocoding | `/direct` |
| Endpoint for reverse geocoding | `/reverse` |
| Authentication method | `_______________________________` |
| Required query parameters | `Direct: q, appid. Reverse: lat, lon, appid` |
| Sample request with latitude/longitude | `_______________________________` |
| Sample JSON response (formatted example) |
```
```
|
---
## Weather API (3 marks)
| Criteria | Details |
|---------|---------|
| API Provider (Choose one) | **OpenWeather, OpenWeatherMap (or other – provide
details)** |
| API Base URL | `https://api.openweathermap.org/data/2.5` |
| Endpoint for current weather | ^https://api.openweathermap.org/data/2.5/weather` |
| Authentication method | API key using appid` |
| Required query parameters | `lat, lon, appid` |
| Sample JSON response (formatted example) |GET https://api.openweathermap.org/data/2.5/weather?lat=51.5074&lon=-0.1278&units=metric&appid=YOUR_API_KEY
```
{
  "name": "London",
  "weather": [
    {
      "main": "Clouds",
      "description": "scattered clouds"
    }
  ],
  "main": {
    "temp": 15.5,
    "humidity": 70
  },
  "wind": {
    "speed": 3.2
  },
  "cod": 200
}
```
|
---
## Epoch to Human Time Conversion (Python time module) (2 marks)
| Criteria | Details |
|---------|---------|
| Library used | `Python built-in time module` |
| Function used to convert epoch | `time.gmtime() and time.strftime()` |
| Sample code to convert timestamp |1735689600
```
import time

timestamp = 1735689600

human_time = time.strftime(
    "%d %B %Y at %H:%M:%S UTC",
    time.gmtime(timestamp)
)

print(human_time)
```
|
| Output (human-readable time) | `01 January 2025 at 00:00:00 UTC` |
---
## Extended Feature API ( 3 marks)
| Criteria | Details |
|---------|---------|
| API Provider | 'Open Notify — People in Space API' |
| API Base URL | `http://api.open-notify.org` |
| Endpoint | `http://api.open-notify.org/astros.json` |
| Authentication method | `None required` |
| Required query parameters | `None` |
| Sample JSON response (formatted example) |
```
{
  "message": "success",
  "number": 2,
  "people": [
    {
      "name": "Example Astronaut A",
      "craft": "ISS"
    },
    {
      "name": "Example Astronaut B",
      "craft": "ISS"
    }
  ]
}
```
|
---
## Evaluation – Web Architecture, MVC Design & Security
In this section, evaluate how web technologies, architecture, and design patterns
have been applied in your **AstroBot**. Your responses must relate directly to your
implementation and include reflection on your design decisions.
---

### Web Architecture – Client–Server Model (3 marks)
Explain how the client–server model applies to your AstroBot:
- Identify the **client**
The client is the Webex application used by Astronomy Club members on their computers or mobile devices. AstroBot also acts as an API client when requesting information from Webex and external services.- Identify the
**server(s)**
  The servers are Cisco Webex, OpenWeatherMap and Open Notify. Webex handles messages, OpenWeatherMap provides weather and geocoding information, and Open Notify provides ISS location and astronaut information.
- Describe how data flows between:
- When a user enters /weather London in Webex, AstroBot retrieves the message using get_latest_message(). The bot processes the command and requests London's coordinates using get_city_coordinates(). It then retrieves weather information through get_weather() and sends the formatted response back to Webex using send_message().
- User, AstroBot and APIs
Include a **simple block diagram** to illustrate this interaction.

#### Security Considerations: (3 marks )
- Consider but not limiting to secure handling of API keys and tokens, API rate
limiting, and Input validation (e.g., handling user commands safely), include
examples from code where necessary to illustrate.
AstroBot uses get_webex_token() and get_api_key() to obtain credentials. Users can enter their credentials when starting the program rather than storing real keys directly in the source code. This reduces the risk of exposing credentials on GitHub. However, environment variables and hidden password input would provide better protection, AstroBot uses time.sleep(5) to wait five seconds between checking Webex messages. This helps reduce excessive API requests. External weather and ISS requests are made when users enter the corresponding commands. Additional rate limiting and caching could improve the program. AstroBot checks that commands begin with / and validates city names before requesting weather information. For example, get_weather() rejects empty city names and names longer than 80 characters.
if not city or len(city) > 80:
    return "Please enter a valid city name (up to 80 characters)."
---
### RESTful API Usage in Your Application (3 marks )
Explain how REST APIs are used in your AstroBot:
- Describe how HTTP methods (GET, POST) are used
  AstroBot uses GET requests to retrieve information from Webex, OpenWeatherMap and Open Notify. POST requests are used to send responses into the Webex messaging room.
- Explain how your bot interacts with APIs (Webex, Weather, ISS, Geocoding)
  The get_rooms() function retrieves available Webex rooms, while get_latest_message() retrieves the latest message from the selected room. The send_message() function sends AstroBot's response back into Webex.The get_weather() function requests current weather information using coordinates provided by the geocoding API. It retrieves temperature, humidity, wind speed and weather descriptions.The get_iss_location() function sends a GET request to Open Notify to retrieve the ISS's current latitude, longitude and timestamp.The get_city_coordinates() function converts city names into latitude and longitude. The reverse_geocode() function converts coordinates into nearby location names.
- Describe how JSON responses are received and processed
  AstroBot uses Python's response.json() to convert API responses into Python dictionaries or lists. The program extracts the required values using their keys and formats them into readable messages.
Note: Relate your explanation directly to your code for higher grade.
weather = response.json()
temperature = weather["main"]["temp"]

#### Security Considerations: (2 marks)
- Check response status codes, Handling invalid or unexpected API responses,
Avoiding excessive API calls
---
### MVC Design Pattern in AstroBot (3 Marks)
Explain how the **Model–View–Controller (MVC)** pattern applies to your solution:
Provide a short example based on your implementation
| Component | Description and Example (Relate to your Bot) |
|------------|----------------------------------|
| **Model** |Gets and processes data, Retrieves and processes information from external APIs. Examples include get_city_coordinates(), get_weather() and get_iss_location().. |
| **View** |Presents information to the user, Formats information into readable messages for users. Examples include format_weather_message() and format_iss_message().. |
| **Controller** | Receives commands and decides what happens, Handles incoming commands and decides which functions to execute. The main() function acts as the controller by checking /weather, /iss, /astronauts, /help and /quit.|
---
### 🚀 Reflection and Evaluation ( 8 marks )
Reflect on your AstroBot (400 words):
- How effective is your bot in meeting the Astronomy Club’s needs?
- stroBot was designed to improve communication and information sharing within the Astronomy Club. The bot allows members to request weather information using /weather, ISS location information using /iss and astronaut information using /astronauts. These features are useful for learning about space and planning astronomy activities. Members can access information directly through Webex without visiting several websites. The main features have been implemented in Python, although successful testing within Webex is still required to confirm that the entire system works reliably.
- What design decisions worked well?
- One effective design decision was maintaining the modular structure of the starter code. Functions such as get_weather(), get_iss_location() and send_message() have separate responsibilities. This makes the program easier to understand, debug and maintain. I also used an MVC-inspired design by separating data retrieval, message formatting and command handling. Choosing OpenWeatherMap for both weather and geocoding reduced the number of API providers required.
- What challenges did you face when integrating APIs?
- One challenge I experienced was installing the Python requests library. When I first ran AstroBot, Python displayed a ModuleNotFoundError. I resolved this by installing requests using pip in Python 3.14. Another challenge was understanding the different JSON response formats. For example, OpenWeatherMap returns temperature inside the main object, whereas Open Notify returns ISS coordinates inside iss_position. Different functions were required to process these responses correctly.
- What security risks did you identify and how were they handled?
- The main security risks involved exposing API keys, receiving invalid user input and making excessive API requests. AstroBot allows credentials to be entered at runtime rather than placing real keys in the publicly shared code. It also checks input length, validates HTTP responses and uses exception handling to manage errors. The program waits five seconds between polling requests to reduce API traffic. However, runtime credentials remain visible during entry, and Open Notify uses HTTP endpoints without encryption. These are limitations that should be improved.
- How could your solution be improved in the future?
- Future improvements could include storing credentials securely using environment variables, adding weather forecasts for upcoming stargazing sessions and improving API error handling. The bot could also include predicted ISS viewing times for specific cities and a feature that provides astronomy facts. Additional caching, automated testing and more reliable processing of multiple Webex messages would make AstroBot more efficient and dependable.
---
**Tip:** Link your answers directly to your code and examples for higher marks.
### Notes
- Use official documentation for accuracy (e.g. developer.webex.com, locationiq.com
or Mapbox, open-notify.org or other ISS API).
- Be prepared to explain your findings to your instructor or demo how you retrieved
them using tools like Postman, Curl, or Python scripts.
---
### Total: /40
