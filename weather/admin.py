from django.contrib import admin
from .models import SearchHistory


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'search_count', 'last_searched')
    search_fields = ('user__username', 'city')
    list_filter = ('city', 'last_searched')
    ordering = ('-last_searched',)
