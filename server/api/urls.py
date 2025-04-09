from django.urls import path
from api.views import FlightList
from api.views import WeatherGridView

urlpatterns = [
        path('flights/', FlightList().as_view()),
        path('weather-grid/', WeatherGridView().as_view()),
]