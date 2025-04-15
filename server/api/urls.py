from django.urls import path
from api.views import FlightList, CountryNews
from api.views import WeatherGridView

urlpatterns = [
        path('flights/', FlightList().as_view()),
        path('weather/', WeatherGridView().as_view()),
        path('AI/', CountryNews.as_view())
]
