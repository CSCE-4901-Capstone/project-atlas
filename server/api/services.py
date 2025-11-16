from __future__ import annotations
import requests
import socket
import math
import tldextract
import time
from time import monotonic
import json
import os
import asyncio
import feedparser
from shapely.geometry import MultiPoint
from pathlib import Path
import statistics
import aiohttp

from datetime import datetime as dt         #alias datetime for ease of use (use for crewAI)
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED,TimeoutError, as_completed       #dependencies needed for threading
import threading
_cache_lock = threading.RLock()

from typing import Any, Dict, List, Tuple, Optional      #included to make database value handling easier

#library for secure key handling
import dotenv
from dotenv import load_dotenv

#library needed for DB communication
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app


#libraries and global variable declarations necessary for geolocation
# Global throttle for geopy across all threads (token-bucket-ish: 1 req/sec)
_GEOPY_MIN_INTERVAL = 1.5  # seconds; change to 0.7 if you have permission
_last_geopy_ts = 0.0
_geopy_lock = threading.Lock()

# geopy for lat/lon (as requested)
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# extruct to parse JSON-LD (schema.org) from publisher homepage
import extruct
from w3lib.html import get_base_url


load_dotenv()       #load the .env file with needed credentials

#OR_Keys
AI_API_key = os.getenv("OPENROUTER_API_KEY")  #fetch the API_key from environment variables of the server (for the AI model)
AI_API_key2 = os.getenv("OPENROUTER_API_KEY2")  #fetch the API_key from environment variables of the server (for the AI model)
AI_API_key3 = os.getenv("OPENROUTER_API_KEY3")  #fetch the API_key from environment variables of the server (for the AI model)
AI_API_key4 = os.getenv("OPENROUTER_API_KEY4")  #fetch the API_key from environment variables of the server (for the AI model)
AI_API_key5 = os.getenv("OPENROUTER_API_KEY5")  #fetch the API_key from environment variables of the server (for the AI model)


#weather_Keys
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY") #fetch the API_key from environment variables of the server (for the Weather)

#News_Keys
NEWS_API_key = os.getenv("NEWS_API_KEY")
NEWS_API_key2 = os.getenv("NEWS_API_KEY2")
NEWS_API_key3 = os.getenv("NEWS_API_KEY3")
NEWS_API_key4 = os.getenv("NEWS_API_KEY4")
NEWS_API_key5 = os.getenv("NEWS_API_KEY5")

#DB info pulled from env file used for DB operations
info = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": (os.getenv("PRIVATE_KEY") or ""),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN") or "googleapis.com",        
}
    
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

    AI_Role2 = role ="""
    You are a geo-locator assistant. Whenever I give you a json containing a URL to a news article, the title of the article, and a country field, 
    your job is to determine the most likely city where the article was published from and its country of origin based on the latitude and longitude, 
    and then respond ONLY in JSON format. Do all research, verification, and background checks silently in the background. PROCESS QUICKLY!

    The JSON format must be:

    {
    "city": "<city name>",
    "url": "<(provided)>",
    "title": "<(provided)>",
    "country": "<(provided)>",
    "latitude": <decimal latitude>,
    "longitude": <decimal longitude>
    }

    Rules:
    - Use decimal degrees for coordinates (positive = N/E, negative = S/W).
    - Always provide up to 4 decimal places.
    - If the city is unknown, use the nearest identifiable location (region or country) instead.
    - Do not include any text outside the JSON.
    - Do not number the bullet points
    """
    AI_Role3 = '''You are an administrative analyst who is responsible for providing holistic, comprehensive, and informative
    briefs on a selected country.

    Task: Given JSON blocks for WEATHER, FLIGHTS, and NEWS for a COUNTRY, write a HOLISTIC BRIEF.

    Rules:
    - Output 3 bullet points in Markdown do not number the bullet points.
    - Use only paragraphs for each bullet point and use one bullet point to give a recommendation based on current events
    - Avoid negative connotation or outlook determine
    - Do not number the list
    - Only print the list no other p elements or unnecessary text 
    - Each bullet must include at least one numeric fact (e.g., °C, wind m/s, aircraft count, timestamp or date).
    - Use tags that define the summarization through emojis
    - If a section is sparse or uncertain, say so briefly rather than inventing facts.
    - Format the response so that it is easy to read with good sectioning as well.
    - RETURN THE ANALYSIS QUICKLY. ANALYSIS SHOULD NOT EXCEED 5 SECONDS BUT AT THE MINIMUM BE 2 SECONDS IN LENGTH.
    '''


    def EnterPrompt_C_Data(self,prompt,Role_choice):
        if (Role_choice == 0):
            Role = self.AI_Role1
        elif (Role_choice == 1):
            Role = self.AI_Role2
        elif (Role_choice == 2):
            Role = self.AI_Role3
        else:
            Role = Role_choice      #if not defined as a role, simply use whatever was passed to Role_choice as the role

        model = "nvidia/nemotron-nano-12b-v2-vl:free" #"meta-llama/llama-4-maverick:free" #"openrouter/openai/gpt-4o-mini"
        headers = {
        "Authorization": f"Bearer {AI_API_key}",
        "Content-Type": "application/json"
        }
        print(prompt)
        SendMessage = {
            "model": model,  # e.g., "xai/grok-2-mini"
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": Role}
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt}
                    ]
                }
            ],
            "temperature": 0.2
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
            
            #CODE EXECUTES ONLY WHEN THE FIRST AI_API_KEY FAILED
            # treat 401/402/429 or error text mentioning rate/quota/insufficient as "limit ran out"
            resp_text_lower = (response.text or "").lower()
            
            #CHECK whether in fact the api key ran into its call limitation
            is_limit_error = (
                response.status_code in (401, 402, 429) or
                ("error" in data and isinstance(data["error"], dict) and any(
                    s in str(data["error"]).lower() for s in ["rate", "quota", "insufficient", "overloaded"]
                )) or
                any(s in resp_text_lower for s in ["rate", "quota", "insufficient", "overloaded", "limit"])
            )

            #try the other keys until you get a response
            if is_limit_error:
                # try next keys in order; swap AI_API_key and re-use the same headers/SendMessage
                for next_key in [k for k in [AI_API_key2, AI_API_key3, AI_API_key4, AI_API_key5] if k]:
                    if not next_key:
                        continue

                    headers["Authorization"] = f"Bearer {next_key}"
                    print("🔁 Quota/limit hit; swapping key and retrying...")

                    response = requests.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        json=SendMessage
                    )
                    try:
                        data = response.json()
                    except Exception as e:
                        print(f"[OpenRouter] Request failed: {e}")
                        return "AI response not recieved."

                    #Send out the correct response once sure that its a good response
                    if response.status_code == 200 and "choices" in data:
                        RETURNED_response = data["choices"][0]["message"]["content"]
                        print(RETURNED_response)
                        return RETURNED_response
        
        #return error message in event that that a non-key related issue is preventing the response
        except:
            print(f"[OpenRouter] Error {response.status_code}: {response.text}")
            print("Trying with another AI_API_key")
            return "AI response not recieved."

class WeatherAPIAsync:
    def __init__(self, step=2):
        # Grid boundaries and resolution
        self.LAT_MIN, self.LAT_MAX = -90, 90
        self.LON_MIN, self.LON_MAX = -180, 180
        self.STEP = step

        # Grid size
        self.rows = int(((self.LAT_MAX - self.LAT_MIN) // self.STEP) + 1)
        self.cols = int(((self.LON_MAX - self.LON_MIN) // self.STEP) + 1)

    def coords_to_index(self, lat, lon):
        if not (self.LAT_MIN <= lat < self.LAT_MAX) or not (self.LON_MIN <= lon < self.LON_MAX):
            return None
        row = int((lat - self.LAT_MIN) // self.STEP)
        col = int((lon - self.LON_MIN) // self.STEP)
        return row, col

    async def _fetch_weather(self, session, lat, lon):
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": WEATHER_API_KEY,
            "units": "metric",
        }
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()

    async def _fetch_cell(self, session, lat_index, lon_index, lat, lon):
        try:
            data = await self._fetch_weather(session, lat, lon)
            temp = data.get("main", {}).get("temp")
            return lat_index, lon_index, temp
        except Exception as e:
            print(f"Failed to fetch ({lat}, {lon}): {e}")
            return lat_index, lon_index, None

    async def fill_grid_async(self):
        """Fetch live temperature data for every grid cell and return 2D array."""
        grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        tasks = []

        async with aiohttp.ClientSession() as session:
            for lat_index in range(self.rows):
                for lon_index in range(self.cols):
                    lat = self.LAT_MIN + lat_index * self.STEP
                    lon = self.LON_MIN + lon_index * self.STEP
                    tasks.append(self._fetch_cell(session, lat_index, lon_index, lat, lon))

            results = await asyncio.gather(*tasks)

        for lat_index, lon_index, value in results:
            grid[lat_index][lon_index] = value

        if grid is not None:
            print("fill_grid_async(self): Weather Data Cached")
        elif grid is None:
            print("fill_grid_async(self): Error recieving Weather Data. Weather Data was cached unsuccessfully")

        return grid


class PrecipitationAPIAsync(WeatherAPIAsync):
    def __init__(self, step=1):
        super().__init__(step=step) 

    async def _fetch_cell(self, session, lat_index, lon_index, lat, lon):
        try:
            data = await self._fetch_weather(session, lat, lon) 
            rain = data.get('rain', {}).get('1h', 0)
            snow = data.get('snow', {}).get('1h', 0)
            
            precipitation = rain + snow
            
            return lat_index, lon_index, precipitation
        except Exception as e:
            print(f"Failed to fetch precipitation ({lat}, {lon}): {e}")
            return lat_index, lon_index, None

    async def fill_grid_async(self, **kwargs):
        
        grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        tasks = []

        async with aiohttp.ClientSession() as session:
            for lat_index in range(self.rows):
                for lon_index in range(self.cols):
                    lat = self.LAT_MIN + lat_index * self.STEP
                    lon = self.LON_MIN + lon_index * self.STEP
                    
                    tasks.append(self._fetch_cell(session, lat_index, lon_index, lat, lon))

            results = await asyncio.gather(*tasks)

        for lat_index, lon_index, value in results:
            grid[lat_index][lon_index] = value

        
        if grid is not None:
            print("fill_grid_async(self,**kwargs): Data cached Successfully")
        elif grid is None:
            print("fill_grid_async(self,**kwargs): Attempt Unsuccessful. Data not cached.")

        return grid

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

    def GatherArticles(self, CountryChoice):
        NEWS_API_url = "https://newsapi.org/v2/everything"

        for key in [k for k in [NEWS_API_key, NEWS_API_key2, NEWS_API_key3, NEWS_API_key4, NEWS_API_key5] if k]:
            params = {
                "q": CountryChoice,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": 10,
                "apiKey": key,
            }
            try:
                print(f"Gathering articles for {CountryChoice} with key {key[:6]}...")
                response = requests.get(NEWS_API_url, params=params, timeout=10)
                data = response.json()
            except Exception:
                continue  # skip to next key if a connection or parse error occurs

            # if success, return immediately
            if response.status_code == 200 and data.get("status") == "ok":
                return data

            # rotate only on rate-limit or quota errors
            code = str(data.get("code", "")).lower()
            msg = str(data.get("message", "")).lower()
            if not (response.status_code in (401, 429)
                    or code in {"apikeyexhausted", "apikeydisabled", "ratelimited", "maximumresultsreached"}
                    or any(s in msg for s in ["rate", "quota", "exhaust", "over quota", "limit"])):
                return data  # non-quota error, return as-is and stop trying

        return {"status": "error", "message": "All NewsAPI keys failed or are rate-limited."}


    def GatherArticles_InMass(self,CountryChoice):

        NEWS_API_url = "https://newsapi.org/v2/everything"

        for key in [k for k in [NEWS_API_key, NEWS_API_key2, NEWS_API_key3, NEWS_API_key4, NEWS_API_key5] if k]:
            params = {
                "q": CountryChoice,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": 100,
                "apiKey": key,
            }
            try:
                print(f"Gathering articles for {CountryChoice} with key {key[:6]}...")
                response = requests.get(NEWS_API_url, params=params, timeout=10)
                data = response.json()
            except Exception:
                continue  # skip to next key if a connection or parse error occurs

            # if success, return immediately
            if response.status_code == 200 and data.get("status") == "ok":
                return data

            # rotate only on rate-limit or quota errors
            code = str(data.get("code", "")).lower()
            msg = str(data.get("message", "")).lower()
            if not (response.status_code in (401, 429)
                    or code in {"apikeyexhausted", "apikeydisabled", "ratelimited", "maximumresultsreached"}
                    or any(s in msg for s in ["rate", "quota", "exhaust", "over quota", "limit"])):
                return data  # non-quota error, return as-is and stop trying

        return {"status": "error", "message": "All NewsAPI keys failed or are rate-limited."}


    def GatherArticles_DB_Refresh(self,CountryChoice: str) -> dict:     #ensure that a dict of country names can be passed as an argument
        NEWS_API_url = "https://newsapi.org/v2/everything"

        for key in [k for k in [NEWS_API_key, NEWS_API_key2, NEWS_API_key3, NEWS_API_key4, NEWS_API_key5] if k]:
            params = {
                "q": CountryChoice,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": 5,
                "apiKey": key,
            }
            try:
                print(f"Gathering articles for {CountryChoice} with key {key[:6]}...")
                response = requests.get(NEWS_API_url, params=params, timeout=10)
                data = response.json()
            except Exception:
                continue  # skip to next key if a connection or parse error occurs

            # if success, return immediately
            if response.status_code == 200 and data.get("status") == "ok":
                return data

            # rotate only on rate-limit or quota errors
            code = str(data.get("code", "")).lower()
            msg = str(data.get("message", "")).lower()
            if not (response.status_code in (401, 429)
                    or code in {"apikeyexhausted", "apikeydisabled", "ratelimited", "maximumresultsreached"}
                    or any(s in msg for s in ["rate", "quota", "exhaust", "over quota", "limit"])):
                return data  # non-quota error, return as-is and stop trying

        return {"status": "error", "message": "All NewsAPI keys failed or are rate-limited."}


    def Gather_DB_for_Save(self, *country_groups: dict) -> None:                #funciton used to gather new articles
        file_idx = 1          # current output file number
        buffer = []           # holds up to 100 article objects (flattened)

        # === Output directory: server/api/Article_cache
        api_dir = Path(__file__).resolve().parent          # -> get the /server/api directory
        out_dir = api_dir / "Article_cache"                # -> add subdirectory to make /server/api/Article_cache path
        out_dir.mkdir(parents=True, exist_ok=True)


        for group in country_groups:
            for country in group.values():
                try:
                    data = self.GatherArticles_DB_Refresh(country)
                    cleaned = self.Parse_Spit_Mass(data)

                    # Add each article (flattened) into the rolling buffer
                    for art in cleaned.get("articles", []):
                        buffer.append(art)
                        

                        #group gathered files into those of 100 (should be about 5 files) into a subdirectory (Article_cache)
                        if len(buffer) == 100:
                            out_path = out_dir / f"CountriesGroup{file_idx}.json"
                            
                            with out_path.open(f"CountriesGroup{file_idx}.json", "w", encoding="utf-8") as f:
                                json.dump(buffer, f, indent=2)
                            print(f"Wrote 100 articles in CountriesGroup{file_idx}.json to {out_path}")
                            file_idx += 1
                            buffer = []

                    print(f"Saved data for {country}")

                except requests.HTTPError as e:
                    print(f"[HTTP {e.response.status_code}] {country}: {e}")
                except Exception as e:
                    print(f"[Error] {country}: {e}")
        
        #make sure to write out any partial buffers in event that 100 articles aren't gathered            
        if buffer:
            out_path = out_dir / f"CountriesGroup{file_idx}.json"
            with out_path.open("w", encoding="utf-8") as f:
                json.dump(buffer, f, ensure_ascii=False, indent=2)
            print(f"Wrote {len(buffer)} articles to {out_path} (final partial file)")



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
    
    def Parse_Spit_Mass(self, Articles):
        if not isinstance(Articles, dict) and Articles.get("status") == "error":
            return { "articles": [], "error": Articles.get("message") or Articles.get("code") or "NewsAPI error" }
        if not isinstance(Articles, dict) or "articles" not in Articles:
            return { "articles": [], "error": "Invalid Response from NEWS_API" }

        items = Articles.get("articles", [])
        Formatted_Articles = []
        for i, a in enumerate(items, start=1):
            Formatted_Articles.append({
                "title": a.get("title"),
                "url": a.get("url"),
                "country": a.get("queried_country"),
            })
        return {"articles": Formatted_Articles}

    def NewsPointBuilder(self,CountryList):
        #Articles = []           #create empty list to hold articles
        AI = Gemini_API()       #make instance of AI to serve as a geolocator

        if isinstance(CountryList, str) and CountryList in globals():
            CountryList = globals()[CountryList]         #set the country array once matched to the global array

        CountryList = list(CountryList.values())                 #ensure that the list for countries is created

        #items = Articles.get("articles", [])                #used for parsing the articles
        Formatted_Articles = []                 #array to hold the list of the formatted articles that are passed to AI component

        for country in CountryList:                 #append articles for every country in the array after pulling articles

            try:
                #use different Parse_spit function, but this new one retains the country field.
                
                
                Response_chunk = self.GatherArticles_InMass(country)
                #Articles.append(Response_chunk)                             #append each recieved article for each country

            except Exception as e:
                print(f"Error while gathering Articles for {country}: {e}")
                continue

            #Error handling for NewsAPI
            if not isinstance(Response_chunk, dict):
                print(f"{country}: non-dict response")
                continue
            if Response_chunk.get("status") == "error":
                print(f"{country}: NewsAPI error -> {Response_chunk.get('message') or Response_chunk.get('code')}")
                continue

            for a in (Response_chunk.get("articles",[]) or []):
                Formatted_Articles.append({
                    "url": a.get("url"),
                    "title": a.get("title"),
                    "country": country,           #set the country to that of the country already being read in from input
                })

        #Articles.clear()                    #clear the for stuff not needed to ensure there are no memory leaks

        #REMOVE if slows down application significantly
        print(Formatted_Articles)           #print out the parsed data to ensure that data was created and stored properly

        try:
            Formatted_Articles = AI.EnterPrompt_C_Data(Formatted_Articles,1)            #make JSON prompt and then assign GeoLocator Role
        except Exception as e:
            print(f"AI reponse error for geolocation data of country: {e}")

        #REMOVE if slows down application significantly
        print(Formatted_Articles)           #print out the parsed data to ensure that data was created and stored properly

        return {"articles": Formatted_Articles}

class Agentic_AI(ExternalAPI):              #work on after getting the congestion filter built out completely

    AI_model = Gemini_API()         #use instance of AI model already created earlier

    def Weather_Gather(self, country: str) -> str:
        Role = f'''Your main goal is to act as a meteorologist for the country {country},
        Find meaningful weather observations occuring in {country}. Your task is to analyze
        the weather to an extent where the information provided would be inline with what an
        expert would provide to someone if asked for a full-on weather report. Restrict the analysis to 1 paragraph of text in markdown
        and process the request QUICKLY.Only return the paragraph text. Do not include any other text.
        '''
        prompt = f"for the country of {country} find the most relevant data for today relevant to your role"

        print("making request for Weather_gather()")
        #make call to api and return the data
        return self.AI_model.EnterPrompt_C_Data(prompt,Role)
    
    def Temperature_Weather_Gather(self,country:str) -> str:
        Role = f'''Your main goal is to act as a meteorologist for the country {country},
        Find meaningful weather observations occuring in {country}. Your task is to analyze
        the weather to an extent where the information provided would provide meaningful insights on
        TEMPERATURE/climate of the country in question. Restrict to 1 paragraph of text in markdown
        and process the request QUICKLY.
        Only return the paragraph text. Do not include any other text.'''
        prompt = f"for the country of {country} find the most relevant data for today relevant to your role"

        print("making request for Temperature_Weather_gather()")
        #make call to api and return the data
        return self.AI_model.EnterPrompt_C_Data(prompt,Role)
    
    def Percipitation_Weather_Gather(self,country:str) -> str:
        Role = f'''Your main goal is to act as a meteorologist for the country {country},
        Find meaningful weather observations occuring in {country}. Your task is to analyze
        the weather to an extent where the information provided would provide meaningful insights on
        Precipitaiton (including snow, hail, sleet) of the country in question. Restrict to 1 paragraph of text in markdown
        and process the request QUICKLY.
        Only return the paragraph text. Do not include any other text.'''
        prompt = f"for the country of {country} find the most relevant data for today relevant to your role"

        print(f"making request for Percipitation_Weather_gather({country})")
        #make call to api and return the data
        return self.AI_model.EnterPrompt_C_Data(prompt,Role)

    def Disaster_Gather(self,country:str) -> str:
        Role = f'''Your main goal is to act as a Natural Scientist for the country {country}. Your area of
        expertise is seismology, volcanology, hydrology, and fire science (interms of wild fires).
        Find meaningful weather observations occuring in {country} relating to recent natural disasters occuring
        within {country}. Your task is to analyze the natural disasters to an extent where the information provided would provide 
        meaningful insights on natual disasters occuring for the country in question. Restrict to 1 paragraph of text in markdown
        and process the request QUICKLY.
        Only return the paragraph text. Do not include any other text.'''
        prompt = f"for the country of {country} find the most relevant data for today relevant to your role"

        print(f"making request for Disaster_gather({country})")
        #make call to api and return the data
        return self.AI_model.EnterPrompt_C_Data(prompt,Role)

    def Flight_Gather(self, country: str) -> str:
        Role = f'''You are an Air Traffic Operations Analyst. Your job is to deliver RECENT, numbers-first flight activity for the country: {country}.

        ### Mission
        1) Report the most recent **average daily flights** (arrivals + departures) for {country} from a reputable source updated THIS WEEK if possible.
        2) Break down flights for the **five most populous cities** in {country} (aggregate multi-airport city systems, e.g., “London = LHR+LGW+STN+LTN+LCY”).
        3) Compute each city’s **share (%)** of {country}’s total.
        4) Return a single JSON object (no extra text).

        ### Data Freshness Rules
        - PRIORITIZE sources updated this week (e.g., EUROCONTROL/NATS/FAA/ICAO/state ANSPs).
        - If exact “this week” per-city numbers are not published, use the most recent monthly/weekly airport-level averages **published within the last 30 days**, and clearly label the period in the JSON.
        - DO NOT use data older than 12 months.
        - If a city lacks a fresh numeric value, set that city’s fields to null and add a short “note”.

        ### Calculation Rules
        - Share (%) = (city avg_daily_flights / country_total_avg_daily_flights) * 100, rounded to 2 decimals.
        - When aggregating a multi-airport city, sum airport averages first, then compute the share.
        - Keep units consistent: “avg_daily_flights” counts flights (arrivals+departures).

        ### Tone & Constraints
        - Prefer precise numbers from sources; if reading off a chart, state “estimated from chart” in methodology_notes.
        - Avoid blogs/forums; only cite primary/official or widely recognized aviation analytics.
        - Process request QUICKLY!
        '''

        prompt = f"for the country of {country} find the most relevant data for today relevant to your role"

        print(f"making request for Flight_gather({country})")
        #make call to api and return the data
        return self.AI_model.EnterPrompt_C_Data(prompt,Role)

    def Flight_Trend_Gather(self, country: str) -> str:
        Role = f'''You are an Air Traffic Operations Analyst. Your job is to deliver RECENT, numbers-first flight activity for the country: {country}.

        ### Mission
        1) Report the most recent **average daily flights** (arrivals + departures) for {country} from a reputable source updated THIS WEEK if possible.
        2) Break down flights for the **five most populous cities** in {country} (aggregate multi-airport city systems, e.g., “London = LHR+LGW+STN+LTN+LCY”).
        3) Compute each city’s **share (%)** of {country}’s total.
        4) Return a series of bullets with the analysis no longer than 20 bullet points
        5) Process request QUICKLY. DO NOT GIVE THE RESPONSE IN MARKDOWN, SIMPLY RETRN IT AS A STRING with good formatting.
        6) ONLY RETURN THE BUULLETS, NO OTHER INTRODUCTORY TEXT. ENSURE THERE IS AT LEAST ONE SPACE BETWEEN THE BULLETS.
        
        ### Data Freshness Rules
        - PRIORITIZE sources updated this week (e.g., EUROCONTROL/NATS/FAA/ICAO/state ANSPs).
        - If exact “this week” per-city numbers are not published, use the most recent monthly/weekly airport-level averages **published within the last 30 days**, and clearly label the period in the JSON.
        - DO NOT use data older than 12 months.
        - If a city lacks a fresh numeric value, set that city’s fields to null and add a short “note”.

        ### Calculation Rules
        - Share (%) = (city avg_daily_flights / country_total_avg_daily_flights) * 100, rounded to 2 decimals.
        - When aggregating a multi-airport city, sum airport averages first, then compute the share.
        - Keep units consistent: “avg_daily_flights” counts flights (arrivals+departures).

        ### Tone & Constraints
        - Prefer precise numbers from sources; if reading off a chart, state “estimated from chart” in methodology_notes.
        - Avoid blogs/forums; only cite primary/official or widely recognized aviation analytics.
        - Process request QUICKLY!
        '''

        prompt = f"for the country of {country} find the most relevant data for today relevant to your role"

        print(f"making request for Flight_Trend_gather({country})")
        #make call to api and return the data
        return self.AI_model.EnterPrompt_C_Data(prompt,Role)

    def News_Gather(self, country: str) -> str:
        Role = f'''You are a journalist who specializes in news for the country of {country}.

        Your objective is to find out what the most current topics of interest are in {country} and
        formulate an in-depth analysis on the most talked about and also not so often touched on areas
        of {country}'s news that might be easy to see or hard to see for an outsider to {country}. Restrict the
        analysis to 1 paragraph in markdown. Only return the paragraph text. Do not include any other text.
        '''
        prompt = f"for the country of {country} find the most relevant data for today relevant to your role"

        print(f"making request for News_gather({country})")
        #make call to api and return the data
        return self.AI_model.EnterPrompt_C_Data(prompt,Role)
    def Holistic_View(self, country: str,timeout=15):        #SessionNum,
        print("starting call for Holistic_View()")
        print("threading data...")

        Weather_Data = ""           #initialize variables before threading
        Flight_Data = ""
        News_Data = ""


        #THREAD RESPONSES TO REDUCE LATENCY
        with ThreadPoolExecutor(max_workers=3) as pool:
            W_Data_THREAD = pool.submit(self.Weather_Gather, country)
            F_Data_THREAD = pool.submit(self.Flight_Gather, country)
            N_Data_THREAD = pool.submit(self.News_Gather, country)

            #SET THREAD RESPONSE OF WEATHER
            try:
                Weather_Data = W_Data_THREAD.result(timeout=60) or ""
            except Exception as e:
                print(f"Weather_Gather failed: {e}")
                Weather_Data = ""

            #SET THREAD RESPONSE OF FLIGHTS
            try:
                Flight_Data = F_Data_THREAD.result(timeout=60) or ""
            except Exception as e:
                print(f"Flight_Gather failed: {e}")
                Flight_Data = ""

            #SET THREAD RESPONSE OF NEWS
            try:
                News_Data = N_Data_THREAD.result(timeout=60) or ""
            except Exception as e:
                print(f"News_Gather failed: {e}")
                News_Data = ""

        #constructing Prompt with data for AI agent to have context for analysis
        Prompt = (
            f"Country to be analyzed: {country}\n\n"
            "Weather Data to be considered:\n" + Weather_Data + "\n\n"
            "Flight Data to be considered:\n" + Flight_Data + "\n\n"
            "News Data to be considered:\n" + News_Data + "\n\n"
        )

        #update logic

        return self.AI_model.EnterPrompt_C_Data(Prompt,Role_choice=2)           #perform holistic analysis


class DisasterAPI(ExternalAPI):
    def __init__(self):
        super().__init__()

    def fetch_data(self):
        self.update_last_modified()
        url = "https://eonet.gsfc.nasa.gov/api/v3/events"

        try:
            response = requests.get(url, )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Error, An HTTP error has occurred:\n{e}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"A request error has occured:\n{e}")
            return []

        return self.build_output(response.json())

    def build_output(self, default_output):
        events_list = default_output['events']
        output = []

        for event in events_list:
            events_dict = {}
            events_dict['type'] = event['categories'][0]['id']
            geometry_list = event['geometry']
            magnitudes = []
            coordinate_list = []
            for geometry in geometry_list:
                magnitudes.append(geometry['magnitudeValue'])
                coordinate_list.append(geometry['coordinates'])

            center = MultiPoint(coordinate_list).centroid
            #mean_magnitude = statistics.mean(magnitudes)
            events_dict['longitude'] = center.x
            events_dict['latitude'] = center.y
            #events_dict['magnitude'] = mean_magnitude

            output.append(events_dict)
        return output

class DB_Manager_NEWS(ExternalAPI):
    
    def GetNew_Articles():                  #function used to get new geolocated Articles from NewsAPI 
        NEWS = NEWS_API()                   #create instance of NEWS_API class to gain access to necessary functions
        
        #get the names of all countries that need to be processed
        first_20_C = NEWS_API.first_20
        second_20_C = NEWS_API.second_20
        third_20_C = NEWS_API.third_20
        fourth_20_C = NEWS_API.fourth_20
        fifth_20_C = NEWS_API.fifth_20
        
        Articles = {}           #create variable to hold the articles that will be collected
        
        api_dir = Path(__file__).resolve().parent           #get server/api directory
        out_dir_Article = api_dir / "Article_cache"                 #add on Article_cache subdirectory to path
        out_dir_geo = api_dir / "Geolocated_cache"                 #add on Article_cache subdirectory to path
        
        #Make call to NEWS API to get some articles for refresh
        try:
            
            #collect about 500 total articles (5 for each 100 countries) and save the articles to Article_cache subdirectory
            NEWS_API.Gather_DB_for_Save(first_20_C,second_20_C,third_20_C,fourth_20_C,fifth_20_C)
            
            if len(out_dir_Article) == 0:               #check to see whether the articles have populated in Article_cache subdirectory
                print("Error adding Articles to Article_cache subdirectory")
                return
            elif len(out_dir_Article) >= 1:
                print("Files present in Article_cache subdirectory")            
                  
            Geo = Geolocator()          #create instance of Geolocator class to gain access to necessary functions
            
            #geolocate the articles in Article_cache and save the geolocated articles to Geolocated_cache in Geolocated_cache subdirectory
            Geo.process_countries_sequential()
            
            if len(out_dir_geo) == 0:               #check to see whether the Geolocated Articles have populated
                print("Error adding Articles to Geolocated_cache subdirectory")
                return
            elif len(out_dir_geo) >= 1:
                print("Files present in Geolocate_cache subdirectory")                           
            
            #at this point no need for articles in Article_cache thus they can be deleted
            DB_Manager_NEWS.delete_article_cache()
            
        
        except Exception as e:          #if error encountered print message to the terminal
            print(f"[NEWS_API] Request failed in DB_Update_Collection: {e}")
            return "There was an error recieving and processing articles for DB collection update."
        
        return
    
    #Variable used to define a news point from the pulled, stored, and cleaned articles from NEWS_API
    News_Point = ("city", "country", "latitude", "longitude", "title", "url")
    
    def load_geolocated_cache_arrays(self,out_dir_geo) -> List[List[Dict]]:
        """
        Returns [file1_items[], file2_items[], ...],
        one inner list per *_geolocated.json file.
        """
        data: List[List[Dict]] = []
        
        for p in sorted(out_dir_geo.glob("CountriesGroup*_geolocated.json")):
            try:
                with p.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    data.append(data)
                else:
                    print(f"[warn] {p.name} is not a JSON array; skipped")
            except Exception as e:
                print(f"[warn] failed to read {p.name}: {e}")
        return data
    
    def norm_url(self,u: Optional[str]) -> Optional[str]:
        if not isinstance(u, str):
            return None
        return u.strip().rstrip("/")


    def fetch_DB_urls(self,db, collection_names: List[str]) -> set[str]:
        """
        Streams all docs from the given collections and returns a set of 'url' fields.
        Simple & explicit; fine unless your collections are massive.
        """
        urls: set[str] = set()
        for col in collection_names:
            for snap in db.collection(col).stream():
                d = snap.to_dict() or {}
                u = DB_Manager_NEWS.norm_url(d.get("url"))
                if u:
                    urls.add(u)
        return urls
    
    def DB_Push(self):              
        """Push new refreshed articles from Geolocated_cache into Firestore."""
        print("=== Starting Firestore push ===")

        # get server/api directory
        api_dir = Path(__file__).resolve().parent           
        out_dir_geo = api_dir / "Geolocated_cache"          

        # make connection to Firestore using firebase_admin credentials
        if not firebase_admin._apps:
            cred = credentials.Certificate(info)
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        
        # load cached geolocated articles + already recorded URLs
        cols = [f"CountriesGroup{i}" for i in range(1, 20)]
        data = self.load_geolocated_cache_arrays(out_dir_geo)
        recorded_urls = self.fetch_DB_urls(db, cols)

        seen_now = set(recorded_urls)
        created, skipped = 0, 0
        batch = db.batch()
        in_batch, batch_size = 0, 400      # commit every ~400 for safety
        col_idx = 0

        # flatten all lists (in case load_geolocated_cache_arrays returns nested arrays)
        flat_data = []
        for group in data:
            if isinstance(group, list):
                flat_data.extend(group)
            elif isinstance(group, dict):
                flat_data.append(group)

        print(f"Total candidate articles: {len(flat_data)}")
        print(f"Already in DB: {len(recorded_urls)}")

        for article in flat_data:
            url = self.norm_url(article.get("url"))
            if not url:
                continue

            if url in seen_now:
                skipped += 1
                continue

            seen_now.add(url)
            created += 1

            # rotate through the 19 collections (CountriesGroup1 → 19)
            col_name = cols[col_idx % len(cols)]
            col_idx += 1

            # make a Firestore-safe doc ID
            doc_id = url.replace("/", "_")[:500]

            ref = db.collection(col_name).document(doc_id)
            batch.set(ref, article)
            in_batch += 1

            # commit when reaching limit
            if in_batch >= batch_size:
                batch.commit()
                print(f"Committed {in_batch} new docs so far...")
                batch = db.batch()
                in_batch = 0

        # commit any remaining writes
        if in_batch > 0:
            batch.commit()
            print(f"Committed {in_batch} remaining docs.")

        print(f"=== Done pushing: {created} new, {skipped} skipped ===")
        return

    
    def DB_Pull(self):                      #function used to pull articles from collections in the database for News filter
            #refer to info dict constructed from .env variable for DB credentials to firestore
        if not firebase_admin._apps:
            cred = credentials.Certificate(info)
            firebase_admin.initialize_app(cred)
    
        #create instance of firestore DB connection
        db = firestore.client()
        
        #Create an array where each index is a collection of about 100 news articles for easier storage and easier parsing of data
        collections: List[List[Dict[str, Any]]] = []
        
        for coll in sorted(db.collections(), key=lambda c: c.id):   # stable order
            items: List[Dict[str, Any]] = []                        #specify all news points within a colleciton as an item
            
            for snap in db.collection(coll.id).stream():            # all docs in this collection
                data = snap.to_dict() or {}
                items.append(data)


            collections.append(items)
        
        return collections      #return the constructed array with all the json data
    
    def delete_article_cache(self):                 #function to delete files in Article_cache server/api/Article_cache once files are processed
        api_dir = Path(__file__).resolve().parent           #get server/api directory
        out_dir = api_dir / "Article_cache"                 #add on Article_cache subdirectory to path
        for p in out_dir.glob("CountriesGroup*.json"):
            p.unlink(missing_ok=True)
        print("Article_cache cleared.")
        
    def delete_geolocated_cache(self):
        api_dir = Path(__file__).resolve().parent           #get server/api directory
        out_dir = api_dir / "Geolocated_cache"                 #add on Article_cache subdirectory to path
        for p in out_dir.glob("CountriesGroup*_geolocated.json"):
            p.unlink(missing_ok=True)
        print("Geolocated_cache cleared.")
    
class Geolocator(ExternalAPI):                  #class that will be used for geolocation of articles
    # -----------------------------------------------------------------------------
    # Configuration
    # -----------------------------------------------------------------------------
    #declaration of required global values needed
    server_api_dir = Path(__file__).resolve().parent          # -> get the /server/api directory
    
    INPUT_DIR = server_api_dir / "Article_cache"                # -> add subdirectory to make /server/api/Article_cache path     # folder where CountriesGroupX.json files are stored
    OUTPUT_DIR = server_api_dir / "Geolocated_cache"            # -> add subdirectory to make /server/api/Geolocated_cache path     #folder where the Geolocated articles will be stored
    START_FILE = 1
    END_FILE = 19
    THROTTLE = 0.6                 # seconds between articles (Nominatim safe)
    VERBOSE = False                # True = detailed logs

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    
    # Geopy Nominatim (ALWAYS set a meaningful/unique user_agent for your app) // rate limit should be fine with 1 request/second
    _geolocator = Nominatim(user_agent="article_geolocator_ajs0576_v1")

    def _geocode_with_timeout(self,q):
        # 8–12 seconds is reasonable; 10 is a sweet spot
        return Geolocator._geolocator.geocode(q, timeout=10)

    _forward_geocode = RateLimiter(
        _geocode_with_timeout,
        min_delay_seconds=1.2,        # was 1.0
        max_retries=3,                # was 2 or default
        error_wait_seconds=4.0,       # wait between retries
        swallow_exceptions=True
    )


    # default to this url if not able to geolocate: ipinfo.io (no key needed for basic free usage; rate limits apply)
    _IPINFO_URL = "https://ipinfo.io/{ip}/json"
    

    PUBLISHER_FALLBACK: Dict[str, Tuple[str, str]] = {
        "economictimes.indiatimes.com": ("Mumbai", "India"),
        "indiatimes.com":               ("Mumbai", "India"),
        "timesofindia.com":             ("Mumbai", "India"),
        "livemint.com":                 ("New Delhi", "India"),
        "thehindu.com":                 ("Chennai", "India"),
        "thehindubusinessline.com":     ("Chennai", "India"),
        "indianexpress.com":            ("New Delhi", "India"),
        "rediff.com":                   ("Mumbai", "India"),
        "variety.com":                  ("Los Angeles", "United States"),
        "irishtimes.com":               ("Dublin", "Ireland"),
        "financialpost.com":            ("Toronto", "Canada"),
        "digitaljournal.com":           ("Toronto", "Canada"),
        "abc.net.au":                   ("Sydney", "Australia"),
        "sputnikglobe.com":             ("Moscow", "Russia"),
        "yahoo.com":                    ("New York", "United States"),
        "huffpost.com":                 ("New York", "United States"),
    }

    # TLD → country (used when nothing else works)
    TLD_COUNTRY: Dict[str, str] = {
        "in": "India",
        "us": "United States",
        "au": "Australia",
        "ie": "Ireland",
        "ca": "Canada",
        "ru": "Russia",
        "uk": "United Kingdom",
        "cn": "China",
        "ph": "Philippines",
    }
    
    
    #helper functions used to make handling of data easier
    def _p(self,verbose: bool, *args) -> None:
        if verbose:
            print(*args, flush=True)

    def _round4(self,x: Optional[float]) -> Optional[float]:
        try:
            return round(float(x), 4) if x is not None and not math.isnan(float(x)) else None
        except Exception:
            return None

    def _domain_parts(self,url: str) -> Tuple[str, str, str]:
        """
        Returns (full_host, registered_domain, suffix).
        For https://economictimes.indiatimes.com/...:
        full_host        = 'economictimes.indiatimes.com'
        registered_domain= 'indiatimes.com'
        suffix           = 'com'
        """
        ext = tldextract.extract(url)
        full_host = ".".join([p for p in (ext.subdomain, ext.domain, ext.suffix) if p]).lower()
        registered = (ext.registered_domain or "").lower()
        suffix = (ext.suffix or "").lower()
        return full_host, registered, suffix

    # -----------------------------------------------------------------------------
    # Functions needed for Tier 1 search on Wikipedia: Wikidata — website (P856) → HQ (P159) → coords (P625)
    # -----------------------------------------------------------------------------
    _WD_SPARQL = "https://query.wikidata.org/sparql"
    _cache_wd: Dict[str, Tuple[Optional[str], Optional[str], Optional[float], Optional[float]]] = {}

    def wikidata_hq_lookup_by_site_fragment(self,fragment: str, verbose: bool=False) -> Tuple[Optional[str], Optional[str], Optional[float], Optional[float]]:
        """
        Try to find publisher HQ city/country (+coords) via Wikidata given a website fragment.
        Returns (hq_label, country_label, lat, lon) — any may be None.
        """
        #if fragment in _cache_wd:
        #    _p(verbose, f"    [wd] cache HIT for '{fragment}'")
        #    return _cache_wd[fragment]
        hit = Geolocator._wd_cache_get(fragment)
        if hit is not None:
            Geolocator._p(verbose, f"    [wd] cache HIT for '{fragment}'")
            return hit

        query = f"""
        SELECT ?hqLabel ?hqCountryLabel ?coord WHERE {{
        ?org wdt:P856 ?site .
        FILTER(CONTAINS(LCASE(STR(?site)), "{fragment.lower()}"))
        OPTIONAL {{ ?org wdt:P159 ?hq . }}
        OPTIONAL {{ ?hq wdt:P625 ?coord . }}
        OPTIONAL {{
            ?hq wdt:P17 ?hqCountry .
        }}
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }} LIMIT 1
        """
        try:
            r = requests.get(Geolocator._WD_SPARQL, params={"query": query, "format":"json"}, timeout=25)
            r.raise_for_status()
            rows = r.json().get("results", {}).get("bindings", [])
            if rows:
                row = rows[0]
                hq_label = row.get("hqLabel", {}).get("value")
                hq_country = row.get("hqCountryLabel", {}).get("value")
                coord = row.get("coord", {}).get("value")  # "Point(lon lat)"
                lat = lon = None
                if coord:
                    lon_s, lat_s = coord.replace("Point(", "").replace(")", "").split()
                    lat, lon = Geolocator._round4(float(lat_s)), Geolocator._round4(float(lon_s))
                Geolocator._cache_wd[fragment] = (hq_label, hq_country, lat, lon)
                return Geolocator._cache_wd[fragment]
        except Exception as e:
            Geolocator._p(verbose, f"    [wd][ERR] {e}")

        Geolocator._cache_wd[fragment] = (None, None, None, None)
        return Geolocator._cache_wd[fragment]

    def wikidata_hq_lookup(self,url: str, verbose: bool=False) -> Tuple[Optional[str], Optional[str], Optional[float], Optional[float]]:
        """
        Try full host first, then registered domain.
        """
        full_host, registered, _ = Geolocator._domain_parts(url)
        hq_label, hq_country, lat, lon = Geolocator.wikidata_hq_lookup_by_site_fragment(full_host, verbose=verbose)
        if any([hq_label, hq_country, lat, lon]):
            return hq_label, hq_country, lat, lon
        return Geolocator.wikidata_hq_lookup_by_site_fragment(registered, verbose=verbose)

    # -----------------------------------------------------------------------------
    # Function neeeded for Tier 2 search on organization homepage: Parse homepage JSON-LD for address (city/country)
    # -----------------------------------------------------------------------------
    def ldjson_address(self,url: str, verbose: bool=False) -> Tuple[Optional[str], Optional[str]]:
        """
        Fetch publisher homepage and parse JSON-LD looking for address fields.
        Returns (city, country) if found; else (None, None).
        """
        try:
            Geolocator._p(verbose, f"    [ldjson] fetching homepage → {url}")
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            base_url = get_base_url(r.text, url)
            data = extruct.extract(r.text, base_url=base_url, syntaxes=['json-ld'])
            for item in data.get('json-ld', []):
                if not isinstance(item, dict):
                    continue
                # Common places: Organization, NewsMediaOrganization, LocalBusiness, etc.
                if item.get("@type") in ("Organization", "NewsMediaOrganization", "Corporation", "LocalBusiness"):
                    addr = item.get("address") or {}
                    # address may itself be a dict or list of dicts
                    if isinstance(addr, dict):
                        city = addr.get("addressLocality")
                        country = addr.get("addressCountry")
                        if city or country:
                            return city, country if isinstance(country, str) else (country.get("name") if isinstance(country, dict) else country)
                    elif isinstance(addr, list):
                        for a in addr:
                            if isinstance(a, dict):
                                city = a.get("addressLocality")
                                country = a.get("addressCountry")
                                if city or country:
                                    return city, country if isinstance(country, str) else (country.get("name") if isinstance(country, dict) else country)
        except Exception as e:
            Geolocator._p(verbose, f"    [ldjson][ERR] {e}")
        return None, None
    
    # -----------------------------------------------------------------------------
    # Function needed for Tier 3 search using IP address matching: IP-based location (uses IP address to get a rough server location)
    # -----------------------------------------------------------------------------
    
    def ip_geolocate_domain(self,domain: str, verbose: bool=False) -> Tuple[Optional[str], Optional[str], Optional[float], Optional[float]]:
        """
        Resolve domain → IP, then query ipinfo.io for rough (city,country,lat,lon).
        This is server/CDN location (not necessarily newsroom HQ).
        """
        try:
            ip = socket.gethostbyname(domain)
            Geolocator._p(verbose, f"    [ipgeo] {domain} → {ip}")
            resp = requests.get(Geolocator._IPINFO_URL.format(ip=ip), timeout=10)
            
            #proceed if we get a valid IP address
            if resp.ok:
                data = resp.json()
                city = data.get("city")
                country = data.get("country")
                loc = data.get("loc")  # "lat,lon"
                lat = lon = None
                if loc:
                    lat_s, lon_s = loc.split(",")
                    lat, lon = Geolocator._round4(float(lat_s)), Geolocator._round4(float(lon_s))
                return city, country, lat, lon
        except Exception as e:
            Geolocator._p(verbose, f"    [ipgeo][ERR] {e}")
        return None, None, None, None
    
    # -----------------------------------------------------------------------------
    # geopy (coordinate engine) helpers 
    # -----------------------------------------------------------------------------
    
    def _geopy_throttled_geocode(self,q):
        """Thread-safe global throttle for geopy geocoding."""
        global _last_geopy_ts
        with _geopy_lock:
            now = monotonic()
            wait = _GEOPY_MIN_INTERVAL - (now - _last_geopy_ts)
            if wait > 0:
                time.sleep(wait)
            # call underlying (already rate-limited) geopy
            loc = Geolocator._forward_geocode(q)
            _last_geopy_ts = monotonic()
            return loc

    # Replace geocode_place to use the global throttle (thread-safe)
    def geocode_place(self,place: str, verbose: bool=False) -> Tuple[Optional[float], Optional[float]]:
        if not place:
            return None, None
        try:
            loc = Geolocator._geopy_throttled_geocode(place)
            if loc:
                lat, lon = Geolocator._round4(loc.latitude), Geolocator._round4(loc.longitude)
                Geolocator._p(verbose, f"    [geopy] '{place}' → {lat},{lon}")
                return lat, lon
        except Exception as e:
            Geolocator._p(verbose, f"    [geopy][ERR] {e}")
        return None, None

    # Wrap cache reads/writes that multiple threads may touch
    def _wd_cache_get(self,k):
        with _cache_lock:
            return Geolocator._cache_wd.get(k)
    def _wd_cache_set(self,k, v):
        with _cache_lock:
            Geolocator._cache_wd[k] = v

    def geocode_place(self,place: str, verbose: bool=False) -> Tuple[Optional[float], Optional[float]]:
        """
        Use geopy.Nominatim to resolve a place string to (lat,lon).
        """
        if not place:
            return None, None
        try:
            loc = Geolocator._forward_geocode(place)
            if loc:
                lat, lon = Geolocator._round4(loc.latitude), Geolocator._round4(loc.longitude)
                Geolocator._p(verbose, f"    [geopy] '{place}' → {lat},{lon}")
                return lat, lon
        except Exception as e:
            Geolocator._p(verbose, f"    [geopy][ERR] {e}")
        return None, None
    
    # -----------------------------------------------------------------------------
    # Resolver function for a single article using 3-tiered approach (tiered domain→(city,country), then geopy→coords)
    # -----------------------------------------------------------------------------
    
    def resolve_article(self,article: Dict[str, Any], verbose: bool=False) -> Dict[str, Any]:
        """
        Resolve city,country for the publisher domain using the tiered approach.
        Then use geopy to turn that into (lat,lon). Returns EXACT schema dict.
        """
        url = article.get("url")
        title = article.get("title")
        input_country = article.get("country")
        city = None
        country = None
        lat = None
        lon = None

        Geolocator._p(verbose, f"\n[Article] {title}")
        Geolocator._p(verbose, f"  URL: {url}")
        full_host, registered, suffix = Geolocator._domain_parts(url)
        homepage = f"https://{registered}" if registered else url

        # Quick publisher map (if you have lots from same sites, this is fastest)
        if full_host in Geolocator.PUBLISHER_FALLBACK:
            city, country = Geolocator.PUBLISHER_FALLBACK[full_host]
            Geolocator._p(verbose, f"  hit PUBLISHER_FALLBACK full_host → {city}, {country}")
        elif registered in Geolocator.PUBLISHER_FALLBACK:
            city, country = Geolocator.PUBLISHER_FALLBACK[registered]
            Geolocator._p(verbose, f"  hit PUBLISHER_FALLBACK registered → {city}, {country}")

        # Tier 1: Wikidata (if still unknown)
        if not city and not country:
            Geolocator._p(verbose, "  [Tier1] Wikidata lookup ...")
            hq_label, hq_country, wd_lat, wd_lon = Geolocator.wikidata_hq_lookup(url, verbose=verbose)
            if hq_label or hq_country or (wd_lat and wd_lon):
                city = city or hq_label
                country = country or hq_country
                if wd_lat is not None and wd_lon is not None:
                    lat, lon = wd_lat, wd_lon
                    Geolocator._p(verbose, f"    Wikidata coords → {lat},{lon}")
                else:
                    Geolocator._p(verbose, f"    Wikidata names → city='{city}', country='{country}'")

        # Tier 2: JSON-LD on homepage (if still unknown city/country)
        if not city and not country:
            Geolocator._p(verbose, "  [Tier2] Homepage JSON-LD ...")
            c_city, c_country = Geolocator.ldjson_address(homepage, verbose=verbose)
            if c_city or c_country:
                city = city or c_city
                country = country or c_country
                Geolocator._p(verbose, f"    JSON-LD → city='{city}', country='{country}'")

        # Tier 3: IP-based geolocation (last-resort for names)
        if not city and not country:
            Geolocator._p(verbose, "  [Tier3] IP-based geolocation ...")
            ip_city, ip_country, ip_lat, ip_lon = Geolocator.ip_geolocate_domain(registered or full_host, verbose=verbose)
            if ip_city or ip_country:
                city = city or ip_city
                country = country or ip_country
                Geolocator._p(verbose, f"    IPGeo → city='{city}', country='{country}'")
            # If coords arrived here and nothing else will, we can accept them
            if lat is None and lon is None and ip_lat is not None and ip_lon is not None:
                lat, lon = ip_lat, ip_lon
                Geolocator._p(verbose, f"    IPGeo coords → {lat},{lon}")

        # Additional hints: provided article["country"]
        if not country and input_country:
            country = input_country
            Geolocator._p(verbose, f"  using input country hint → '{country}'")

        # TLD heuristic (e.g. .in → India) if still nothing
        if not country and suffix in Geolocator.TLD_COUNTRY:
            country = Geolocator.TLD_COUNTRY[suffix]
            Geolocator._p(verbose, f"  TLD heuristic '.{suffix}' → country='{country}'")

        # Absolute default if still missing
        if not city and not country:
            city, country = "Washington", "United States"
            Geolocator._p(verbose, "  DEFAULT → Washington, United States")

        # Get coordinates (use geopy if we only have names; keep Wikidata/IP coords if already present)
        if lat is None or lon is None:
            q = None
            if city and country:
                q = f"{city}, {country}"
            elif country:
                q = country
            else:
                q = "United States"
            lat, lon = Geolocator.geocode_place(q, verbose=verbose)

        # Final safety (should be rare)
        if lat is None or lon is None:
            # As a very last attempt, geocode country alone or default to US
            q = country or "United States"
            lat, lon = Geolocator.geocode_place(q, verbose=verbose)
            if lat is None or lon is None:
                city, country, lat, lon = "Washington", "United States", 38.9072, -77.0369

        return {
            "city": city or "Unknown",
            "url": url,
            "title": title,
            "country": country or "Unknown",
            "latitude": Geolocator._round4(lat),
            "longitude": Geolocator._round4(lon),
        }
        
    # -----------------------------------------------------------------------------
    # Batch processor function used to geolocate all articles in a file of interest (threaded for 4 PROCESSES AT THE MOMENT)
    # -----------------------------------------------------------------------------
        #When changing number of threads, simply change the int in max_workers argument in the function (by default set to 4)
        
    def geolocate_articles_json_concurrent(self, articles: List[Dict[str, Any]], max_workers: int = 4, verbose: bool = False) -> List[Dict[str, Any]]:
        """
        Concurrent version:
        - Runs resolve_article() in a thread pool.
        - Enforces a global geopy throttle (1 req/sec across all threads).
        - Keeps output order identical to input.
        """
        n = len(articles)
        Geolocator._p(verbose, f"=== Geolocator start (concurrent, n={n}, workers={max_workers}) ===")

        # submit jobs with their original index so we can restore order
        results: List[Optional[Dict[str, Any]]] = [None] * n
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {ex.submit(Geolocator.resolve_article, art, verbose): i for i, art in enumerate(articles)}
            for fut in as_completed(futures):
                i = futures[fut]
                try:
                    results[i] = fut.result()
                except Exception as e:
                    # On failure, write a minimal placeholder so array shape is preserved
                    a = articles[i]
                    Geolocator._p(verbose, f"[ERR] article {i+1}: {e}")
                    results[i] = {
                        "city": "Unknown",
                        "url": a.get("url"),
                        "title": a.get("title"),
                        "country": a.get("country") or "Unknown",
                        "latitude": None,
                        "longitude": None,
                    }

        Geolocator._p(verbose, "=== Geolocator finish (concurrent) ===")
        # type: ignore (we always fill)
        return results  # type: ignore
        
        
    #function used to start the process of Geolocation after Article_cache subdirectory is populated   
    def process_countries_sequential():
        print("\n🌍 Starting sequential geolocation run\n")

        for idx in range(Geolocator.START_FILE, Geolocator.END_FILE + 1):
            filename = f"CountriesGroup{idx}.json"
            input_path = os.path.join(Geolocator.INPUT_DIR, filename)
            output_path = os.path.join(Geolocator.OUTPUT_DIR, filename.replace(".json", "_geolocated.json"))

            # Skip if missing
            if not os.path.exists(input_path):
                print(f"⚠️  Skipping {filename} — file not found.")
                continue

            print(f"\n🟢 [{idx}/{Geolocator.END_FILE}] Processing {filename} ...")
            start_time = time.time()

            try:
                with open(input_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if not isinstance(data, list):
                    print(f"  ⚠️  {filename} is not a JSON list — skipping.")
                    continue

                enriched = Geolocator.geolocate_articles_json_concurrent(data, max_workers=4, verbose=Geolocator.VERBOSE)

                with open(output_path, "w", encoding="utf-8") as out:
                    json.dump(enriched, out, ensure_ascii=False, indent=2)

                duration = round(time.time() - start_time, 1)
                print(f"  ✅ Finished {filename} in {duration}s → {output_path}")

            except json.JSONDecodeError:
                print(f"  ❌ JSON parse error in {filename} — skipping.")
            except Exception as e:
                print(f"  ❌ Unexpected error in {filename}: {e}")

        print("\n🏁 Sequential geolocation complete.\n")