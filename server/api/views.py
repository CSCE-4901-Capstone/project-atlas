import time
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import Gemini_API
from .services import WeatherAPI

from api.models import FlightModel
from api.serializers import FlightSerializer
from api.services import FlightAPI

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



class TravelCountry(APIView):                #handles connection to external API for AI interaction 

        AI_gemini = Gemini_API()
    
        def post(self,request):
                prompt = request.data.get("prompt","")
                result = AI_gemini.EnterPrompt(prompt)                  #calling function within gemini class to send the prompt to the API per django requirements
        
                return Response({"response":result}) 
        
class WeatherGridView(APIView):
    """
    Fills and returns a 2D temperature grid based on OpenWeatherMap
    """        
    api = WeatherAPI()

    def get(self, request, format=None):
        try:
            #Sample grid
            sample_points = [
                (lat,lon)
                for lat in range(-45, 45, 10)
                for lon in range(-35, 145, 10)
            ]
            grid = self.api.fill_grid(sample_points)

            #return dimensions
            return Response({
                "width": self.api.cols,
                "height": self.api.rows,
                "data": grid
            },status=status.HTTP_200_OK)
        except Exception as e:
            print(" WeatherGridView error:", e)
            return Response({"error": str(e)}, status=500)