from django.db import models
from django.contrib.auth.models import User


class SearchHistory(models.Model):
    city = models.CharField(max_length=124)
    search_count = models.IntegerField(default=1)
    last_searched = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city} ({self.search_count} times)"


class UserSearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey(SearchHistory, on_delete=models.CASCADE)
    search_count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.cities}"
