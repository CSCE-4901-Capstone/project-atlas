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



class CountryNews(APIView):                #handles connection to external API for AI interaction 

        AI_Gemini = Gemini_API()
    
        def post(self,request,format=None):                             #this method is used to post the initial travel prompt to the GPT_API
                country = request.data.get("country")  #from the post request sent fron AISummary.jsx read in the country value and store it.
                Role_choice = request.data.get("Role_choice")
                
                prompt = f'''Give me a list of 5 articles about major events that are occurring within {country}. 
                        Return it in a JSON format where it has a list called articles where each entry has a title, 
                        description, source and link. ONLY GIVE THE JSON, NO MARKDOWN!!!!!'''
                
                result = self.AI_Gemini.EnterPrompt_C_Data(prompt,Role_choice)                  #calling function within gemini class to send the prompt to the API per django requirements
                return Response({"response":result}, status=status.HTTP_200_OK) 
                
#TODO: MAKE ANOTHER VIEW THAT DOES THE TRAVEL INFORMATION AS WELL.    
#prompt = f"the country in question is {country}. ONLY RETURN a list of important documents needed for travel to the country!" #reformat the recieved county into the prompt for the model
