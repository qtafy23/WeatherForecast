from django.urls import path
from .views import WeatherView, home, city_autocomplete, some_view


app_name = 'Weather'

urlpatterns = [
    path('', home, name='home'),
    path('weather/<str:city>/', WeatherView.as_view(), name='weather'),
    path('city-autocomplete/', city_autocomplete, name='city-autocomplete'),
]
