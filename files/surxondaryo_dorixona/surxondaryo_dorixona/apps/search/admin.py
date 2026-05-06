from django.contrib import admin
from .models import SearchHistory


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('query', 'region', 'results_count', 'user', 'searched_at')
    list_filter = ('region', 'searched_at')
    search_fields = ('query', 'user__username', 'ip_address')
    readonly_fields = (
        'user', 'query', 'region', 'results_count',
        'user_lat', 'user_lng', 'ip_address', 'user_agent', 'searched_at'
    )
    date_hierarchy = 'searched_at'
