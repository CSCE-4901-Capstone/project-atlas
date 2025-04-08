import time
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import FlightModel
from api.serializers import FlightSerializer
from api.services import FlightAPI, Gemini_API

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



class GenerateGPT_ResponseList(APIView):                #handles connection to external API for AI interaction 

        AI_gemini = Gemini_API()
    
        def post(self,request,format=None):
                prompt = request.data.get("prompt","")
                result = self.AI_gemini.EnterPrompt_C_Data(prompt)                  #calling function within gemini class to send the prompt to the API per django requirements
        
                return Response({"response":result}) 
