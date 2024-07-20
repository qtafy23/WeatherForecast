from django.db import models
from django.contrib.auth.models import User

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=124)
    search_count = models.IntegerField(default=1)
    last_searched = models.DateTimeField(auto_now=True)
