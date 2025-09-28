import time
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import WeatherAPIAsync, PrecipitationAPIAsync
import asyncio

from api.models import FlightModel
from api.serializers import FlightSerializer
from api.services import FlightAPI,NEWS_API     #,Gemini_API,

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
            grid = asyncio.run(api.fill_grid_async(force_refresh=refresh))

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
                    return Response({"error": "No Country Passed/detected"},status=status.HTTP_400_BAD_REQUEST)

                RAW_articles = self.NEWS.GatherArticles(CountryChoice)

                result = self.NEWS.Parse_Spit(RAW_articles)
                
                #error checking for News_API to see if correct output was recieved
                if result.get("error"):
                    return Response(result, status=status.HTTP_502_BAD_GATEWAY)     #flag if invalid output was recieved
                
                return Response(result, status=status.HTTP_200_OK)      #return good output if nothing wrong was detected

#TODO: MAKE ANOTHER VIEW THAT DOES THE TRAVEL INFORMATION AS WELL.
#prompt = f"the country in question is {country}. ONLY RETURN a list of important documents needed for travel to the country!" #reformat the recieved county into the prompt for the model

class Heatmap(APIView):
    
    NEWS = NEWS_API()
    
    def get(self,request,format=None):             #GET request for all the articles needed to populate congestion
        #in future: optimize to also account for first_20, second_20, etc.
        Mass_Articles = self.NEWS.NewsPointBuilder(self.NEWS.first_20)
        
        return Response(Mass_Articles, status=status.HTTP_200_OK)           #return the points after successful data gathering
        

class Agent(APIView):
    
    def post(self,request,format=None):
        return