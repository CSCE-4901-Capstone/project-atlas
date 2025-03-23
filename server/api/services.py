import requests
import time
import json

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
        response = requests.get(url)
        response.raise_for_status()

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
    

    def EnterPrompt(prompt):
        model = "google/gemini-2.0-pro-exp-02-05:free"
        API_key = os.getenv("OPENROUTER_API_KEY")  #fetch the API_key from environment variables of the server
        
        headers = {
        "Authorization": f"Bearer {API_key}",
        "Content-Type": "application/json"
        }
        AI_Role = '''You are to assume the role of a global news gatherer.
        Your main objective will be to identify the country being spoken of in the prompt,
        and then provide information on the documentation needed to travel to that country assuming the 
        user is an American national.'''
        SendMessage = {
            "model" = model,                #make sure the message is being sent to the gemini model
            "messages":[
                {#Message to define role of AI in prompt exchange
                    "role": "system",   
                    "type": "text",
                    "text": AI_Role
                },
                {#Message to define the message being sent to the AI
                    "role": "user",
                    "type": "text",
                    "text": prompt
                }
            ]
            
        }
        #pushing data to GPT to get processed data
        #additional prompt engineering will be added to ensure proper data fromat is expected
        
    def ReturnPrompt():
        #return data to be implemented from API call
        pass
