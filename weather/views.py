import logging
import requests
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import SearchHistory
from .serializers import SearchHistorySerializer
from weatherforecast import settings


logger = logging.getLogger(__name__)


class WeatherTemplateView(TemplateView):
    template_name = 'weather/weather.html'


class WeatherView(APIView):
    def get(self, request, city):
        user = request.user
        if user.is_authenticated:
            history, created = SearchHistory.objects.get_or_create(user=user, city=city)
            if not created:
                history.search_count += 1
                history.save()

        # Получение координат города
        geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={settings.OPENWEATHER_API_KEY}"
        geocode_response = requests.get(geocode_url).json()
        if not geocode_response:
            logger.error(f"City not found: {city}")
            return Response({"error": "City not found"}, status=status.HTTP_404_NOT_FOUND)

        lat = geocode_response[0]['lat']
        lon = geocode_response[0]['lon']

        # Получение прогноза погоды
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&hourly=precipitation&hourly=windspeed_10m&start=now&end=tomorrow"
        weather_response = requests.get(weather_url).json()

        if 'error' in weather_response:
            logger.error(f"Error fetching weather data: {weather_response['reason']}")
            return Response({"error": weather_response['reason']}, status=status.HTTP_400_BAD_REQUEST)

        return Response(weather_response, status=status.HTTP_200_OK)
