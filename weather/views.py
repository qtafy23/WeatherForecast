import logging
import requests
from django.http import JsonResponse
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import UserSearchHistory, SearchHistory
from weatherforecast import settings


logger = logging.getLogger(__name__)


def city_autocomplete(request):
    if 'term' in request.GET:
        term = request.GET.get('term')
        geocode_url = (
            f'{settings.GEC_URL}q={term}&limit=5'
            f'&appid={settings.OPENWEATHER_API_KEY}'
        )

        try:
            # Выполнение запроса к API
            geocode_response = requests.get(geocode_url).json()
            suggestions = []

            # Проверка, что ответ является списком
            if isinstance(geocode_response, list):
                for result in geocode_response:
                    if isinstance(result, dict):
                        city_name = result.get('name', '')
                        country = result.get('country', '')
                        if city_name and country:
                            suggestions.append(f"{city_name}, {country}")
            else:
                # Обработка неожидаемого формата ответа
                return JsonResponse(
                    {'error': 'Неожиданный формат ответа'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return JsonResponse(suggestions, safe=False)
        except requests.RequestException as e:
            # Обработка ошибки запроса
            return JsonResponse(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    return JsonResponse([], safe=False)


class WeatherTemplateView(TemplateView):
    template_name = 'weather/weather.html'


class WeatherView(APIView):
    def get(self, request, city):
        request.session['last_city'] = city

        cityhistory, created = SearchHistory.objects.get_or_create(city=city)
        if not created:
            cityhistory.search_count += 1
            cityhistory.save()

        user = request.user
        if user.is_authenticated:
            history, created = UserSearchHistory.objects.get_or_create(
                user=user, city=cityhistory
            )
            if not created:
                history.search_count += 1
                history.save()

        # Получение координат города
        geocode_url = (
            f"{settings.GEC_URL}q={city}&limit=1"
            f"&appid={settings.OPENWEATHER_API_KEY}"
        )
        geocode_response = requests.get(geocode_url).json()
        if not geocode_response:
            logger.error(f"City not found: {city}")
            return Response(
                {"error": "City not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        lat = geocode_response[0]['lat']
        lon = geocode_response[0]['lon']

        # Получение прогноза погоды
        weather_url = (
            f"{settings.WEATHER_URL}={lat}&longitude={lon}"
            f"&hourly=temperature_2m&hourly=precipitation"
            f"&hourly=windspeed_10m&start=now&end=tomorrow"
        )
        weather_response = requests.get(weather_url).json()

        if 'error' in weather_response:
            logger.error(
                f"Error fetching weather data: {weather_response['reason']}"
            )
            return Response(
                {"error": weather_response['reason']},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(weather_response, status=status.HTTP_200_OK)


class LastCityView(APIView):
    def get(self, request):
        last_city = request.session.get('last_city', None)
        return Response({'last_city': last_city}, status=status.HTTP_200_OK)
