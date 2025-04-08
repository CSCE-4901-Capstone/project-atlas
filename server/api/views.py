import time
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import FlightModel
from api.serializers import FlightSerializer
from api.services import FlightAPI

from api.models import WeatherModel
from api.serializers import WeatherSerializer
from api.services import WeatherAPI

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
    
class WeatherList(APIView):
    """
    Connects to OpenWeatherMap and return data by coordinates
    """
    api_weather = WeatherAPI()

    def get(self, request, format=None):
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')

        weather = self.api.fetch_weather()
        return Response(weather, status=status.HTTP_200_OK)