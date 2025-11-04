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
from api.services import FlightAPI,NEWS_API,Agentic_AI, DisasterAPI     #,Gemini_API,

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

    NEWS = NEWS_API()

    def get(self,request,format=None):             #GET request for all the articles needed to populate congestion
        #in future: optimize to also account for first_20, second_20, etc.



        #Would Work, but NEWS API wants $500 USD monthly.... we are figuring out a workaround
        #Mass_Articles = self.NEWS.NewsPointBuilder(self.NEWS.first_20)

        Mass_Articles = [
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/india/shah-banos-daughter-sends-legal-notice-to-emraan-hashmi-yami-gautams-haq/articleshow/125047347.cms",
    "title": "Shah Bano's daughter sends legal notice to Emraan Hashmi, Yami Gautam's 'HAQ'",
    "country": "India",
    "latitude": 19.0760,
    "longitude": 72.8777
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/news/new-updates/indians-went-crazy-after-south-africa-captain-laura-wolvaardt-thanks-team-india-on-twitter-it-turned-out-to-be-fake/articleshow/125047331.cms",
    "title": "Indians went crazy after South Africa Captain Laura Wolvaardt thanks Team India on Twitter, it turned out to be fake",
    "country": "India",
    "latitude": 19.0751,
    "longitude": 72.8786
  },
  {
    "city": "Mumbai",
    "url": "https://m.economictimes.com/markets/stocks/news/a-measured-move-opec-balances-growth-with-caution/opec-balances-expectations-and-caution/slideshow/125047485.cms",
    "title": "A Measured Move: OPEC+ balances growth with caution",
    "country": "India",
    "latitude": 19.0769,
    "longitude": 72.8768
  },
  {
    "city": "Mumbai",
    "url": "https://economictimes.indiatimes.com/tech/technology/pine-labs-ipo-could-unlock-esops-worth-rs-1360-crore/articleshow/125047189.cms",
    "title": "Pine Labs IPO could unlock Esops worth Rs 1,360 crore",
    "country": "India",
    "latitude": 19.0755,
    "longitude": 72.8789
  },
  {
    "city": "Gurgaon",
    "url": "https://indianexpress.com/article/cities/delhi/breakthrough-gurgaon-police-arrest-fugitive-gangster-deepak-nandal-rohtak-10342837/",
    "title": "In another breakthrough, Gurgaon police arrest key associate of fugitive gangster Deepak Nandal in Rohtak",
    "country": "India",
    "latitude": 28.4595,
    "longitude": 77.0266
  },
  {
    "city": "Mumbai",
    "url": "https://www.indiatimes.com/trending/haq-real-story-shah-bano-fight-for-justice-after-husband-abandoned-her-yami-gautam-emraan-hashmi/articleshow/125046584.html",
    "title": "Haq real story: Shah Bano's historic fight for justice after her husband abandoned her",
    "country": "India",
    "latitude": 19.0775,
    "longitude": 72.8752
  },
  {
    "city": "Chennai",
    "url": "https://www.thehindubusinessline.com/markets/stock-markets/markets-open-flat-amid-mixed-global-cues-shriram-finance-leads-gainers-with-5-rally/article70234957.ece",
    "title": "Markets open flat amid mixed global cues; Shriram Finance leads gainers with 5% rally",
    "country": "India",
    "latitude": 13.0827,
    "longitude": 80.2707
  },
  {
    "city": "Mumbai",
    "url": "https://www.rediff.com/movies/report/revealed-when-juhi-met-shah-rukh-for-the-first-time/20251103.htm",
    "title": "REVEALED! When Juhi Met SRK For 1st Time!",
    "country": "India",
    "latitude": 19.0746,
    "longitude": 72.8793
  },
  {
    "city": "Delhi",
    "url": "https://economictimes.indiatimes.com/news/science/pm-modi-launches-rs-1-lakh-crore-rdi-fund-to-spur-private-investment-in-research-development/articleshow/125047079.cms",
    "title": "PM Modi launches Rs 1 lakh crore RDI Fund to spur private investment in research & development",
    "country": "India",
    "latitude": 28.6139,
    "longitude": 77.2090
  },
  {
    "city": "Melbourne",
    "url": "https://berwicknews.starcommunity.com.au/sport/2025-11-03/cricket-world-rallies-together/",
    "title": "Cricket world rallies together",
    "country": "Australia",
    "latitude": -37.8136,
    "longitude": 144.9631
  }
]

        return Response(Mass_Articles, status=status.HTTP_200_OK)           #return the points after successful data gathering


class Agent(APIView):

    api = Agentic_AI()          #make instance of the Agentic AI class to use in the frontend

    def post(self,request,format=None):
        #print recieved data from post request of frontend
        print("request.data:", request.data)

        CountryChoice = request.data.get("country")             #from the post request sent fron AISummary.jsx read in the country value and store it.
        SessionNum = request.data.get("session")

        if not CountryChoice:
            return Response({"error": "No Country Passed/detected for Agent(APIView)"},status=status.HTTP_400_BAD_REQUEST)

        result = self.api.Holistic_View(CountryChoice,SessionNum)          #make call for the Holistic_View of the AI_Agent

        #error checking for News_API to see if correct output was recieved
        #if result.get("error"):
        #    return Response(result, status=status.HTTP_502_BAD_GATEWAY)     #flag if invalid output was recieved

        return Response(result, status=status.HTTP_200_OK)      #return good output if nothing wrong was detected

class DisasterList(APIView):
    """
    Handles the connection to the external disaster api
    """
    api = DisasterAPI()

    def get(self, request, format=None):
        disasters = self.api.fetch_data()
        return Response(disasters, status=status.HTTP_200_OK)

