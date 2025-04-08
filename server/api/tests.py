from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class WeatherAPITest(APITestCase):
    def test_get_weather_data(self):
        url = reverse('weather-list')  # match this to your urls.py name if needed
        response = self.client.get(f"{url}?lat=32.7767&lon=-96.7970")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('temperature', response.data)