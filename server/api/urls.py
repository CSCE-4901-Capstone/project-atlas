from django.urls import path
from api.views import FlightList, CountryNews

urlpatterns = [
        path('flights/', FlightList.as_view()),
        path('AI/', CountryNews.as_view())
]
 
 
 