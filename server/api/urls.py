from django.urls import path
from api.views import FlightList, GenerateGPT_ResponseList

urlpatterns = [
        path('flights/', FlightList.as_view())
        path('AI/', GenerateGPT_ResponseList.as_view())
]
 
 
 