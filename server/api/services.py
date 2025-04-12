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
    Your main objective will be to identify the country being spoken of in the prompt,
    and then provide information on the documentation needed to travel to that country assuming the 
    user is an American national.'''
        
    def EnterPrompt_C_Data(self,prompt):
        model = "google/gemini-2.0-pro-exp-02-05:free"
        
        headers = {
        "Authorization": f"Bearer {API_key}",
        "Content-Type": "application/json"
        }
        
        SendMessage = {
            "model": model,                #make sure the message is being sent to the gemini model
            "messages": [
                {#Message to define role of AI in prompt exchange
                    "role": "system",
                    "content": [   
                    {"type": "text", "text": self.AI_Role1}
                    ]
                },
                {#Message to define the message being sent to the AI
                    "role": "user",
                    "content": [   
                    {"type": "text", "text": prompt}
                    ]
                }
            ]
        }
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",           #url of API endpoint
                headers = headers,                          #sending the headers so API knows who is accessing and what format to use
                DataRecieved = json.dumps(SendMessage)              #prompt converted to json file so it can be used by API
            )
            #pushing data to GPT to get processed data
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            
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

        #Grid Constants
        self.LAT_MIN, self.LAT_MAX = -90, 90
        self.LON_MIN, self.LON_MAX = -180, 180
        self.STEP = 5 #5-degree interval

        #Empty Grid
        self.rows = (self.LAT_MAX - self.LAT_MIN) // self.STEP
        self.cols = (self.LON_MAX - self.LON_MIN) // self.STEP
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def coords_to_index(self, lat, lon):
        if not (self.LAT_MIN <= lat < self.LAT_MAX) or not (self.LON_MIN <= lon < self.LON_MAX):
            return None
        row = int((lat - self.LAT_MIN) // self.STEP)
        col = int((lon - self.LON_MIN) // self.STEP)
        return row, col   

    def fetch_weather(self, lat, lon):
        """
        Fetches data based on latitude and longitude.
        """
        self.update_last_modified()
        url = "https://api.openweathermap.org/data/2.5/weather"
        parameters = {
            'lat': lat,
            'lon': lon,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }

        response = requests.get(url, params=parameters)
        response.raise_for_status()
        return self.build_weather(response.json())
    
    def build_weather(self, raw_data):
        """
        Formats weather data into more simpler terms
        """
        return {
            'latitude': raw_data.get('coord', {}).get('lat'),
            'longitude': raw_data.get('coord', {}).get('lon'),
            'temperature': raw_data.get('main', {}).get('temp'),
            'description': raw_data.get('weather', [{}])[0].get('description'),
            'timestamp': raw_data.get('dt'),
            'location_name': raw_data.get('name')

        }
    
    def fill_grid(self, sample_points):
        """
        Given a list of coorinate points, fetch temperature and store in grid
        """
        for lat, lon in sample_points:
            try:
                weather = self.fetch_weather(lat, lon)
                index = self.coords_to_index(lat, lon)
                if index:
                    row, col = index
                    self.grid[row][col] = weather['temperature']
            except Exception as e:
                print(f"Failed to fetch data for ({lat}, {lon}): {e}")
                continue
        return self.grid