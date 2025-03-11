from django.urls import path
from . import views

urlpatterns = [
        path('flights/', views.FlightList().as_view())
]
