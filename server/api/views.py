import threading
_refresh_thread_started = False
_refresh_thread_lock = threading.Lock()
_refresh_is_running = threading.Lock()                  # lock to prevent overlapping the thread upon refreshing the filter
_stop_event = threading.Event()                         # stops thread gracefully


import time
import os
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import WeatherAPIAsync, PrecipitationAPIAsync
from django.conf import settings        #settings imported for thread management
import asyncio

from api.models import FlightModel
from api.serializers import FlightSerializer
from api.services import FlightAPI,NEWS_API,Agentic_AI, DisasterAPI, DB_Manager_NEWS    #,Gemini_API,


from api.variables import data_1, data_2


class FlightList(APIView):
    """
    Handles the connection to the external flight API
    """
    api = FlightAPI()

    # TODO: find a way to update the db effeciently using the serializer, maybe move the database updating to the services file to update and send in one go
    def get(self, request, format=None):
        #last_mod = self.api.get_last_modified()
        flights = self.api.fetch_data()
        return Response(flights, status=status.HTTP_200_OK)


                #return Response({"response":result})


class WeatherGridView(APIView):
    """
    Fills and returns a 2D temperature grid based on OpenWeatherMap (async version)
    """

    def get(self, request, format=None):
        try:
            api = WeatherAPIAsync()

            # Read query parameter: ?refresh=true
            refresh = request.GET.get("refresh", "false").lower() == "true"

            # Run the async grid filler with refresh flag
            grid = asyncio.run(api.fill_grid_async())

            return Response({
                "lon": api.rows,
                "lat": api.cols,
                "data": grid
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print("WeatherGridView error:", e)
            return Response({"error": str(e)}, status=500)

class PrecipitationGridView(APIView):
    def get(self, request, format=None):
        try:
            api = PrecipitationAPIAsync()
            refresh = request.GET.get("refresh", "false").lower() == "true"
            grid = asyncio.run(api.fill_grid_async(force_refresh=refresh))

            return Response({
                "lon": api.rows,
                "lat": api.cols,
                "data": grid
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print("PrecipitationGridView error:", e)
            return Response({"error": str(e)}, status=500)

class CountryNews(APIView):                #handles connection to external API for AI interaction

        #AI_Gemini = Gemini_API()
        NEWS = NEWS_API()

        def post(self,request,format=None):                             #this method is used to post the initial travel prompt to the GPT_API
                CountryChoice = request.data.get("country")             #from the post request sent fron AISummary.jsx read in the country value and store it.
                
                if not CountryChoice:
                    return Response({"error": "No Country Passed/detected for CountryNews(APIView)"},status=status.HTTP_400_BAD_REQUEST)

                
                
                RAW_articles = self.NEWS.GatherArticles(CountryChoice)

                result = self.NEWS.Parse_Spit(RAW_articles)

                #error checking for News_API to see if correct output was recieved
                if result.get("error"):
                    return Response(result, status=status.HTTP_502_BAD_GATEWAY)     #flag if invalid output was recieved

                return Response(result, status=status.HTTP_200_OK)      #return good output if nothing wrong was detected

#TODO: MAKE ANOTHER VIEW THAT DOES THE TRAVEL INFORMATION AS WELL.
#prompt = f"Plain text, no markdown.the country in question is {country}. ONLY RETURN a list of important documents needed for travel to the country!" #reformat the recieved county into the prompt for the model

class Heatmap(APIView):

    NEWS = NEWS_API()               #Initiate the instance of the NEWS_API class for NEWS API article gathering
    DB = DB_Manager_NEWS()          #Initiate the instance o the DB_Manager_NEWS  for Database communication
    
    def Start_DB_refresh(self):
        #run funciton to push new geolocated articles after an hour of use
        
        if not _stop_event.wait(timeout = 10):     #wait 10 secs before starting first refresh
            pass
        
        while not _stop_event.is_set():
            
            if _refresh_is_running.acquire(blocking = False):       #ensure that there aren't overlapping threads (don't run 2 threads at the same time)
                try:
                    # NOTE: refresh the DB once every hour 
                    
                    print("[Background] Starting periodic article refresh...")
                    
                    self.DB.GetNew_Articles()          #Geolocate new articles in server/api/Article_cache and store them to server/api/Geolocated_cache, also start the Gather_DB_for_save() function
                    
                    self.DB.DB_Push()             # push only new ones to Firestore
                    
                    self.DB.delete_geolocated_cache()           #delete the articles in the cache to free up space in the server
                    print("[Background] Refresh complete. Waiting 1 hour...")
                    
                except Exception as e:
                    print(f"[Background] Error during refresh: {e}")
                
                finally:
                    _refresh_is_running.release()
                
            _stop_event.wait(timeout = 3600)  # wait 1 hour before repeating
    
    def _ensure_refresh_thread(self):
        global _refresh_thread_started
        with _refresh_thread_lock:
            if not _refresh_thread_started:
                # In Django dev server, the auto-reloader runs code twice.
                # Only start in the main process.
                if os.environ.get("RUN_MAIN") == "true" or not settings.DEBUG:
                    t = threading.Thread(target=self.Start_DB_refresh, daemon=True)
                    t.start()
                    _refresh_thread_started = True
                    print("[Heatmap] Background refresh thread started for DB.")
    
    def get(self,request,format=None):             #GET request for all the articles needed to populate congestion
        
        #self._ensure_refresh_thread()           #start the refresh thread once
        
        Mass_Articles = []

        #This section of the code gathers all the articles Mass_Articles and returns it to the frontend
        try:
            Mass_Articles = self.DB.DB_Pull()               #gather all the articles currently in the collections of DB
        
        except Exception as e:
            print(f"Error encountered during DB_Pull: {e}")
            Mass_Articles = None        #set to none to execute default code
        
        if Mass_Articles is None:       #default to following pre-defined json data if data doesn't load 
            Mass_Articles[data_1, data_2]           #import data from 2 collections in variables.py in event that DB calls are unsuccessful so the application looks funcitonally correct
            
        else:
            print("\nData from firebase collections retrieved successfully!\n\n")
        
        #In event that future debugging needs to be conducted, but datapoints want to be accessed without conducting database calls, comment DB functions in Heatmap class and uncomment the code block directly below    
        '''
        Mass_Articles.insert(0, data_1)
        Mass_Articles.insert(1, data_2)
        #Display error message to terminal in case we don't have a successulf DB call
        print(f"{Mass_Articles[0][0]}\n\n{Mass_Articles[1][0]}")        
        '''

            #This section of code calls for new articles to be pulled and updated to database (Not Returned to Frontend)
            
            
            #print first retrieved json file from firebae upon successful retrieval of data!!! 
            #(revert to static JSON array in event that firebase code does not return any values to give illusion of functional filter)

            
            
        print(f"{Mass_Articles[0][0]}\n\n{Mass_Articles[1][0]}\n\n{Mass_Articles[2][0]}\n\n{Mass_Articles[3][0]}\n\n")
        

        return Response(Mass_Articles, status=status.HTTP_200_OK)           #return the points after successful data gathering


class Agent(APIView):

    api = Agentic_AI()          #make instance of the Agentic AI class to use in the frontend

    def post(self,request,format=None):
        #print recieved data from post request of frontend
        print("request.data:", request.data)

        CountryChoice = request.data.get("country")             #from the post request sent fron AISummary.jsx read in the country value and store it.
        SessionNum = request.data.get("session")
        SelectedFilter = request.data.get("FilterSelected")             #retrieve name of the filter currently selected


        #print values to terminal to verify were recieved
        print(f"CountryChoice: {CountryChoice}\nSessionNum: {SessionNum}\nSelectedFilter: {SelectedFilter}")

        if not CountryChoice:
            return Response({"error": "No Country Passed/detected for Agent(APIView). REQUIRED AS IT IS ESSENTIAL PARAMETER FOR AGENT FUNCTIONALITY"},status=status.HTTP_400_BAD_REQUEST)

        
        if SelectedFilter ==  None:             #on even that no filter is selected provide a holistic view
            result = self.api.Holistic_View(CountryChoice)    #,SessionNum      #make call for the Holistic_View of the AI_Agent

        elif SelectedFilter == "Flights":       #set results to a summary of flight data from the AI
            result = self.api.Flight_Trend_Gather(CountryChoice)    
            
        elif SelectedFilter == "Disasters":         #set results to a summary of flight data from the AI
            result = self.api.Disaster_Gather(CountryChoice)    
        
        elif SelectedFilter == "Temperature":           #set results to a summary of Temperature specific weather data from the AI
            result = self.api.Temperature_Weather_Gather(CountryChoice)        
            
        elif SelectedFilter == "Precipitation":         #set results to a summary of Percipitation specific weather data from the AI
            result = self.api.Percipitation_Weather_Gather(CountryChoice)  
            
        elif SelectedFilter == "News":        #set results to a summary of current News trends from the AI
            result = self.api.News_Gather(CountryChoice)
        
        #print out the response just to make sure it was recieved properly
        print(f"{result}")

        return Response(result, status=status.HTTP_200_OK)      #return good output if nothing wrong was detected

class DisasterList(APIView):
    """
    Handles the connection to the external disaster api
    """
    api = DisasterAPI()

    def get(self, request, format=None):
        disasters = self.api.fetch_data()
        return Response(disasters, status=status.HTTP_200_OK)

