from django.urls import path
from api.views import FlightList, TravelCountry

urlpatterns = [
        path('flights/', FlightList.as_view()),
        path('AI/', TravelCountry.as_view())
]
 