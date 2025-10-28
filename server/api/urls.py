from django.urls import path
from api.views import FlightList, CountryNews, Agent, Heatmap, DisasterList, PopulationView     #import the classes to be used from views.py
from api.views import WeatherGridView
from api.views import PrecipitationGridView


urlpatterns = [
        path('flights/', FlightList().as_view()),
        path("weather/", WeatherGridView.as_view(), name="weather-grid"),
        path('AI/', CountryNews.as_view()),
        path('NewsCongestion/',Heatmap.as_view()),
        path('Agent/', Agent.as_view()),
        path('precipitation/', PrecipitationGridView.as_view(), name='precipitation-grid'),
        path('disaster/', DisasterList().as_view()),
        path('population/', PopulationView.as_view()),


]
