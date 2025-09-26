import requests
import time
import json
import os
import asyncio

#library for secure key handling
import dotenv
from dotenv import load_dotenv

load_dotenv()       #load the .env file with needed credentials
AI_API_key = os.getenv("OPENROUTER_API_KEY")  #fetch the API_key from environment variables of the server (for the AI model)
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY") #fetch the API_key from environment variables of the server (for the Weather)
NEWS_API_key = os.getenv("NEWS_API_KEY")

class ExternalAPI():
    def __init__(self):
        self.last_modified = None

    def update_last_modified(self):
        self.last_modified = time.time()

    def get_last_modified(self):
        return  self.last_modified


class FlightAPI(ExternalAPI):
    def __init__(self):
        super().__init__()

    def fetch_data(self):
        self.update_last_modified()
        url = "https://opensky-network.org/api/states/all"

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Error, An HTTP error has occurred:\n{e}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"A request error has occured:\n{e}")
            return []

        return self.build_output(response.json())

    def build_output(self, default_output):
        states_list = default_output['states']
        output = []
        seen_icao24s = set()

        for state in states_list:
            if state[0] in seen_icao24s:
                continue

            seen_icao24s.add(state[0])

            flight_dict = {}
            flight_dict['icao24'] = state[0]
            flight_dict['callsign'] = state[1].strip() if state[1] else None
            flight_dict['country'] = state[2]
            flight_dict['longitude'] = state[5]
            flight_dict['latitude'] = state[6]
            flight_dict['velocity'] = state[9]
            flight_dict['direction'] = state[10]
            flight_dict['category'] = state[17] if len(state) > 17 else None
            output.append(flight_dict)
        return output

class Gemini_API(ExternalAPI):

    AI_Role1 = '''You are to assume the role of a travel planner.
    Your MAIN OBJECTIVE will be to PROVIDE travel information on the country being spoken of
    in the prompt. Assume the traveler is a United States citizen. ONLY RESPOND it in a list format
    where the list consists of necessary travel documents.'''

    AI_Role2 = role = """
    You are a geo-locator assistant. Whenever I give you a URL to a news article, your job is to determine the most likely city where the article was published from, and then respond ONLY in JSON format. Do all research, verification, and background checks silently in the background.

    The JSON format must be:

    {
    "city": "<city name>",
    "url": "<provided url>",
    "title": "<title of article",
    "country": "<country name>",
    "latitude": <decimal latitude>,
    "longitude": <decimal longitude>
    }

    Rules:
    - Use decimal degrees for coordinates (positive = N/E, negative = S/W).
    - Always provide up to 4 decimal places.
    - If the city is unknown, use the nearest identifiable location (region or country) instead.
    - Do not include any text outside the JSON.
    """


    def EnterPrompt_C_Data(self,prompt,Role_choice):
        if (Role_choice == 0):
            Role = self.AI_Role1
        elif (Role_choice == 1):
            Role = self.AI_Role2

        model = "meta-llama/llama-4-maverick:free"
        headers = {
        "Authorization": f"Bearer {AI_API_key}",
        "Content-Type": "application/json"
        }
        print(prompt)
        SendMessage = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        response = requests.get(
        url="https://openrouter.ai/api/v1/key",
        headers={
            "Authorization": f"Bearer {AI_API_key}"
        }
        )
        print(json.dumps(response.json(), indent=2))
        print("🧠 Sending prompt to OpenRouter:", json.dumps(SendMessage, indent=2))
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers = headers,
                json = SendMessage
            )
            data = response.json()
            if response.status_code == 200 and "choices" in data:
                RETURNED_response =  response.json()["choices"][0]["message"]["content"]
                print(RETURNED_response)
                return RETURNED_response
            else:
                print(f"[OpenRouter] Error {response.status_code}: {response.text}")
                return "AI response not recieved."
        except Exception as e:
            print(f"[OpenRouter] Request failed: {e}")
            return "AI service error. Connection failed to be made."

    def get_history(self):
        return []

    def save_history(self,NewHistory: list):
        pass

class WeatherAPIAsync:
    def __init__(self):
        #Grid boundaries and resolution
        self.LAT_MIN, self.LAT_MAX = -90, 90
        self.LON_MIN, self.LON_MAX = -180, 180
        self.STEP = 2  # Keep this at a high-resolution value

        #Grid size
        self.rows = ((self.LAT_MAX - self.LAT_MIN) // self.STEP) + 1
        self.cols = ((self.LON_MAX - self.LON_MIN) // self.STEP) + 1

        #Initialize empty grid
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        
        # ADDED: A property for the cache filename
        self.cache_file = "weather_cache.json"

    def coords_to_index(self, lat, lon):
        if not (self.LAT_MIN <= lat < self.LAT_MAX) or not (self.LON_MIN <= lon < self.LON_MAX):
            return None
        row = int((lat - self.LAT_MIN) // self.STEP)
        col = int((lon - self.LON_MIN) // self.STEP)
        return row, col

    async def _fetch_weather(self, session, lat, lon):
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()

    async def _fetch_and_store(self, session, lat_index, lon_index, lat, lon):
        try:
            data = await self._fetch_weather(session, lat, lon)
            temp = data.get('main', {}).get('temp')
            self.grid[lat_index][lon_index] = temp
        except Exception as e:
            print(f"Failed to fetch ({lat}, {lon}): {e}")
            self.grid[lat_index][lon_index] = None

    async def fill_grid_async(self, force_refresh=False):
        if not force_refresh and os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as f:
                    self.grid = json.load(f)
                    return self.grid
            except Exception as e:
                print(f"Failed to load cached data from {self.cache_file}: {e}")

        #Fetch live data concurrently
        import aiohttp
        async with aiohttp.ClientSession() as session:
            tasks = []
            for lat_index in range(self.rows):
                for lon_index in range(self.cols):
                    lat = self.LAT_MIN + lat_index * self.STEP
                    lon = self.LON_MIN + lon_index * self.STEP
                    tasks.append(self._fetch_and_store(session, lat_index, lon_index, lat, lon))
            await asyncio.gather(*tasks)

        #Save to cache
        try:
            with open(self.cache_file, "w") as f:
                json.dump(self.grid, f)
        except Exception as e:
            print(f"Failed to write cache to {self.cache_file}: {e}")

        return self.grid

class PrecipitationAPIAsync(WeatherAPIAsync):
    def __init__(self):
        super().__init__()
        self.cache_file = "precip_cache.json"

    async def _fetch_and_store(self, session, lat_index, lon_index, lat, lon):
        try:
            data = await self._fetch_weather(session, lat, lon)
            rain = data.get('rain', {}).get('1h', 0)
            snow = data.get('snow', {}).get('1h', 0)
            precipitation = rain + snow
            self.grid[lat_index][lon_index] = precipitation
        except Exception as e:
            print(f"Failed to fetch precipitation ({lat}, {lon}): {e}")
            self.grid[lat_index][lon_index] = None

class NEWS_API(ExternalAPI):
    
    #Arrays that house the countries that could be looked at for News Congestion
    first_20 = {
        1: "India", 2: "China", 3: "United States", 4: "Indonesia", 5: "Pakistan",
        6: "Nigeria", 7: "Brazil", 8: "Bangladesh", 9: "Russia", 10: "Ethiopia",
        11: "Mexico", 12: "Japan", 13: "Egypt", 14: "Philippines", 15: "DR Congo",
        16: "Vietnam", 17: "Iran", 18: "Turkey", 19: "Germany", 20: "Thailand"
    }

    second_20 = {
        21: "Tanzania", 22: "United Kingdom", 23: "France", 24: "South Africa", 25: "Italy",
        26: "Kenya", 27: "Myanmar", 28: "Colombia", 29: "South Korea", 30: "Sudan",
        31: "Uganda", 32: "Spain", 33: "Algeria", 34: "Iraq", 35: "Argentina",
        36: "Afghanistan", 37: "Yemen", 38: "Canada", 39: "Morocco", 40: "Saudi Arabia"
    }

    third_20 = {
        41: "Ukraine", 42: "Uzbekistan", 43: "Peru", 44: "Angola", 45: "Malaysia",
        46: "Mozambique", 47: "Ghana", 48: "Madagascar", 49: "Nepal", 50: "Venezuela",
        51: "Ivory Coast", 52: "North Korea", 53: "Australia", 54: "Niger", 55: "Sri Lanka",
        56: "Burkina Faso", 57: "Syria", 58: "Cambodia", 59: "Senegal", 60: "Chad"
    }

    fourth_20 = {
        61: "Somalia", 62: "Zimbabwe", 63: "Guinea", 64: "Rwanda", 65: "Benin",
        66: "Burundi", 67: "Tunisia", 68: "Bolivia", 69: "Belgium", 70: "Haiti",
        71: "Cuba", 72: "South Sudan", 73: "Dominican Republic", 74: "Czechia", 75: "Greece",
        76: "Jordan", 77: "Paraguay", 78: "Laos", 79: "Libya", 80: "Nicaragua"
    }

    fifth_20 = {
        81: "Kyrgyzstan", 82: "El Salvador", 83: "Togo", 84: "Sierra Leone", 85: "Eritrea",
        86: "Singapore", 87: "Denmark", 88: "Finland", 89: "Norway", 90: "Slovakia",
        91: "Ireland", 92: "New Zealand", 93: "Costa Rica", 94: "Liberia", 95: "Oman",
        96: "Panama", 97: "Kuwait", 98: "Mauritania", 99: "Croatia", 100: "Georgia"
    }
    
    #Dictionary used is the data that constitutes a news point onto the globe
    #when hovering over a point, it should give you the name of the article as a hyperlink to the news article online
    NEWS_POINT = {
        "city":None,
        "url":None,
        "title":None,
        "country":None,
        "latitude":None,
        "longitude":None
    }
    
    def GatherArticles(self,CountryChoice):
        NEWS_API_url = 'https://newsapi.org/v2/everything'
        params = {
            'q': CountryChoice,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 5,
            'apiKey': NEWS_API_key
        }
        print(CountryChoice)
        response = requests.get(NEWS_API_url, params=params)
        return response.json()
    
    def Parse_Spit(self, Articles):
        if not isinstance(Articles, dict) and Articles.get("status") == "error":
            return { "articles": [], "error": Articles.get("message") or Articles.get("code") or "NewsAPI error" }
        if not isinstance(Articles, dict) or "articles" not in Articles:
            return { "articles": [], "error": "Invalid Response from NEWS_API" }
        
        items = Articles.get("articles", [])
        Formatted_Articles = []
        for i, a in enumerate(items, start=1):
            Formatted_Articles.append({
                "Num": i,
                "title": a.get("title"),
                "description": a.get("description"),
                "source": (a.get("source") or {}).get("name"),
                "link": a.get("url"),
            })
        return {"articles": Formatted_Articles}
    
class Agentic_AI(ExternalAPI):
    def Weather_Gather(self):
        return
    def Flight_Gather(self):
        return
    def News_Gather(self):
        return
    def Holistic_View(self):
        return

