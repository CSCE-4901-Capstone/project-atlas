from django.urls import path
from api.views import FlightList

urlpatterns = [
        path('flights/', FlightList().as_view())
]

