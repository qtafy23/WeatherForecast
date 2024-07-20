from django.urls import path
from .views import WeatherView, WeatherTemplateView, city_autocomplete

app_name = 'Weather'

urlpatterns = [
    path('', WeatherTemplateView.as_view(), name='weather_view'),
    path('weather/<str:city>/', WeatherView.as_view(), name='weather'),
    path('city-autocomplete/', city_autocomplete, name='city-autocomplete'),
]
