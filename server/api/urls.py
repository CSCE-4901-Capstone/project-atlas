from django.urls import path
from .views import FlightList, AI_Model

urlpatterns = [
        path('flights/', views.FlightList().as_view())
]
 