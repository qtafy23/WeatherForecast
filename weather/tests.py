from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserSearchHistory


class WeatherTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_user_search_history_creation(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get('/weather/London/')
        self.assertEqual(response.status_code, 200)
        history = UserSearchHistory.objects.get(user=self.user, city='London')
        self.assertEqual(history.search_count, 1)
