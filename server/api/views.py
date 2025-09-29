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
        
        
        
        #Would Work, but NEWS API wants $500 USD monthly.... we are figuring out a workaround
        #Mass_Articles = self.NEWS.NewsPointBuilder(self.NEWS.first_20)
        
        Mass_Articles = [
            { "city": "Berlin", "url": "https://example.com/news/berlin", "title": "Berlin update", "country": "Germany", "latitude": 52.5200, "longitude": 13.4050 },
            { "city": "Munich", "url": "https://example.com/news/munich", "title": "Munich update", "country": "Germany", "latitude": 48.1374, "longitude": 11.5755 },
            { "city": "Hamburg", "url": "https://example.com/news/hamburg", "title": "Hamburg update", "country": "Germany", "latitude": 53.5511, "longitude": 9.9937 },
            { "city": "Paris", "url": "https://example.com/news/paris", "title": "Paris update", "country": "France", "latitude": 48.8566, "longitude": 2.3522 },
            { "city": "Lyon", "url": "https://example.com/news/lyon", "title": "Lyon update", "country": "France", "latitude": 45.7640, "longitude": 4.8357 },
            { "city": "Marseille", "url": "https://example.com/news/marseille", "title": "Marseille update", "country": "France", "latitude": 43.2965, "longitude": 5.3698 },
            { "city": "Madrid", "url": "https://example.com/news/madrid", "title": "Madrid update", "country": "Spain", "latitude": 40.4168, "longitude": -3.7038 },
            { "city": "Barcelona", "url": "https://example.com/news/barcelona", "title": "Barcelona update", "country": "Spain", "latitude": 41.3851, "longitude": 2.1734 },
            { "city": "Valencia", "url": "https://example.com/news/valencia", "title": "Valencia update", "country": "Spain", "latitude": 39.4699, "longitude": -0.3763 },
            { "city": "Rome", "url": "https://example.com/news/rome", "title": "Rome update", "country": "Italy", "latitude": 41.9028, "longitude": 12.4964 },
            { "city": "Milan", "url": "https://example.com/news/milan", "title": "Milan update", "country": "Italy", "latitude": 45.4642, "longitude": 9.1900 },
            { "city": "Naples", "url": "https://example.com/news/naples", "title": "Naples update", "country": "Italy", "latitude": 40.8518, "longitude": 14.2681 },
            { "city": "London", "url": "https://example.com/news/london", "title": "London update", "country": "United Kingdom", "latitude": 51.5074, "longitude": -0.1278 },
            { "city": "Manchester", "url": "https://example.com/news/manchester", "title": "Manchester update", "country": "United Kingdom", "latitude": 53.4808, "longitude": -2.2426 },
            { "city": "Edinburgh", "url": "https://example.com/news/edinburgh", "title": "Edinburgh update", "country": "United Kingdom", "latitude": 55.9533, "longitude": -3.1883 },
            { "city": "New York", "url": "https://example.com/news/new-york", "title": "New York update", "country": "United States", "latitude": 40.7128, "longitude": -74.0060 },
            { "city": "San Francisco", "url": "https://example.com/news/san-francisco", "title": "San Francisco update", "country": "United States", "latitude": 37.7749, "longitude": -122.4194 },
            { "city": "Chicago", "url": "https://example.com/news/chicago", "title": "Chicago update", "country": "United States", "latitude": 41.8781, "longitude": -87.6298 },
            { "city": "Toronto", "url": "https://example.com/news/toronto", "title": "Toronto update", "country": "Canada", "latitude": 43.6532, "longitude": -79.3832 },
            { "city": "Vancouver", "url": "https://example.com/news/vancouver", "title": "Vancouver update", "country": "Canada", "latitude": 49.2827, "longitude": -123.1207 },
            { "city": "Montreal", "url": "https://example.com/news/montreal", "title": "Montreal update", "country": "Canada", "latitude": 45.5017, "longitude": -73.5673 },
            { "city": "Tokyo", "url": "https://example.com/news/tokyo", "title": "Tokyo update", "country": "Japan", "latitude": 35.6762, "longitude": 139.6503 },
            { "city": "Osaka", "url": "https://example.com/news/osaka", "title": "Osaka update", "country": "Japan", "latitude": 34.6937, "longitude": 135.5023 },
            { "city": "Kyoto", "url": "https://example.com/news/kyoto", "title": "Kyoto update", "country": "Japan", "latitude": 35.0116, "longitude": 135.7681 },
            { "city": "Seoul", "url": "https://example.com/news/seoul", "title": "Seoul update", "country": "South Korea", "latitude": 37.5665, "longitude": 126.9780 },
            { "city": "Busan", "url": "https://example.com/news/busan", "title": "Busan update", "country": "South Korea", "latitude": 35.1796, "longitude": 129.0756 },
            { "city": "Singapore", "url": "https://example.com/news/singapore", "title": "Singapore update", "country": "Singapore", "latitude": 1.3521, "longitude": 103.8198 },
            { "city": "Sydney", "url": "https://example.com/news/sydney", "title": "Sydney update", "country": "Australia", "latitude": -33.8688, "longitude": 151.2093 },
            { "city": "Melbourne", "url": "https://example.com/news/melbourne", "title": "Melbourne update", "country": "Australia", "latitude": -37.8136, "longitude": 144.9631 },
            { "city": "São Paulo", "url": "https://example.com/news/sao-paulo", "title": "São Paulo update", "country": "Brazil", "latitude": -23.5505, "longitude": -46.6333 }
        ]



        
        return Response(Mass_Articles, status=status.HTTP_200_OK)           #return the points after successful data gathering
        

class Agent(APIView):
    
    def post(self,request,format=None):
        return