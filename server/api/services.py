import requests
import time
import json
import os

#library for secure key handling
import dotenv
from dotenv import load_dotenv
#below is library for database connection and 
'''import firebase_admin
from firebase_admin import credentials, firestore'''



load_dotenv()       #load the .env file with needed credentials
API_key = os.getenv("OPENROUTER_API_KEY")  #fetch the API_key from environment variables of the server (for the AI model)
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY") #fetch the API_key from environment variables of the server (for the Weather)
NEWS_API_key = os.getenv("NEWS_API_KEY")

print("Loaded OpenWeather API Key:", WEATHER_API_KEY)

'''#Below is the connection to the firebase hosted database
Database_path = os.getenv("FIREBASE_PATH")
DB_creds = credentials.Certificate(Database_path)
firebase_admin.initialize_app(DB_creds)

DB = firestore.client()             #Create Database instance in the backend'''


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
    
    AI_Role2 = '''asdfasf'''
    
    def EnterPrompt_C_Data(self,prompt,Role_choice):
        #selection of AI role to make the call to the API
        if (Role_choice == 0):
            Role = self.AI_Role1
        elif (Role_choice == 1):
            Role = self.AI_Role2
            
        model = "meta-llama/llama-4-maverick:free"
        
        #model = "google/gemini-2.5-pro-exp-03-25:free"
        
        headers = {
        "Authorization": f"Bearer {AI_API_key}",
        "Content-Type": "application/json"
        }
        
        #for future debuggin, in case the API_Key is changed, uncomment the code below to check if API_Key supports Model being used
        '''response = requests.get(
            url="https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {API_key}"}
        )
        print(response.json())'''

        '''{#Message to define role of AI in prompt exchange
                "role": "system",
                "content": Role
            },'''
        
        print(prompt)
        
        SendMessage = {
            "model": model,                #make sure the message is being sent to the gemini model
            "messages": [
                {#Message to define the message being sent to the AI
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
                "https://openrouter.ai/api/v1/chat/completions",           #url of API endpoint
                headers = headers,                          #sending the headers so API knows who is accessing and what format to use
                json = SendMessage              #prompt converted to json file so it can be used by API
            )
            
            data = response.json()
            
            #pushing data to GPT to get processed data
            if response.status_code == 200 and "choices" in data:
                
                #collect the response from the AI model
                RETURNED_response =  response.json()["choices"][0]["message"]["content"]
                
                #output the returned Message from the API
                print(RETURNED_response)
                
                return RETURNED_response #use line to return prompt raw
            
            else:   #display error message in event that API request is unsuccessful
                print(f"[OpenRouter] Error {response.status_code}: {response.text}")
                return "AI response not recieved."
        except Exception as e:
            print(f"[OpenRouter] Request failed: {e}")
            return "AI service error. Connection failed to be made."
    
    def get_history(self): #retrieve the history already allocated in the database for a specific user
        
        return []
    
    def save_history(self,NewHistory: list): #save the new history to the database or file for a specific user
        pass

class WeatherAPI(ExternalAPI):
    def __init__(self):
        super().__init__()

        # Grid Constants
        self.LAT_MIN, self.LAT_MAX = -90, 90
        self.LON_MIN, self.LON_MAX = -180, 180
        self.STEP = 10  # 5-degree interval

        # Empty Grid
        self.rows = (self.LAT_MAX - self.LAT_MIN) // self.STEP
        self.cols = (self.LON_MAX - self.LON_MIN) // self.STEP
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        # Caching configuration
        self.cache_file = "weather_cache.json"
        self.cache_expiry = 3600  # 1 hour in seconds (adjust as needed)

    def coords_to_index(self, lat, lon):
        if not (self.LAT_MIN <= lat < self.LAT_MAX) or not (self.LON_MIN <= lon < self.LON_MAX):
            return None
        row = int((lat - self.LAT_MIN) // self.STEP)
        col = int((lon - self.LON_MIN) // self.STEP)
        return row, col

    def load_cache(self):
        """Load cached data if it exists and is fresh"""
        if os.path.exists(self.cache_file):
            file_age = time.time() - os.path.getmtime(self.cache_file)
            if file_age < self.cache_expiry:
                try:
                    with open(self.cache_file, 'r') as f:
                        self.grid = json.load(f)
                        print("Loaded weather data from cache")
                        return True
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error loading cache: {e}")
        return False

    def save_cache(self):
        """Save current grid data to cache file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.grid, f)
            print("Saved weather data to cache")
        except IOError as e:
            print(f"Error saving cache: {e}")

    def fetch_weather(self, lat, lon):
        """Fetches weather data based on latitude and longitude"""
        self.update_last_modified()
        
        url = "https://api.openweathermap.org/data/2.5/weather"
        parameters = {
            'lat': lat,
            'lon': lon,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }

        try:
            response = requests.get(url, params=parameters)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch weather for ({lat}, {lon}): {e}")
            return None

    def fill_grid(self):
        """
        Fill the grid with weather data, using cache if available and fresh
        Otherwise fetch new data and cache it
        """
        # Try to load from cache first
        if self.load_cache():
            return self.grid

        # If cache not available or expired, fetch fresh data
        print("Fetching fresh weather data...")
        for lat_index in range(self.rows):
            for lon_index in range(self.cols):
                lat = self.LAT_MIN + lat_index * self.STEP
                lon = self.LON_MIN + lon_index * self.STEP
                weather_data = self.fetch_weather(lat, lon)
                if weather_data:
                    self.grid[lat_index][lon_index] = weather_data.get('main', {}).get('temp')
                time.sleep(0.02)  # Small delay to avoid rate limiting

        # Save the fresh data to cache
        self.save_cache()
        return self.grid
    
class NEWS_API(ExternalAPI):
    
    def GatherArticles(self,CountryChoice):          #function for getting LIVE valid articles pertaining to a CountryChoice
        
        NEWS_API_url = 'https://newsapi.org/v2/everything'          #NEWS_API endpoint
        
        params = {              #parameters to be sent to the NEWS API
            'q': CountryChoice,         # Search query
            'language': 'en',              # English articles only
            'sortBy': 'publishedAt',       # Sort by latest news
            'pageSize': 5,                 # Number of articles
            'apiKey': NEWS_API_key              # Your API key
        }
        print(CountryChoice)
        # Make the request to the NEWS API
        response = requests.get(NEWS_API_url, params=params)
        
        return response.json()          #return the json response collection of article
