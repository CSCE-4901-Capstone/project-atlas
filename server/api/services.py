import requests
import time
import json
import os

#library for secure key handling
import dotenv
from dotenv import load_dotenv

#below is library for database connection and 
#import firebase_admin
#from firebase_admin import credentials, firestore

load_dotenv()       #load the .env file with needed credentials
API_key = os.getenv("OPENROUTER_API_KEY")  #fetch the API_key from environment variables of the server (for the AI model)

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
