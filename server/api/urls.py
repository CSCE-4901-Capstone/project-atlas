from django.urls import path
from api.views import FlightList, CountryNews, Agent
from api.views import WeatherGridView


urlpatterns = [
        path('flights/', FlightList().as_view()),
        path("weather/", WeatherGridView.as_view(), name="weather-grid"),
        path('AI/', CountryNews.as_view()),
        path('Agent/', Agent.as_view())
]
