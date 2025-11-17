import time
import threading
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import WeatherAPIAsync, PrecipitationAPIAsync
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
        
        while True:
            try:
                time.sleep(600)  # wait 10 minutes before first refresh
                print("[Background] Starting periodic article refresh...")
                self.NEWS.Gather_DB_for_Save()     # fetch and geolocate new articles
                self.DB.GetNew_Articles()          #Geolocate new articles in server/api/Article_cache and store them to server/api/Geolocated_cache
                
                self.DB.DB_Push()             # push only new ones to Firestore
                
                self.DB.delete_geolocated_cache()           #delete the articles in the cache to free up space in the server
                print("[Background] Refresh complete. Waiting 1 hour...")
                
            except Exception as e:
                print(f"[Background] Error during refresh: {e}")
            time.sleep(3600)  # wait 1 hour before repeating
    
    
    def get(self,request,format=None):             #GET request for all the articles needed to populate congestion
        Mass_Articles = []
        
        '''# --- start background refresh thread  ---
        if not hasattr(self, "refresh_thread") or not self.refresh_thread.is_alive():
            self.refresh_thread = threading.Thread(target=self.Start_DB_refresh, daemon=True)
            self.refresh_thread.start()
            print("[Heatmap] Background refresh thread started for DB.")

        
        #This section of the code gathers all the articles Mass_Articles and returns it to the frontend
        try:
            Mass_Articles = self.DB.DB_Pull()               #gather all the articles currently in the collections of DB
        
        except Exception as e:
            print(f"Error encountered during DB_Pull: {e}")
            Mass_Articles = None        #set to none to execute default code
        
        if Mass_Articles is None:    '''   #default to following pre-defined json data if data doesn't load
            
        Mass_Articles[0] = data_1
        
        Mass_Articles[1] = data_2
            
        '''else:
            print("Data from firebase collections retrieved successfully!")'''

        #This section of code calls for new articles to be pulled and updated to database (Not Returned to Frontend)
        
        
        #print first retrieved json file from firebae upon successful retrieval of data!!! 
        #(revert to static JSON array in event that firebase code does not return any values to give illusion of functional filter)
        #Display error message to terminal in case we don't have a successulf DB call
        
        print(f"{Mass_Articles[0]}")
        

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

